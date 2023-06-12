from django.shortcuts import render

# Create your views here.
from django.middleware.csrf import get_token
from django.http import JsonResponse

def csrf_token_view(request):
    # Generate CSRF token
    csrf_token = get_token(request)

    # Return the CSRF token in the response
    return JsonResponse({'csrfToken': csrf_token})
