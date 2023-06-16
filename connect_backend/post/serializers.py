from .models import Post, Comment

from account.serializers import UserSerializer

from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'body','likes_count' ,'created_by', 'created_at_formatted',]


class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
 
    class Meta:
        model = Comment
        fields = ['id', 'body', 'created_by', 'created_at_formatted',]


class PostDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = ['id', 'body', 'likes_count', 'created_by', 'created_at_formatted', 'comments']
























