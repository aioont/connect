from django.conf import settings
from .forms import SignupForm

from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from rest_framework.response import Response




# @api_view(['GET'])
# def me(request):
#     return JsonResponse({
#         'id': request.user.id,
#         'name': request.user.name,
#         'email': request.user.email
#     })


 


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def me(request):
    data = {
        'id': request.user.id,
        'username': request.user.name,
        'email': request.user.email,
    }
    return Response(data)

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

    return JsonResponse({'status': message})




























