from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path("register/", RegisterView.as_view(), name="register"),
    path("register/step1/", RegisterStep1View.as_view(), name="register_step1"),
    path("register/step2/", RegisterStep2View.as_view(), name="register_step2"),


    path('fixture-page-tournaments/', FixturePageCricketTournamentView.as_view(), name='fixture-page-cricket-tournament-list'),
    path('fixture-page-matches-by-tournament/<int:eventID>/', FixturePageMatchesByTournamentView.as_view(), name='matches-by-tournament-url'),


    path('predict-page-match-details/<int:matchID>/', MatchDetailView.as_view(), name='match-details'),
    path('predict-page-new-match-details/<int:matchID>/', NewMatchDetailView.as_view(), name='match-details'),

    path('user-score/<str:username>/<int:eventID>/<int:leaderboardID>/', UserScoreGraphView.as_view(), name='user-score-graph'),
    path("user/<str:username>/leaderboards/", UserLeaderboardsView.as_view(), name="user-leaderboards"),
    path("user/<str:username>/event/<int:eventID>/submissions/", UserEventSubmissionsView.as_view(), name="user-event-submissions"),
    path("profile-page-tournaments/", ProfilePageTournamentListView.as_view(), name="profile-page-tournament-list"),

    path("user/<str:username>/event/<int:eventID>/graph/", UserOverallScoreGraphView.as_view(), name="user-overall-score-graph"),
    path("event/<int:eventID>/kpis/", EventKPIsView.as_view(), name="event-kpis"),


    path("common-leaderboard/rankings/<int:eventID>/", CommonLeaderboardRankingsView.as_view(), name="leaderboard-rankings"),
    path("leaderboard/<int:leaderboardID>/user/<str:username>/", LeaderboardUserRankView.as_view(), name="leaderboard-user-rank"),



]
