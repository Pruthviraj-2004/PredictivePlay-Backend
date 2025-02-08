from django.contrib import admin
from .models import *

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('userID', 'username', 'name', 'email', 'createdAt', 'updatedAt')
    search_fields = ('username', 'name', 'email')


@admin.register(CricketTournament)
class CricketTournamentAdmin(admin.ModelAdmin):
    list_display = ("eventID", "eventName", "eventStartDate", "eventEndDate", "status", "createdAt")
    list_filter = ("status", "eventStartDate", "eventEndDate")
    search_fields = ("eventName",)
    ordering = ("-eventStartDate",)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("teamID", "teamName", "teamShortForm", "event")
    list_filter = ("event",)
    search_fields = ("teamName", "event__eventName")
    ordering = ("event__eventName",)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("playerID", "playerName", "playerRole", "playing11status", "team", "event")
    list_filter = ("playerRole", "playing11status", "team", "event")
    search_fields = ("playerName", "team__teamName", "event__eventName")
    ordering = ("playerID",)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("matchID", "event", "team1", "team2", "matchDate", "matchStartTime1st", "matchStartTime2nd")
    list_filter = ("event", "team1", "team2", "matchDate")
    search_fields = ("team1__teamName", "team2__teamName", "event__eventName")
    ordering = ("-matchDate",)


@admin.register(WinnerMatchDetails)
class WinnerMatchDetailsAdmin(admin.ModelAdmin):
    list_display = ("winnerMatchID", "match", "winner_team", "playerofmatch", "mostrunsplayer", "mostwickettaker", "createdAt", "updatedAt")
    list_filter = ("winner_team", "match__event")
    search_fields = ("match__team1__teamName", "match__team2__teamName", "winner_team__teamName")
    ordering = ("-createdAt",)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("submissionID", "user", "match", "winningTeam", "mostRunsScorer", "mostWicketsTaker", "manOfTheMatch", "submissionScores", "createdAt", "updatedAt")
    list_filter = ("match","match__event", "winningTeam",  "user")
    search_fields = ("user__username", "match__team1__teamName", "match__team2__teamName", "winningTeam__teamName")
    ordering = ("-submissionID",)


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ("leaderboardID", "leaderboardName", "event", "createdBy", "emailEndsWith", "winningTeamPoints", "manOfTheMatchPoints", "mostRunsScorerPoints", "mostWicketsTakerPoints", "createdAt", "updatedAt")
    list_filter = ("event", "createdBy", "emailEndsWith")
    search_fields = ("leaderboardName", "createdBy__username")
    ordering = ("leaderboardID",)


@admin.register(LeaderboardMember)
class LeaderboardMemberAdmin(admin.ModelAdmin):
    list_display = ("leaderboardMemberID", "leaderboard", "user", "points", "createdAt", "updatedAt")
    list_filter = ( "leaderboard__event", "leaderboard", "user")
    search_fields = ("user__username", "leaderboard__leaderboardName")
    ordering = ("-points",)
  
