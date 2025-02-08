from rest_framework import serializers
from .models import *

class ALLCricketTournamentSerializer(serializers.ModelSerializer):
    eventStartDate = serializers.DateField(format="%d-%m-%Y")
    eventEndDate = serializers.DateField(format="%d-%m-%Y")
    status = serializers.SerializerMethodField()
    class Meta:
        model = CricketTournament
        fields = ['eventID', 'eventName', 'eventStartDate', 'eventEndDate', 'status']
    
    def get_status(self, obj):
        return obj.get_status_display()

class ALLMatchSerializer(serializers.ModelSerializer):
    eventID = serializers.IntegerField(source='tournament.eventID', read_only=True)  # Send only eventID

    class Meta:
        model = Match
        fields = ['matchID', 'eventID', 'team1', 'team2', 'matchDate', 'matchStartTime1st', 'matchStartTime2nd', 'location']

class HomePageCricketTournamentSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    class Meta:
        model = CricketTournament
        fields = ["eventID", "eventName", "status"]

    def get_status(self, obj):
        return obj.get_status_display()



#Serializers Related to Fixtures Page
class FixturePageTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['teamID', 'teamName', 'teamShortForm']

class FixturePageMatchSerializer(serializers.ModelSerializer):
    eventID = serializers.PrimaryKeyRelatedField(source='event', read_only=True)
    team1 = FixturePageTeamSerializer(read_only=True)
    team2 = FixturePageTeamSerializer(read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = ['matchID', 'eventID', 'team1', 'team2', 'matchDate', 'matchStartTime1st', 'matchStartTime2nd', 'location', 'status']

    def get_status(self, obj):
        return dict(Match.STATUS_CHOICES).get(obj.status, "Unknown")



#Serializers related to PredictPage
class PlayerSerializer(serializers.ModelSerializer):
    mostRunsScorerPercentage = serializers.SerializerMethodField()
    mostWicketsTakerPercentage = serializers.SerializerMethodField()
    manOfTheMatchPercentage = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ['playerID', 'playerName', 'manOfTheMatchPercentage', 'mostRunsScorerPercentage', 'mostWicketsTakerPercentage']

    def get_mostRunsScorerPercentage(self, obj):
        match = self.context.get("match")
        return self.get_selection_percentage(match, obj, field="mostRunsScorer")

    def get_mostWicketsTakerPercentage(self, obj):
        match = self.context.get("match")
        return self.get_selection_percentage(match, obj, field="mostWicketsTaker")

    def get_manOfTheMatchPercentage(self, obj):
        match = self.context.get("match")
        return self.get_selection_percentage(match, obj, field="manOfTheMatch")

    def get_selection_percentage(self, match, player, field):
        if not match:
            return 0

        total_submissions = Submission.objects.filter(match=match).count()
        selected_count = Submission.objects.filter(match=match, **{field: player}).count()

        return round((selected_count / total_submissions) * 100, 2) if total_submissions > 0 else 0

class TeamWithPlayersSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True, source='player_set')
    winningTeamPercentage = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['teamID', 'teamName', 'teamShortForm', 'winningTeamPercentage', 'players']

    def get_winningTeamPercentage(self, obj):
        match = self.context.get("match")
        return self.get_selection_percentage(match, obj)

    def get_selection_percentage(self, match, team):
        if not match:
            return 0

        total_submissions = Submission.objects.filter(match=match).count()
        selected_count = Submission.objects.filter(match=match, winningTeam=team).count()

        return round((selected_count / total_submissions) * 100, 2) if total_submissions > 0 else 0

class MatchDetailSerializer(serializers.ModelSerializer):
    eventID = serializers.PrimaryKeyRelatedField(source='event', read_only=True)
    teamA = TeamWithPlayersSerializer(source='team1', read_only=True)
    teamB = TeamWithPlayersSerializer(source='team2', read_only=True)

    class Meta:
        model = Match
        fields = [
            'matchID', 'eventID', 'teamA', 'teamB', 'matchDate',
            'matchStartTime1st', 'matchStartTime2nd', 'location', 'status'
        ]



#New serializers for PredictPage
# class NewPlayerSerializer(serializers.ModelSerializer):
#     teamShortForm = serializers.CharField(source="team.teamShortForm", read_only=True)
#     manOfTheMatchPercentage = serializers.SerializerMethodField()
#     mostRunsScorerPercentage = serializers.SerializerMethodField()
#     mostWicketsTakerPercentage = serializers.SerializerMethodField()

#     class Meta:
#         model = Player
#         fields = ['playerID', 'playerName', 'teamShortForm', 'manOfTheMatchPercentage', 'mostRunsScorerPercentage', 'mostWicketsTakerPercentage']

#     def get_manOfTheMatchPercentage(self, obj):
#         return self.get_percentage(obj, "manOfTheMatch")

#     def get_mostRunsScorerPercentage(self, obj):
#         return self.get_percentage(obj, "mostRunsScorer")

#     def get_mostWicketsTakerPercentage(self, obj):
#         return self.get_percentage(obj, "mostWicketsTaker")

#     def get_percentage(self, obj, field):
#         match = self.context.get("match")
#         if not match:
#             return 0

#         total_submissions = Submission.objects.filter(match=match).count()
#         selected_count = Submission.objects.filter(match=match, **{field: obj}).count()

#         return round((selected_count / total_submissions) * 100, 2) if total_submissions > 0 else 0

class NewPlayerSerializer(serializers.ModelSerializer):
    teamShortForm = serializers.CharField(source="team.teamShortForm", read_only=True)
    manOfTheMatchPercentage = serializers.SerializerMethodField()
    mostRunsScorerPercentage = serializers.SerializerMethodField()
    mostWicketsTakerPercentage = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ['playerID', 'playerName', 'teamShortForm', 'manOfTheMatchPercentage', 'mostRunsScorerPercentage', 'mostWicketsTakerPercentage']

    def get_manOfTheMatchPercentage(self, obj):
        return self.get_percentage(obj, "manOfTheMatch")

    def get_mostRunsScorerPercentage(self, obj):
        return self.get_percentage(obj, "mostRunsScorer")

    def get_mostWicketsTakerPercentage(self, obj):
        return self.get_percentage(obj, "mostWicketsTaker")

    def get_percentage(self, obj, field):
        match = self.context.get("match")
        if not match:
            return 0

        total_submissions = Submission.objects.filter(match=match).count()
        selected_count = Submission.objects.filter(match=match, **{field: obj}).count()

        return round((selected_count / total_submissions) * 100, 2) if total_submissions > 0 else 0

    def to_representation(self, instance):
        """Dynamically include only relevant percentage fields based on category"""
        data = super().to_representation(instance)
        category = self.context.get("category")

        if category == "manOfTheMatch":
            data.pop("mostRunsScorerPercentage", None)
            data.pop("mostWicketsTakerPercentage", None)
        elif category == "mostRunsScorer":
            data.pop("manOfTheMatchPercentage", None)
            data.pop("mostWicketsTakerPercentage", None)
        elif category == "mostWicketsTaker":
            data.pop("manOfTheMatchPercentage", None)
            data.pop("mostRunsScorerPercentage", None)

        return data


class NewTeamSerializer(serializers.ModelSerializer):
    winningTeamPercentage = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['teamID', 'teamName', 'teamShortForm', 'winningTeamPercentage']

    def get_winningTeamPercentage(self, obj):
        match = self.context.get("match")
        return self.get_selection_percentage(match, obj)

    def get_selection_percentage(self, match, team):
        if not match:
            return 0
        total_submissions = Submission.objects.filter(match=match).count()
        selected_count = Submission.objects.filter(match=match, winningTeam=team).count()

        return round((selected_count / total_submissions) * 100, 2) if total_submissions > 0 else 0


class NewMatchDetailSerializer(serializers.ModelSerializer):
    eventID = serializers.PrimaryKeyRelatedField(source='event', read_only=True)
    teams = serializers.SerializerMethodField()
    manOfTheMatchPlayers = serializers.SerializerMethodField()
    mostRunsScorerPlayers = serializers.SerializerMethodField()
    mostWicketsTakerPlayers = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = [
            'matchID', 'eventID', 'teams', 'manOfTheMatchPlayers', 'mostRunsScorerPlayers', 'mostWicketsTakerPlayers',
            'matchDate', 'matchStartTime1st', 'matchStartTime2nd', 'location', 'status'
        ]

    def get_teams(self, obj):
        team_serializer = NewTeamSerializer([obj.team1, obj.team2], many=True, context={'match': obj})
        return team_serializer.data

    def get_manOfTheMatchPlayers(self, obj):
        players = Player.objects.filter(team__in=[obj.team1, obj.team2], playing11status=0)
        return NewPlayerSerializer(players, many=True, context={'match': obj}).data

    def get_mostRunsScorerPlayers(self, obj):
        players = Player.objects.filter(
            team__in=[obj.team1, obj.team2], playing11status=0, playerRole__in=[0, 2]
        )
        return NewPlayerSerializer(players, many=True, context={'match': obj}).data

    def get_mostWicketsTakerPlayers(self, obj):
        players = Player.objects.filter(
            team__in=[obj.team1, obj.team2], playing11status=0, playerRole__in=[1,2]
        )
        return NewPlayerSerializer(players, many=True, context={'match': obj}).data


#ProfilePage and LeaderboardNames dropbox
class UserLeaderboardsSerializer(serializers.ModelSerializer):
    leaderboardID = serializers.IntegerField(source="leaderboard.leaderboardID")
    leaderboardName = serializers.CharField(source="leaderboard.leaderboardName")

    class Meta:
        model = LeaderboardMember
        fields = ["leaderboardID", "leaderboardName"]

#ProfilePage Tournment details
class ProfilePageCricketTournamentSerializer(serializers.ModelSerializer):
    eventStartDate = serializers.DateField(format="%d-%m-%Y")
    eventEndDate = serializers.DateField(format="%d-%m-%Y")
    status = serializers.SerializerMethodField()

    class Meta:
        model = CricketTournament
        fields = ["eventID", "eventName", "eventStartDate", "eventEndDate", "status"]

    def get_status(self, obj):
        return obj.get_status_display()


#ProfilePage Event all submissioins
class UserEventSubmissionsSerializer(serializers.ModelSerializer):
    matchID = serializers.IntegerField(source="match.matchID")
    matchDate = serializers.DateField(source="match.matchDate", format="%d-%m-%Y")

    class Meta:
        model = Submission
        fields = ["submissionID", "matchID", "matchDate", "winningTeam", "mostRunsScorer", "mostWicketsTaker", "manOfTheMatch", "score", "submissionScores"]

#ProfilePage Graph Serializers
class UserMatchScoreSerializer(serializers.ModelSerializer):
    matchDate = serializers.DateField(format="%d-%m-%Y")

    class Meta:
        model = Submission
        fields = ['match_id', 'matchDate', 'score', "submissionScores"]


class UserOverallScoreGraphSerializer(serializers.ModelSerializer):
    matchDate = serializers.DateField(format="%d-%m-%Y")
    
    class Meta:
        model = Submission
        fields = ["match_id", "matchDate", "submissionScores"]

