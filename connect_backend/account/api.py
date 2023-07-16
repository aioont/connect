from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .forms import SignupForm, ProfileEditForm
from .models import User, FriendshipRequest
from .serializers import UserSerializer, FriendshipRequestSerializer
from notification.utils import create_notification
from django.core.mail import send_mail


@api_view(['GET'])
def my_friendship_suggestions(request):
    serializer = UserSerializer(request.user.people_you_may_know.all(), many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def editpassword(request):
    user = request.user
    
    form = PasswordChangeForm(data=request.POST, user=user)
    if form.is_valid():
        form.save()

        return JsonResponse({'message': 'success'})    
    else:
        return JsonResponse({'message': form.errors.as_json()}, safe=False)

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

    if friendship_request.status == 'accepted':
        user.friends.add(request.user)
        user.friends_count = user.friends_count + 1
        user.save()

        request_user = request.user
        request_user.friends_count = request_user.friends_count + 1
        request_user.save()

        notification = create_notification(request, 'accepted_friendrequest', friendrequest_id=friendship_request.id)
    else:
        notification = create_notification(request, 'rejected_friendrequest', friendrequest_id=friendship_request.id)

    

    

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

    if not all_friends1 and not all_friends2:

        friendrequest = FriendshipRequest.objects.create(connect_with=user, created_by=request.user)
        
        notification = create_notification(request, 'new_friendrequest', friendrequest_id=friendrequest.id)
        
        return JsonResponse({'message': 'Friend Reqeust Send'})
    else:
        return JsonResponse({'message': 'Friend Reqeust Already Send'})
    
    


@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
        'avatar': request.user.get_avatar()
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
        user.is_active = False
        user.save()

        url = f'http://127.0.0.1:8000/activateemail/?email={user.email}&id={user.id}'

        send_mail(
            "Connect - Please verify your email",
            f"Verify your account by clicking the url : {url}",
            "noreply@connect.com",
            [user.email],
            fail_silently=False,
        )


    else:
        message = form.errors.as_json()
    
    print(message)

    return JsonResponse({'message': message}, safe=False)
        




























