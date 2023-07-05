from django.shortcuts import render
from rest_framework import status

from user_app.api.serializers import RegisterSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
# from user_app import models
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import auth

from rest_framework.permissions import IsAuthenticated

from user_app.models import Account


def create_account(account):
    data = {}

    data['username'] = account.username
    data['email'] = account.email
    data['first_name'] = account.first_name
    data['last_name'] = account.last_name
    data['phone'] = account.phone

    return data


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def sessionView(request):

    if request.method == 'GET':
        user = request.user
        print(user)
        account = Account.objects.get(email=user)

        data = {}
        if account is not None:
            data = create_account(account)
            data['response'] = 'You are authenticated'

            return Response(data)

        else:
            data['error'] = 'User not found'
            return Response(data, status=status.HTTP_404_NOT_FOUND)


# Create your views here.
@api_view(['POST', ])
def logoutView(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST', ])
def loginView(request):
    data = {}
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

    account = auth.authenticate(email=email, password=password)

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
def registerView(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            account = serializer.save()
            data = create_account(account)
            data['response'] = 'Register is successfully'

            return Response(data)
        else:
            data = serializer.errors
            return Response(data)
