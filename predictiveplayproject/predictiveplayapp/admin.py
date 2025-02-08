from django.contrib import admin
from .models import *

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('userID', 'username', 'name', 'email', 'createdAt', 'updatedAt')
    search_fields = ('username', 'name', 'email')
    readonly_fields = ('createdAt', 'updatedAt')


@admin.register(CricketTournament)
class CricketTournamentAdmin(admin.ModelAdmin):
    list_display = ("eventID", "eventName", "eventStartDate", "eventEndDate", "status", "createdAt", "updatedAt")
    list_filter = ("status", "eventStartDate", "eventEndDate")
    search_fields = ("eventName",)
    ordering = ("-eventStartDate",)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("teamID", "teamName", "teamShortForm", "event", "createdAt", "updatedAt")
    list_filter = ("event",)
    search_fields = ("teamName", "event__eventName")
    ordering = ("teamShortForm",)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("playerID", "playerName", "playerRole", "playing11status", "team", "event", "createdAt", "updatedAt")
    list_filter = ("playerRole", "playing11status", "team", "event")
    search_fields = ("playerName", "team__teamName", "event__eventName")
    ordering = ("playerID",)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("matchID", "event", "team1", "team2", "matchDate", "matchStartTime1st", "matchStartTime2nd", "createdAt", "updatedAt")
    list_filter = ("event", "matchDate")
    search_fields = ("team1__teamName", "team2__teamName", "event__eventName")
    ordering = ("-matchDate",)


@admin.register(WinnerMatchDetails)
class WinnerMatchDetailsAdmin(admin.ModelAdmin):
    list_display = ("winnerMatchID", "match", "winner_team", "playerofmatch", "mostrunsplayer", "mostwickettaker", "createdAt", "updatedAt")
    list_filter = ("winner_team",)
    search_fields = ("match__team1__teamName", "match__team2__teamName", "winner_team__teamName")
    ordering = ("-createdAt",)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("submissionID", "user", "match", "winningTeam", "mostRunsScorer", "mostWicketsTaker", "manOfTheMatch", "submissionScores", "createdAt", "updatedAt")
    list_filter = ("user", "match", "winningTeam")
    search_fields = ("user__username", "match__team1__teamName", "match__team2__teamName", "winningTeam__teamName")
    ordering = ("-createdAt",)


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ("leaderboardID", "leaderboardName", "createdBy", "emailEndsWith", "winningTeamPoints", "manOfTheMatchPoints", "mostRunsScorerPoints", "mostWicketsTakerPoints", "createdAt", "updatedAt")
    search_fields = ("leaderboardName", "createdBy__username")
    ordering = ("-createdAt",)


@admin.register(LeaderboardMember)
class LeaderboardMemberAdmin(admin.ModelAdmin):
    list_display = ("leaderboardMemberID", "leaderboard", "user", "points", "createdAt", "updatedAt")
    list_filter = ("leaderboard",)
    search_fields = ("user__username", "leaderboard__leaderboardName")
    ordering = ("-points", "-createdAt")
  
