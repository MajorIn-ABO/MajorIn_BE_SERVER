from django.contrib import admin

# Register your models here.

from .models import User, Post, Major, Category, Post_Comment, Post_Like, Post_bookmark

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Major)
admin.site.register(Category)
admin.site.register(Post_Comment)
admin.site.register(Post_Like)
admin.site.register(Post_bookmark)