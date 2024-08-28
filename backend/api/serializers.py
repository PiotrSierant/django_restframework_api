from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)

        # Generowanie tokena
        token = Token.objects.create(user=user)

        return user



class NipSerializer(serializers.Serializer):
    nip = serializers.CharField(max_length=10)

    def validate_nip(self, value):
        if len(value) != 10 or not value.isdigit():
            raise serializers.ValidationError("Numer NIP musi mieć 10 cyfr.")
        return value