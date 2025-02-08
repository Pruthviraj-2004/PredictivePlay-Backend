from django.db import models
from .fields import EncryptedEmailField
from django.contrib.auth.models import User

from django.contrib.postgres.fields import JSONField

class UserInfo(models.Model):
    userID = models.AutoField(primary_key=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=24)
    email = EncryptedEmailField(max_length=255, unique=True)

    score1 = models.IntegerField(default=0)
    score2 = models.IntegerField(default=0)
    userScores = models.JSONField(default=dict)

    is_in_global_leaderboard = models.BooleanField(default=True)
    is_in_weekly_leaderboard = models.BooleanField(default=True)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
    


class CricketTournament(models.Model):
    STATUS_CHOICES = [
        (0, "Upcoming"),
        (1, "Ongoing"),
        (2, "Completed"),
    ]

    eventID = models.AutoField(primary_key=True)
    eventName = models.CharField(max_length=32)

    eventStartDate = models.DateField()
    eventEndDate = models.DateField()

    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.eventName
    


class Team(models.Model):
    teamID = models.AutoField(primary_key=True)

    teamName = models.CharField(max_length=32)
    teamShortForm = models.CharField(max_length=8, null=True)

    event = models.ForeignKey(CricketTournament, on_delete=models.CASCADE)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.teamName
    


class Player(models.Model):
    PLAYER_ROLES = [
        (0, "Batsman"),
        (1, "Bowler"),
        (2, "AllRounder"),
    ]

    PLAYER_PLAYING_STATUS = [
        (0, "Always"),
        (1, "In Squad"),
        (2, "Substitute"),
    ]

    playerID = models.IntegerField(primary_key=True)
    playerName = models.CharField(max_length=64)

    playerRole = models.IntegerField(choices=PLAYER_ROLES)
    playing11status = models.IntegerField(choices=PLAYER_PLAYING_STATUS)

    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    event = models.ForeignKey(CricketTournament, on_delete=models.CASCADE, null=True)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.playerName} ({self.team.teamName})"
    


class Match(models.Model):
    STATUS_CHOICES = [
        (0, "Upcoming"),
        (1, "Ongoing"),
        (2, "Completed"),
    ]

    matchID = models.IntegerField(primary_key=True)

    event = models.ForeignKey(CricketTournament, on_delete=models.CASCADE)

    team1 = models.ForeignKey(Team, related_name='team1', on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name='team2', on_delete=models.CASCADE)

    matchDate = models.DateField(null=True, default='2025-02-19')
    matchStartTime1st = models.TimeField(null=True, default='19:30:00')
    matchStartTime2nd = models.TimeField(null=True, default='21:00:00')

    location = models.CharField(max_length=64, default='M. Chinnaswamy Stadium')
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.team1.teamName} vs {self.team2.teamName} - {self.event.eventName}"



class WinnerMatchDetails(models.Model):
    winnerMatchID = models.AutoField(primary_key=True)
    match = models.OneToOneField(Match, on_delete=models.CASCADE)
    
    winner_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='winning_matches', blank=True, null=True)
    playerofmatch = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_of_match', blank=True, null=True)
    mostrunsplayer = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='most_runs_player', blank=True, null=True)
    mostwickettaker = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='most_wickets_taker', blank=True, null=True)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Winner: {self.winner_team.teamName if self.winner_team else 'TBD'} - Match {self.match.matchID}"



class Submission(models.Model):
    submissionID = models.AutoField(primary_key=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)

    winningTeam = models.ForeignKey(Team, on_delete=models.CASCADE)
    mostRunsScorer = models.ForeignKey(Player, related_name='most_runs', on_delete=models.CASCADE)
    mostWicketsTaker = models.ForeignKey(Player, related_name='most_wickets', on_delete=models.CASCADE)
    manOfTheMatch = models.ForeignKey(Player, related_name='man_of_match', on_delete=models.CASCADE)
    
    score = models.IntegerField(default=0)
    submissionScores = models.JSONField(default=dict)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.match}"
    


class Leaderboard(models.Model):
    leaderboardID = models.AutoField(primary_key=True)

    leaderboardName = models.CharField(max_length=32)
    leaderboardPassword = models.CharField(max_length=16)

    event = models.ForeignKey(CricketTournament, on_delete=models.CASCADE, default=1)

    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="custom_leaderboard_creator")
    emailEndsWith = models.CharField(max_length=64, blank=True, null=True)

    winningTeamPoints = models.IntegerField(default=0)
    manOfTheMatchPoints = models.IntegerField(default=0)
    mostRunsScorerPoints = models.IntegerField(default=0)
    mostWicketsTakerPoints = models.IntegerField(default=0)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.leaderboardName} - {self.event.eventName}"



class LeaderboardMember(models.Model):
    leaderboardMemberID = models.AutoField(primary_key=True)

    leaderboard = models.ForeignKey(Leaderboard, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    points = models.IntegerField(default=0)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.leaderboard.leaderboardName}"
