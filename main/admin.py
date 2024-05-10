from django.contrib import admin

# Register your models here.

from .models import Token, Major, User, Board, Category, Board_Comment, Board_Like, Board_bookmark, Study, Study_Comment, Study_Like, Usedbooktrade, UsedbooktradeData, Usedbooktrade_Comment

admin.site.register(Token)
admin.site.register(Major)
admin.site.register(User)
admin.site.register(Board)
admin.site.register(Category)
admin.site.register(Board_Comment)
admin.site.register(Board_Like)
admin.site.register(Board_bookmark)
admin.site.register(Study)
admin.site.register(Study_Comment)
admin.site.register(Study_Like)
admin.site.register(Usedbooktrade)
admin.site.register(UsedbooktradeData)
admin.site.register(Usedbooktrade_Comment)