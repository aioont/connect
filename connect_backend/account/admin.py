from django.contrib import admin
from .models import User, FriendshipRequest
# Register your models here.


admin.site.register(User)
admin.site.register(FriendshipRequest)