from blog.forms import UserLoginForm
from . import views
from django.contrib.auth import views as user_views
from django.urls import path

urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', user_views.LoginView.as_view(template_name='user/login.html', authentication_form=UserLoginForm , redirect_authenticated_user=True),
         name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.create_blog, name='create-blog'),
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('<slug:slug>/delete/', views.PostDelete.as_view(), name='delete-post'),
    path('<slug:slug>/edit/', views.PostEdit.as_view(), name='edit-post'),
    path('like/<slug:slug>/', views.likeView, name='like-post'),
   
]
