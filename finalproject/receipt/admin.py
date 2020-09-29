from django.contrib import admin
from .models import User_Ex, Post, Comment

# Register your models here.
admin.site.register(User_Ex)
admin.site.register(Post)
admin.site.register(Comment)