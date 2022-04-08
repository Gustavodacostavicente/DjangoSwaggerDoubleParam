from rest_framework import serializers

from .models import Material, Plant, Vote

from django.contrib.auth.models import User


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'


class PlantSerializer(serializers.ModelSerializer):
    votes = VoteSerializer(many=True, required=False)

    class Meta:
        model = Plant
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    choices = PlantSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Material
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user