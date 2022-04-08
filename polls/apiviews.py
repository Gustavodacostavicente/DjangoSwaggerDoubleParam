from rest_framework import generics, serializers
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Material, Plant, User
from .serializers import MaterialSerializer, PlantSerializer, VoteSerializer, UserSerializer



class MaterialList(generics.ListCreateAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class MaterialDetail(generics.RetrieveDestroyAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class PlantList(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = Plant.objects.filter(poll_id=self.kwargs["pk"])
        return queryset
    serializer_class = PlantSerializer


class CreateVote(APIView):

    def get(self, request, pk, choice_pk):
        voted_by = request.data.get("voted_by")
        data = {'choice': choice_pk, 'poll': pk, 'voted_by': voted_by}
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

from rest_framework.authtoken.models import Token


class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer

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
        Token.objects.create(user=user)
        return user