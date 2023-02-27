from rest_framework import serializers
from django.contrib.auth import get_user_model # If used custom user model

from apps.demologin.models.user import User

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    # password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],

        )

        return user

    class Meta:
        model = UserModel
        # Tuple of serialized model fields (see link [2])
        fields = ("id", "username", "password", "email")



class ChangePasswordSerializer(serializers.Serializer):
    # model = UserModel

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = UserModel
        # Tuple of serialized model fields (see link [2])

