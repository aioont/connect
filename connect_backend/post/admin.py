from django.contrib import admin

# Register your models here.

from .models import Post, PostAttachment, Like, Comment

admin.site.register(Post)
admin.site.register(PostAttachment)
admin.site.register(Like)
admin.site.register(Comment)