"""Serializers for the user API View"""

from django.contrib.auth import (
    get_user_model,
    authenticate,
    )

from django.utils.translation import gettext as _

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        # the fields defined to exist in the json format
        fields = ['email', 'password', 'name']
        # configure the fields defined above                                                       
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
    
    # Only called when the validation is successful
    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        # overwrite the create method to create user using the model we defined
        return get_user_model().objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        """Update and return user"""
        # find the password or default to None
        password = validated_data.pop('password', None)
        # Provided by the model serializer, set everything other than password
        user = super().update(instance, validated_data)

        # set the password using the set_password method
        if password:
            user.set_password(password)
            user.save()
        
        return user

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')
        
        attrs['user'] = user
        return attrs