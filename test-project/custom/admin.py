from django.contrib import admin
from . models import *
# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display    = [field.name for field in Profile._meta.fields]
    search_fields   = ['user']



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display    = [field.name for field in Post._meta.fields if field.name != 'content' ]
    search_fields   = ['title']



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display    = [field.name for field in Comment._meta.fields]
    search_fields   = ['content']