# Generated by Django 5.1.5 on 2025-02-07 17:56

import django.db.models.deletion
import predictiveplayapp.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CricketTournament',
            fields=[
                ('eventID', models.AutoField(primary_key=True, serialize=False)),
                ('eventName', models.CharField(max_length=32)),
                ('eventStartDate', models.DateField()),
                ('eventEndDate', models.DateField()),
                ('status', models.IntegerField(choices=[(0, 'Upcoming'), (1, 'Ongoing'), (2, 'Completed')], default=0)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Leaderboard',
            fields=[
                ('leaderboardID', models.AutoField(primary_key=True, serialize=False)),
                ('leaderboardName', models.CharField(max_length=32, unique=True)),
                ('leaderboardPassword', models.CharField(max_length=16)),
                ('emailEndsWith', models.CharField(blank=True, max_length=64, null=True)),
                ('winningTeamPoints', models.IntegerField(default=0)),
                ('manOfTheMatchPoints', models.IntegerField(default=0)),
                ('mostRunsScorerPoints', models.IntegerField(default=0)),
                ('mostWicketsTakerPoints', models.IntegerField(default=0)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('createdBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom_leaderboard_creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LeaderboardMember',
            fields=[
                ('leaderboardMemberID', models.AutoField(primary_key=True, serialize=False)),
                ('points', models.IntegerField(default=0)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('leaderboard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='predictiveplayapp.leaderboard')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('matchID', models.IntegerField(primary_key=True, serialize=False)),
                ('matchDate', models.DateField(default='2025-02-19', null=True)),
                ('matchStartTime1st', models.TimeField(default='19:30:00', null=True)),
                ('matchStartTime2nd', models.TimeField(default='21:00:00', null=True)),
                ('location', models.CharField(default='M. Chinnaswamy Stadium', max_length=64)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='predictiveplayapp.crickettournament')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('playerID', models.IntegerField(primary_key=True, serialize=False)),
                ('playerName', models.CharField(max_length=64)),
                ('playerRole', models.IntegerField(choices=[(0, 'Batsman'), (1, 'Bowler'), (2, 'Wicketkeeper')])),
                ('playing11status', models.IntegerField(choices=[(0, 'Always'), (1, 'In Squad'), (2, 'Substitute')])),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='predictiveplayapp.crickettournament')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('teamID', models.AutoField(primary_key=True, serialize=False)),
                ('teamName', models.CharField(max_length=32)),
                ('teamShortForm', models.CharField(max_length=8, null=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='predictiveplayapp.crickettournament')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('submissionID', models.AutoField(primary_key=True, serialize=False)),
                ('score', models.IntegerField(default=0)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('manOfTheMatch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='man_of_match', to='predictiveplayapp.player')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='predictiveplayapp.match')),
                ('mostRunsScorer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='most_runs', to='predictiveplayapp.player')),
                ('mostWicketsTaker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='most_wickets', to='predictiveplayapp.player')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('winningTeam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='predictiveplayapp.team')),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='predictiveplayapp.team'),
        ),
        migrations.AddField(
            model_name='match',
            name='team1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team1', to='predictiveplayapp.team'),
        ),
        migrations.AddField(
            model_name='match',
            name='team2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team2', to='predictiveplayapp.team'),
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('userID', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=24, unique=True)),
                ('name', models.CharField(max_length=24)),
                ('email', predictiveplayapp.fields.EncryptedEmailField(unique=True)),
                ('score1', models.IntegerField(default=0)),
                ('score2', models.IntegerField(default=0)),
                ('is_in_global_leaderboard', models.BooleanField(default=True)),
                ('is_in_weekly_leaderboard', models.BooleanField(default=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WinnerMatchDetails',
            fields=[
                ('winnerMatchID', models.AutoField(primary_key=True, serialize=False)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('match', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='predictiveplayapp.match')),
                ('mostrunsplayer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='most_runs_player', to='predictiveplayapp.player')),
                ('mostwickettaker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='most_wickets_taker', to='predictiveplayapp.player')),
                ('playerofmatch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player_of_match', to='predictiveplayapp.player')),
                ('winner_team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winning_matches', to='predictiveplayapp.team')),
            ],
        ),
    ]
