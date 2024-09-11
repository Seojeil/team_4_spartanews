from django.urls import path
from accounts import views


urlpatterns = [
    path('',views.SignupView.as_view()),
]