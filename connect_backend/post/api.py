from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from account.models import User
from account.serializers import UserSerializer

from .models import Post
from .serializers import PostSerializer

from .forms import PostForm


@api_view(['GET'])
def post_list(request):
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)


    posts = Post.objects.filter(created_by__in=list(user_ids))

    serializer = PostSerializer(posts, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def post_list_profile(request, id):
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by=id)

    posts_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)

    return JsonResponse({
        'posts': posts_serializer.data,
        'user': user_serializer.data,
    }, safe=False)


@api_view(['POST'])
def post_create(request):
    data = request.data
    
    form = PostForm(request.data)

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        serializer = PostSerializer(post)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'Error': 'Unable to add your post !'})
