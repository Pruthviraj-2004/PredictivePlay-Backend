from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *

from django.utils.timezone import now, timedelta


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "predictiveplayapp/homepage.html")



class LoginView(View):
    def get(self, request):
        return render(request, "predictiveplayapp/login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home") 
        else:
            return render(request, "predictiveplayapp/login.html", {"error": "Invalid credentials"})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")

class RegisterView(View):
    template_name = "predictiveplayapp/register.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST["username"]
        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        self.create_user_info(user, username, name, email)


        login(request, user)
        return redirect("home")
    
    def create_user_info(self, user, username, name, email):
        """ Creates a UserInfo record linked to the newly registered User """
        UserInfo.objects.create(
            user=user,
            username=username,
            name=name,
            email=email,  # Automatically stored using EncryptedEmailField
        )



class RegisterStep1View(View):
    template_name = "predictiveplayapp/register_step1.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST["username"]
        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            return render(request, self.template_name, {"error": "Username already taken!"})
        
        if User.objects.filter(email=email).exists():
            return render(request, self.template_name, {"error": "Email already registered!"})

        # Store in session to pass to the next step
        request.session["username"] = username
        request.session["name"] = name
        request.session["email"] = email
        request.session["password"] = password

        return redirect("register_step2")  # Redirect to Step 2


class RegisterStep2View(View):
    template_name = "predictiveplayapp/register_step2.html"

    def get(self, request):
        if "username" not in request.session:
            return redirect("register_step1")  # Redirect if Step 1 is not completed
        return render(request, self.template_name)

    def post(self, request):
        leaderboard_name = request.POST["leaderboardName"]
        leaderboard_password = request.POST["leaderboardPassword"]

        # Retrieve user details from session
        username = request.session.get("username")
        name = request.session.get("name")
        email = request.session.get("email")
        password = request.session.get("password")

        # Validate leaderboard credentials
        try:
            leaderboard = Leaderboard.objects.get(leaderboardName=leaderboard_name)
            if leaderboard.leaderboardPassword != leaderboard_password:
                return render(request, self.template_name, {"error": "Incorrect leaderboard password!"})
        except Leaderboard.DoesNotExist:
            return render(request, self.template_name, {"error": "Leaderboard not found!"})

        # Create User & UserInfo
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        UserInfo.objects.create(user=user, username=username, name=name, email=email)

        # Add user to LeaderboardMember
        LeaderboardMember.objects.create(user=user, leaderboard=leaderboard)

        # Log the user in and redirect to home
        login(request, user)
        return redirect("home")



#ViewClasses related to Fixtures Page
class FixturePageCricketTournamentView(APIView):
    def get(self, request):
        upcoming_tournaments = CricketTournament.objects.filter(status=0)
        ongoing_tournaments = CricketTournament.objects.filter(status=1)
        completed_tournaments = CricketTournament.objects.filter(status=2)
        
        upcoming_serializer = ALLCricketTournamentSerializer(upcoming_tournaments, many=True)
        ongoing_serializer = ALLCricketTournamentSerializer(ongoing_tournaments, many=True)
        completed_serializer = ALLCricketTournamentSerializer(completed_tournaments, many=True)

        response_data = {
            "Ongoing": ongoing_serializer.data,
            "Upcoming": upcoming_serializer.data,
            "Completed": completed_serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
class FixturePageMatchesByTournamentView(APIView):
    def get(self, request, eventID):
        matches = Match.objects.filter(event__eventID=eventID)
        
        if not matches.exists():
            return Response({"error": "No matches found for this tournament"}, status=status.HTTP_404_NOT_FOUND)

        grouped_matches = {status_label: [] for _, status_label in Match.STATUS_CHOICES}

        for match in matches:
            status_label = dict(Match.STATUS_CHOICES).get(match.status, "Unknown")
            grouped_matches[status_label].append(FixturePageMatchSerializer(match).data)

        return Response(grouped_matches, status=status.HTTP_200_OK)



#ViewClasses related to PredictPage
class MatchDetailView(APIView):
    def get(self, request, matchID):
        try:
            match = Match.objects.get(matchID=matchID)
            serializer = MatchDetailSerializer(match, context={"match": match})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Match.DoesNotExist:
            return Response({"error": "Match not found"}, status=status.HTTP_404_NOT_FOUND)

class NewMatchDetailView(APIView):
    def get(self, request, matchID):
        try:
            match = Match.objects.get(matchID=matchID)
            context = {"match": match}

            teams = [match.team1, match.team2]
            teams_data = NewTeamSerializer(teams, many=True, context=context).data

            manOfTheMatchPlayers = Player.objects.filter(playing11status=0)
            mostRunsScorerPlayers = Player.objects.filter(playing11status=0, playerRole__in=[0, 2])
            mostWicketsTakerPlayers = Player.objects.filter(playing11status=0, playerRole__in=[1,2])

            match_data = {
                "matchID": match.matchID,
                "eventID": match.event.eventID,
                "teams": teams_data,
                "manOfTheMatchPlayers": NewPlayerSerializer(
                    manOfTheMatchPlayers, many=True, context={**context, "category": "manOfTheMatch"}
                ).data,
                "mostRunsScorerPlayers": NewPlayerSerializer(
                    mostRunsScorerPlayers, many=True, context={**context, "category": "mostRunsScorer"}
                ).data,
                "mostWicketsTakerPlayers": NewPlayerSerializer(
                    mostWicketsTakerPlayers, many=True, context={**context, "category": "mostWicketsTaker"}
                ).data,
                "matchDate": match.matchDate.strftime("%d-%m-%Y"),
                "matchStartTime1st": match.matchStartTime1st.strftime("%H:%M:%S"),
                "matchStartTime2nd": match.matchStartTime2nd.strftime("%H:%M:%S") if match.matchStartTime2nd else None,
                "location": match.location,
                "status": match.status,
            }

            return Response(match_data, status=status.HTTP_200_OK)
        except Match.DoesNotExist:
            return Response({"error": "Match not found"}, status=status.HTTP_404_NOT_FOUND)



#ProfilePage
#Graph1
class UserScoreGraphView(APIView):
    def get(self, request, username, eventID, leaderboardID):
        user = get_object_or_404(User, username=username)
        leaderboard = get_object_or_404(Leaderboard, leaderboardID=leaderboardID)

        if not LeaderboardMember.objects.filter(leaderboard=leaderboard, user=user).exists():
            return Response({"error": "User is not a member of this leaderboard"}, status=status.HTTP_403_FORBIDDEN)

        days_filter = request.GET.get('days', '7')

        if days_filter == '7':
            date_threshold = now() - timedelta(days=7)
        elif days_filter == '14':
            date_threshold = now() - timedelta(days=14)
        else:
            date_threshold = None

        submissions = Submission.objects.filter(user=user, match__event_id=eventID)
        if date_threshold:
            submissions = submissions.filter(match__matchDate__gte=date_threshold)

        filtered_submissions = []
        for submission in submissions:
            if hasattr(submission, "submissionScores") and isinstance(submission.submissionScores, dict):
                if str(leaderboardID) in submission.submissionScores:
                    submission.submissionScores = {
                        str(leaderboardID): submission.submissionScores[str(leaderboardID)]
                    }
                    filtered_submissions.append(submission)
            else:
                if leaderboardID == 1:
                    submission.submissionScores = {str(leaderboardID): 0}
                    filtered_submissions.append(submission)

        data = UserMatchScoreSerializer(filtered_submissions, many=True).data
        return Response({"scores": data}, status=status.HTTP_200_OK)

#Graph2
class UserOverallScoreGraphView(APIView):
    def get(self, request, username, eventID):
        user = get_object_or_404(User, username=username)

        submissions = Submission.objects.filter(user=user, match__event_id=eventID).order_by("match__matchDate")

        total_matches_user_submitted = submissions.count()
        total_matches_event = Match.objects.filter(event_id=eventID).count()

        leaderboard_ids = set()
        for submission in submissions:
            leaderboard_ids.update(submission.submissionScores.keys())

        graph_data = {leaderboard_id: [] for leaderboard_id in leaderboard_ids}

        for submission in submissions:
            match_data = {
                "match_id": submission.match.matchID,
            }

            for leaderboard_id in leaderboard_ids:
                match_data["score"] = submission.submissionScores.get(str(leaderboard_id), 0)
                graph_data[leaderboard_id].append(match_data.copy())

        return Response({"graphData": graph_data, "total_matches_user_submitted":total_matches_user_submitted, "total_matches_event":total_matches_event}, status=status.HTTP_200_OK)

#KPIs
class EventKPIsView(APIView):
    def get(self, request, eventID):
        event = get_object_or_404(CricketTournament, eventID=eventID)

        total_matches = Match.objects.filter(event_id=eventID).count()
        completed_matches = Match.objects.filter(event_id=eventID, status=2).count()
        upcoming_matches = Match.objects.filter(event_id=eventID, status=0).count()

        data = {
            "eventID": eventID,
            "eventName": event.eventName,
            "KPIs": {
                "totalMatches": total_matches,
                "completedMatches": completed_matches,
                "upcomingMatches": upcoming_matches,
            }
        }

        return Response(data, status=status.HTTP_200_OK)


class UserLeaderboardsView(APIView):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)

        # Get all leaderboards where the user is a member
        leaderboard_memberships = LeaderboardMember.objects.filter(user=user).select_related('leaderboard')

        if not leaderboard_memberships.exists():
            return Response({"error": "User is not part of any leaderboard"}, status=status.HTTP_404_NOT_FOUND)

        # Serialize and return data
        data = UserLeaderboardsSerializer(leaderboard_memberships, many=True).data
        return Response({"leaderboards": data}, status=status.HTTP_200_OK)


#Profile page cricket tournaments list
class ProfilePageTournamentListView(APIView):
    def get(self, request):
        tournaments = CricketTournament.objects.all()

        ongoing = tournaments.filter(status=1)
        completed = tournaments.filter(status=2)

        data = {
            "ongoing": ProfilePageCricketTournamentSerializer(ongoing, many=True).data,
            "completed": ProfilePageCricketTournamentSerializer(completed, many=True).data
        }

        return Response(data, status=status.HTTP_200_OK)   


#Profile page all submissions of selected event
class UserEventSubmissionsView(APIView):
    def get(self, request, username, eventID):
        user = get_object_or_404(User, username=username)

        # Get all submissions for the given user and event
        submissions = Submission.objects.filter(user=user, match__event_id=eventID).select_related('match')

        if not submissions.exists():
            return Response({"error": "No submissions found for this event"}, status=status.HTTP_404_NOT_FOUND)

        # Serialize and return data
        data = UserEventSubmissionsSerializer(submissions, many=True).data
        return Response({"submissions": data}, status=status.HTTP_200_OK)
  



#LeaderBoard page

# class CommonLeaderboardRankingsView(APIView):
#     def get(self, request):
#         leaderboard_ids = ["1", "2"]
        
#         rankings = {leaderboard_id: [] for leaderboard_id in leaderboard_ids}

#         recent_match = Match.objects.filter(matchDate__lte=now().date()).order_by("-matchDate", "-matchStartTime1st").first()

#         users = User.objects.all()

#         for user in users:
#             user_scores = {lb_id: 0 for lb_id in leaderboard_ids}
#             recent_gained_points = {lb_id: 0 for lb_id in leaderboard_ids}

#             submissions = Submission.objects.filter(user=user)
#             for submission in submissions:
#                 for lb_id in leaderboard_ids:
#                     user_scores[lb_id] += submission.submissionScores.get(lb_id, 0)

#             if recent_match:
#                 recent_submission = submissions.filter(match=recent_match).first()
#                 if recent_submission:
#                     for lb_id in leaderboard_ids:
#                         recent_gained_points[lb_id] = recent_submission.submissionScores.get(lb_id, 0)

#             for lb_id in leaderboard_ids:
#                 if user_scores[lb_id] > 0 or recent_gained_points[lb_id] > 0:
#                     rankings[lb_id].append({
#                         "username": user.username,
#                         "points": user_scores[lb_id],
#                         "recent_gained_points": recent_gained_points[lb_id]
#                     })

#         for lb_id in leaderboard_ids:
#             rankings[lb_id].sort(key=lambda x: x["points"], reverse=True)

#             for rank, entry in enumerate(rankings[lb_id], start=1):
#                 entry["rank"] = rank

#         return Response(rankings, status=status.HTTP_200_OK)

from django.db.models import Count

# class CommonLeaderboardRankingsView(APIView):
#     def get(self, request):
#         leaderboards = Leaderboard.objects.filter(leaderboardID__in=[1, 2]).annotate(
#             participant_count=Count("leaderboardmember")
#         ).values("leaderboardID", "leaderboardName", "participant_count")

#         leaderboard_data = []
#         recent_match = Match.objects.filter(
#             matchDate__lte=now().date()
#         ).order_by("-matchDate", "-matchStartTime1st").first()

#         for lb in leaderboards:
#             rankings = (
#                 LeaderboardMember.objects.filter(leaderboard__leaderboardID=lb["leaderboardID"])
#                 .select_related("user")
#                 .values("user__username", "points")
#                 .order_by("-points", "user__username")
#             )

#             ranked_users = []
#             for rank, entry in enumerate(rankings, start=1):
#                 user = entry["user__username"]
#                 points = entry["points"]
                
#                 recent_points = 0
#                 if recent_match:
#                     recent_submission = Submission.objects.filter(
#                         user__username=user, match=recent_match
#                     ).first()
#                     if recent_submission:
#                         recent_points = recent_submission.submissionScores.get(str(lb["leaderboardID"]), 0)

#                 ranked_users.append({
#                     "rank": rank,
#                     "username": user,
#                     "points": points,
#                     "recentGainedPoints": recent_points
#                 })

#             leaderboard_data.append({
#                 "leaderboardID": lb["leaderboardID"],
#                 "leaderboardName": lb["leaderboardName"],
#                 "participantCount": lb["participant_count"],
#                 "rankings": ranked_users
#             })

#         return Response({"leaderboards": leaderboard_data}, status=status.HTTP_200_OK)


class CommonLeaderboardRankingsView(APIView):
    def get(self, request, eventID):
        # Fetch leaderboards with names "Global" and "Weekly" under the given eventID
        leaderboards = Leaderboard.objects.filter(
            event__eventID=eventID, leaderboardName__in=["Global", "Weekly"]
        ).annotate(
            participant_count=Count("leaderboardmember")
        ).values("leaderboardID", "leaderboardName", "participant_count")

        leaderboard_data = []
        recent_match = Match.objects.filter(
            event__eventID=eventID, 
            matchDate__lte=now().date()
        ).order_by("-matchDate", "-matchStartTime1st").first()

        for lb in leaderboards:
            rankings = (
                LeaderboardMember.objects.filter(
                    leaderboard__leaderboardID=lb["leaderboardID"]
                )
                .select_related("user")
                .values("user__username", "points")
                .order_by("-points", "user__username")
            )

            ranked_users = []
            for rank, entry in enumerate(rankings, start=1):
                user = entry["user__username"]
                points = entry["points"]

                recent_points = 0
                if recent_match:
                    recent_submission = Submission.objects.filter(
                        user__username=user, 
                        match=recent_match
                    ).first()
                    if recent_submission:
                        recent_points = recent_submission.submissionScores.get(str(lb["leaderboardID"]), 0)

                ranked_users.append({
                    "rank": rank,
                    "username": user,
                    "points": points,
                    "recentGainedPoints": recent_points
                })

            leaderboard_data.append({
                "leaderboardID": lb["leaderboardID"],
                "leaderboardName": lb["leaderboardName"],
                "participantCount": lb["participant_count"],
                "rankings": ranked_users
            })

        return Response({"leaderboards": leaderboard_data}, status=status.HTTP_200_OK)
