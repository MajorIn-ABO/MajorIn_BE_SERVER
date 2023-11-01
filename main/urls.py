from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user/', views.user_view, name='user'),
    path('api/users/', views.UserList.as_view(), name='user-list'),
    path('api/users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('api/users/', views.UserCreate.as_view(), name='user-create'),
    path('api/users/<int:pk>/', views.UserUpdate.as_view(), name='user-update'),
    path('api/posts/', views.PostList.as_view(), name='post-list'),
    path('api/posts/<int:pk>/', views.PostDetail.as_view(), name='post-detail'),
    path('api/posts/', views.PostCreate.as_view(), name='post-create'),
    path('api/posts/<int:pk>/update/', views.PostUpdate.as_view(), name='post-update'),
    path('api/posts/<int:pk>/delete/', views.PostDelete.as_view(), name='post-delete'),
]
