from django.urls import path
from articles import views

urlpatterns = [
    path('', views.ArticleAPIView.as_view()),
    path('<int:pk>/', views.ArticleDetailAPIView.as_view()),
]