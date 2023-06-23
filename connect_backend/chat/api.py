from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User

from .models import Conversation, ConversationMessage
from .serializers import ConversationSerializer, ConversationDetailSerializer, ConversationMessageSerializer


@api_view(['GET'])
def conversation_list(request):
    conversations = Conversation.objects.filter(users__in=list([request.user]))
    serializer = ConversationSerializer(conversations, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def conversation_detail(request, pk):
    conversation = Conversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    serializer = ConversationDetailSerializer(conversation)

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def conversation_get_or_create(request, user_pk):
    user = User.objects.get(pk=user_pk)

    conversations = Conversation.objects.filter(users__in=list([request.user])).filter(users__in=list([user]))

    if conversations.exists():
        conversation = conversations.first()
    else:
        conversation = Conversation.objects.create()
        conversation.users.add(user, request.user)
        conversation.save()

    serializer = ConversationDetailSerializer(conversation)
    
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def conversation_send_message(request, pk):
    print("=== pk ====", pk)
    conversation1 = Conversation.objects.filter(users__in=[request.user]).get(pk=pk)
    sent_to_message = ConversationMessage.objects.filter(conversation=conversation1).first()
    sent_to_email = sent_to_message.sent_to.email if sent_to_message else None
    
    print('==== Conversation object====== : ', conversation1)
    print('==== Sent_to_email =========== : ', sent_to_email)

    conversation_message = ConversationMessage.objects.create(
        conversation=conversation1,
        body=request.data.get('body'),
        created_by=request.user,
        sent_to=sent_to_message.sent_to if sent_to_message else None
    )
    
    serializer = ConversationMessageSerializer(conversation_message)
    
    if sent_to_email:
        print("Sent to Email ID:", sent_to_email)
    
    return JsonResponse(serializer.data, safe=False)
