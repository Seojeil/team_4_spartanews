from django.urls import path
from accounts import views


urlpatterns = [
    path('',views.SignupView.as_view()),
    path("<int:account_id>/", views.UserProfileView.as_view()),
]