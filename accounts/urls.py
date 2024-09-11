from django.urls import path
from accounts import views


urlpatterns = [
    path("<int:account_id>/", views.UserProfileView.as_view(), name = "profile"),
]