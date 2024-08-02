from django.urls import path

from .views import (
    MemberDetailView,
    MemberListView,
    TeamDetailView,
    TeamListView,
)

app_name = "teams_app"

urlpatterns = [
    path("members/", MemberListView.as_view(), name="members"),
    path("members/<int:pk>/", MemberDetailView.as_view(), name="member"),
    path("teams/", TeamListView.as_view(), name="teams"),
    path("teams/<int:pk>/", TeamDetailView.as_view(), name="team"),
]
