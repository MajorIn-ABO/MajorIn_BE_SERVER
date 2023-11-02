from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user/', views.user_view, name='user'),
    path('api/users/', views.UserList.as_view(), name='user-list'),
    path('api/users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('api/users/create/', views.UserCreate.as_view(), name='user-create'),
    path('api/users/<int:pk>/update/', views.UserUpdate.as_view(), name='user-update'),
    path('api/boards/', views.BoardList.as_view(), name='board-list'),
    path('api/boards/<int:pk>/', views.BoardDetail.as_view(), name='board-detail'),
    path('api/boards/<str:category_id>/', views.BoardCategoryList.as_view(), name='board-categorylist'),
    path('api/boards/create/', views.BoardCreate.as_view(), name='board-create'),
    path('api/boards/<int:pk>/update/', views.BoardUpdate.as_view(), name='board-update'),
    path('api/boards/<int:pk>/delete/', views.BoardDelete.as_view(), name='board-delete'),
]
