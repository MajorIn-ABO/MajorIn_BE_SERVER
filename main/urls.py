from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('user/', views.user_view, name='user'),
    path('api/users/', views.UserList.as_view(), name='user-list'),
    path('api/users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('api/users/', views.UserCreate.as_view(), name='user-create'),
    path('api/users/<int:pk>/', views.UserUpdate.as_view(), name='user-update'),
    path('api/posts/', views.PostList.as_view(), name='post-list'),
]
