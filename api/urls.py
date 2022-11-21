from django.urls import path
from api import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # authentication
    path('login/', obtain_auth_token, name='api-login'),
    path('register/', views.register_view, name='api-register'),
    path('logout/', views.logout_view, name='logout'),

    # general endpoints
    path('list/', views.PostList.as_view(), name='post-list'),
    path('<int:pk>/', views.PostDetail.as_view(), name='post-detail'),
    path('<int:pk>/comment-create/',
         views.CommentCreate.as_view(), name="comment-create"),
    path('<int:pk>/comments/', views.CommentList.as_view(), name="comment-list"),
    path('comment/<int:pk>/', views.CommentDetails.as_view(), name="comment-details"),
]
