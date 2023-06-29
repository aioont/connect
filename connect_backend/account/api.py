from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .forms import SignupForm, ProfileEditForm

from .models import User, FriendshipRequest

from .serializers import UserSerializer, FriendshipRequestSerializer





@api_view(['POST'])
def editprofile(request):
    user = request.user
    email = request.data.get('email')

    if User.objects.exclude(id=user.id).filter(email=email).exists():
        return JsonResponse({'message': 'Email already exists'})
    else:
        form = ProfileEditForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
        
        serializer = UserSerializer(user)

        return JsonResponse({'message': 'Information updated', 'user': serializer.data})





@api_view(['POST'])
def handle_request(request, pk, status):
    user = User.objects.get(pk=pk)
    friendship_request = FriendshipRequest.objects.filter(connect_with=request.user).get(created_by=user)
    friendship_request.status = status
    friendship_request.save() 

    user.friends.add(request.user)
    user.friends_count = user.friends_count + 1
    user.save()

    request_user = request.user
    request_user.friends_count = request_user.friends_count + 1
    request_user.save()

    return JsonResponse({'message': 'Friend Reqeust Updated'})



@api_view(['GET'])
def friends(request, pk):
    user = User.objects.get(pk=pk)
    requests = []

    if user == request.user:
        requests = FriendshipRequest.objects.filter(connect_with=request.user, status=FriendshipRequest.SEND)
        print("Requests contains Friendship Request data: ", request)
        requests = FriendshipRequestSerializer(requests, many=True)
        print("Request contain Serializer data : ", request)
        requests = requests.data
        print("Final data in req : ", request)

    friends = user.friends.all()

    print("My freindzzzzz : ", friends)

    return JsonResponse({
        'user': UserSerializer(user).data,
        'friends': UserSerializer(friends, many=True).data,
        'requests': requests
    }, safe=False)

        


@api_view(['POST'])
def send_friendship_request(request, pk):
    user = User.objects.get(pk=pk)


    all_friends1 = FriendshipRequest.objects.filter(connect_with=request.user).filter(created_by=user)
    all_friends2 = FriendshipRequest.objects.filter(connect_with=user).filter(created_by=request.user)
    
    if not all_friends1 or not all_friends2:
        FriendshipRequest.objects.create(connect_with=user, created_by=request.user)
        return JsonResponse({'message': 'Friend Reqeust Send'})
    else:
        return JsonResponse({'message': 'Friend Reqeust Already Send'})
    
    


@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email
    })



@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'

    form = SignupForm({
        'name': data.get('name'),
        'email': data.get('email'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })

    if form.is_valid():
        user = form.save()
    else:
        message = 'Error occured due to form invalid'

    print(message)

    return JsonResponse({'status': message}, safe=False)




























