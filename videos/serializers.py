from rest_framework import serializers
from .models import VideoRequest, Influencer, Payment
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class InfluencerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Influencer
        fields = ["name", "email", "phone", "bio", "user"]
        read_only_fields = ("user",)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        influencer = Influencer.objects.create(user=user, **validated_data)
        return influencer


class VideoRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoRequest
        fields = "__all__"
        read_only_fields = ("user",)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
