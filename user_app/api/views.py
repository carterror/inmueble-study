from django.shortcuts import render
from rest_framework import status

from user_app.api.serializers import RegisterSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
# from user_app import models
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
<<<<<<< HEAD
from django.contrib import auth

from rest_framework.permissions import IsAuthenticated

# from user_app.models import Account
# from django.core.cache import cache


def create_account(account):
    data = {}

    data['username'] = account.username
    data['email'] = account.email

    return data
=======
>>>>>>> parent of 25b4be5 (primer deploy dajngo)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def sessionView(request):

    if request.method == 'GET':
        user = request.user
        print(user)
        # account = User.objects.get(email=user)

        data = {}
        if account is not None:
            data = create_account(account)
            data['response'] = 'You are authenticated'

            return Response(data)

        else:
            data['error'] = 'User not found'
            return Response(data, status=status.HTTP_404_NOT_FOUND)


# Create your views here.
@api_view(['POST',])
def logoutView(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


<<<<<<< HEAD
@api_view(['POST', ])
def loginView(request):
    # cache.delete('mi_cache')
    data = {}
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

    account = auth.authenticate(username=username, password=password)

    if account is not None:
        data = create_account(account)
        data['response'] = 'Login is successfully'

        refresh = RefreshToken.for_user(account)
        data['token'] = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

        return Response(data)

    else:
        data['error'] = 'Login is failed'
        data['error_message'] = [
            'Email or password is incorrect'
        ]
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST', ])
=======
@api_view(['POST',])
>>>>>>> parent of 25b4be5 (primer deploy dajngo)
def registerView(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'Register is successfully'
            data['username'] = account.username
            data['email'] = account.email
            # token = Token.objects.get(user=account).key
            # data['token'] = token
            refresh = RefreshToken.for_user(account)
            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            return Response(data)
        else:
            data = serializer.errors
