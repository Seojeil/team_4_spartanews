from django.urls import path
from accounts import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('',views.SignupView.as_view()),
    path("login/", views.UserLoginView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password/', views.UserChangePasswordView.as_view()),
    path("<int:account_id>/", views.UserProfileView.as_view()),
]