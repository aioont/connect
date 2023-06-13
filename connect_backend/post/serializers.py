from .models import Post

from account.serializers import UserSerializer

from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'body' , 'created_by', 'created_at_formatted',]




























