from django.urls import path
from articles import views

urlpatterns = [
    path('', views.ArticleAPIView.as_view()),
    path('<int:article_pk>/', views.ArticleDetailAPIView.as_view()),
    path('<int:article_pk>/comments/', views.CommentListView.as_view()),
    path('comments/<int:comment_pk>/', views.CommentDetailView.as_view()),
]