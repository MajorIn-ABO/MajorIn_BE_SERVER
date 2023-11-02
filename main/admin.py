from django.contrib import admin

# Register your models here.

from .models import User, Board, Major, Category, Board_Comment, Board_Like, Board_bookmark

admin.site.register(User)
admin.site.register(Board)
admin.site.register(Major)
admin.site.register(Category)
admin.site.register(Board_Comment)
admin.site.register(Board_Like)
admin.site.register(Board_bookmark)