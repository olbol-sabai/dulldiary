from rest_framework import serializers
from rest_framework import exceptions

from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
from django.utils import timezone
from django.db.models import Q

import datetime

UserModel = get_user_model()



class LoginAPISerializer(serializers.ModelSerializer):
    email = serializers.CharField(write_only=True)
    password = serializers.CharField(style={"input-type": 'password'}, write_only=True)

    class Meta:
        model = UserModel
        fields = ["email", "password"]
    
    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = authenticate(username=email, password=password)
        if not user:
            raise exceptions.AuthenticationFailed('Invalid details')
        return data




class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input-type": 'password'}, write_only=True)
    password2 = serializers.CharField(style={"input-type": 'password'}, write_only=True)
    ## read only fields

    class Meta:
        model = UserModel
        fields = ['email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate(self, data):
        pw = data.get('password')
        pw2 = data.pop('password2')
        if pw != pw2:
            raise exceptions.ValidationError('Passwords must match')
        return data
    
    def validate_email(self, data):
        user = UserModel.objects.filter(
            Q(username__iexact=data) | Q(email__iexact=data)
        )
        if user.exists():
            raise serializers.ValidationError("These details are already taken")     
        return data
    
    def create(self, validated_data):
        pw = validated_data.pop('password')
        email = validated_data.pop('email')
        new_user = UserModel(username=email, email=email)
        new_user.set_password(pw)
        new_user.save()
        return new_user
        

    



    
