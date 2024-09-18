from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Handles validation and creation of User instances from input data.
    """
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ( 'email', 'password', 'first_name', 'last_name')
    def validate_username(self, value):
        """
        Validate that the username does not already exist.
        Args:
            value (str): The username to validate.
        Returns:
            str: The validated username.
        Raises:
            serializers.ValidationError: If the firstname already exists.
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must include at least one number.")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must include at least one uppercase letter.")
        return value
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user






