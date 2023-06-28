from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User

from .models import Conversation, ConversationMessage
from .serializers import ConversationSerializer, ConversationDetailSerializer, ConversationMessageSerializer
from account.serializers import UserSerializer

@api_view(['GET'])
def conversation_list(request):
    conversations = Conversation.objects.filter(users__in=list([request.user]))
    serializer = ConversationSerializer(conversations, many=True)

    print("Serializer Friend : ",serializer.data)

    friends = request.user.friends.all()
    friends_serializer = UserSerializer(friends, many=True)
    friends_data = friends_serializer.data

    print("**********\nFriends Data:", friends_data)

    return JsonResponse(serializer.data, safe=False)



@api_view(['GET'])
def conversation_detail(request, pk):
    print("*********** p k ======== ",pk)
    conversation = Conversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    serializer = ConversationDetailSerializer(conversation)

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def conversation_get_or_create(request, user_pk):
    user = User.objects.get(pk=user_pk)
    print('User object of user_pk = ', user)

    conversations = Conversation.objects.filter(users__in=list([request.user])).filter(users__in=list([user]))

    print('Conversations = ', conversations)
    print('Conversations First = ', conversations.first())
    


    if conversations.exists():
        conversation = conversations.first()
        print('Conversations Exist First = ', conversations.first())
    
    else:
        conversation = Conversation.objects.create()
        
        print("USER ====", user)
        print("REQUEST USER ====", request.user)

        conversation.users.add(user, request.user)
        conversation.save()

    serializer = ConversationDetailSerializer(conversation)
    
    print("Serializer data === ", serializer.data)

    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def conversation_send_message(request, pk):
    conversation = Conversation.objects.filter(users__in=[request.user]).get(pk=pk)
    print("=== Conversation1 ===", conversation)
    
    sent_to_message = ConversationMessage.objects.filter(conversation=conversation).first()
    
    print("=== seno_to_message ===", )
    
    sent_to_email = sent_to_message.sent_to if sent_to_message else None
    
    #print('==== Conversation object====== : ', conversation1)
    print('==== Sent_to_email =========== : ', sent_to_email)

    for user in conversation.users.all():
        print("Other User = ", user)
        if user != request.user:
            sent_to = user
            print("Assigned sent_to ===== ",sent_to)
 

    print("Sent to Email ID:", sent_to)    

    conversation_message = ConversationMessage.objects.create(
        conversation=conversation,
        body=request.data.get('body'),
        created_by=request.user,
        sent_to=sent_to
    )
    
    serializer = ConversationMessageSerializer(conversation_message)
    
    if sent_to:
        print("Sent to Email ID:", sent_to)
    
    return JsonResponse(serializer.data, safe=False)
