from rest_framework import generics, status
from rest_framework.views import APIView

from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.db.models import Q
from django_countries import countries
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from django.shortcuts import reverse

UserModel = get_user_model()

from .serializers import RegisterUserSerializer, LoginAPISerializer
from .permissions import AnonPermission

from google.oauth2 import id_token
from google.auth.transport import requests

from rest_framework_simplejwt.tokens import RefreshToken, Token
from rest_framework_simplejwt.views import TokenRefreshView

import jwt
from datetime import timedelta, datetime
refresh_expiration_delta = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
import time

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        "expires": time.time() + refresh_expiration_delta.total_seconds(),
        "email": user.email,
        "image": user.image.name,
        "username": user.username,
        "validated": user.is_validated,
    }


class LoginUserAPIView(generics.GenericAPIView):
    serializer = LoginAPISerializer
    permission_classes = [AnonPermission]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer(data=request.data)
        print(request)
        serializer.is_valid(raise_exception=True)
        email = request.data.get("email", None)
        user = UserModel.objects.filter(
            Q(username__iexact=email) | Q(email__iexact=email)
        ).distinct()
        if not user.exists():
            return Response({"account not found"}, status=status.HTTP_404_NOT_FOUND)
        response = get_tokens_for_user(user.first())
        return Response(response, status=status.HTTP_200_OK)


def send_user_confirmation_email(email):
    user = UserModel.objects.filter(email=email)
    if not user.exists():
        return Response({'detail': 'cannot find user'})
    user = user.first()
    access_token = get_tokens_for_user(user).get("access")

    domain = settings.SITE_URL
    url = reverse('auth:validate')
    redirect_address = domain + url + f'?token={access_token}'

    subject = 'Please Confirm Your DullDiary Registration ... Thanks!'
    message = f'''
        You just signed up for a Dull Diary Account - Click on this link to confirm cheeaz
        {redirect_address}
    '''
    send_mail(
        subject, 
        message, 
        from_email=settings.EMAIL_HOST_USER, 
        recipient_list=[email])


class RegisterUserAPIView(generics.GenericAPIView):

    permission_classes = [AnonPermission]
    serializer = RegisterUserSerializer
    queryset = UserModel.objects.all()

    def get_serializer_context(self):
        return {'request': self.request, 'get_tokens':  get_tokens_for_user }
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user_email = user_data.get("email")
        user = UserModel.objects.filter(email=user_email)
        if not user.exists():
            return Response({'detail': 'cannot find user'})
        user = user.first()
        tokens = get_tokens_for_user(user)
        access_token = tokens.get("access")
        refresh_token = tokens.get("refresh")

        domain = settings.SITE_URL
        url = reverse('auth:validate')
        redirect_address = domain + url + f'?token={access_token}'

        subject = 'Please Confirm Your DullDiary Registration ... Thanks!'
        message = f'''
            You just signed up for a Dull Diary Account - Click on this link to confirm cheeaz
            {redirect_address}
        '''
        send_mail(
            subject, 
            message, 
            from_email=settings.EMAIL_HOST_USER, 
            recipient_list=[user_email])
        return Response({
            'detail': 'You have signed up. Please confirm your account with the link sent to your email to continue',
            'email': user_email,
            "refresh": refresh_token
            },
            status=status.HTTP_201_CREATED)


class ValidateUserFromResentEmail(generics.GenericAPIView):
    permission_classes = []
    serializer_class = []

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", None)
        send_user_confirmation_email(email)
        return Response({'detail': 'Email Resent'})
        


class ValidateUserFromEmail(generics.GenericAPIView):
    permission_classes = []
    serializer_class = []

    def get(self, request, *args, **kwargs):
        token = self.request.query_params.get('token')
        try:
            user_info = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            id = user_info.get('user_id')
            user = UserModel.objects.get(id=id)
            user.is_validated = True
            user.save()
        except jwt.exceptions.ExpiredSignatureError:
            return Response('token has expired -- please request a new email')
        except jwt.exceptions.InvalidTokenError:
            return Response('token is invalid')
        except jwt.exceptions.DecodeError:
            return Response('Improperly formed token')
        return Response(get_tokens_for_user(user), status=status.HTTP_200_OK)
    


class CustomTokenRefreshView(generics.GenericAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = []

    def post(self, request, *args, **kwargs):
        token = self.request.data.get('refresh')
        try:
            user_info = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            id = user_info.get('user_id')
            user = UserModel.objects.get(id=id)
            return Response(get_tokens_for_user(user), status=status.HTTP_200_OK)
        except :
            return Response('invalid token')



class GoogleAuthAPIView(APIView):

    permission_classes = [AnonPermission]
    serializer_class = RegisterUserSerializer
    queryset = UserModel.objects.all()
    CLIENT_ID = '106189049607-3rhlmgu5rmvsnr8kf7fnh3vvs8hts08l.apps.googleusercontent.com'

    def post(self, request, *args, **kwargs):
        profile_obj = request.data.get('profileObj')
        email = profile_obj.get('email')
        username = profile_obj.get('name')
        token_obj = request.data.get('tokenObj')
        token = token_obj.get('id_token')
        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), self.CLIENT_ID)
            userid = idinfo['sub']
        except ValueError:
               return Response({"error": "invalid google token"}, status=status.HTTP_401_UNAUTHORIZED)

        user = UserModel.objects.filter(
            Q(username__iexact=username) | Q(email__iexact=email)
        )
        if not user.exists():
            user = UserModel(username=username, email=email, is_validated=True)
            user.save()
        else:
            user = user.first()
        response = get_tokens_for_user(user)
        return Response(response, status=200)



    def get_serializer_context(self):
        return {'request': self.request}



class CountryListView(APIView):

    def get(self, request, format=None):
        print('yo', countries)
        return Response(countries)