
from django.shortcuts import JsonResponse

from .serializers import PostSerializer
from .models import Post

from rest_framework.decorators import api_view

@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all()

    serializer = PostSerializer(posts, many=True)

    return JsonResponse({'data': serializer.data})



