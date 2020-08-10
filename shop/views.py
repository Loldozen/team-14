from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.authtoken.models import Token


from shop.models import Clothing, Payment
from shop.serializers import UserSerializer,ClothingSerializer, PaymentSerializer
from shop.permissions import IsOwnerOrReadOnly

# Create your views here.

User = get_user_model()

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'clothings': reverse('clothing-list', request=request, format=format),
        'signup': reverse('signup', request=request, format=format)
    })

class ClothingList(generics.ListCreateAPIView):
    queryset = Clothing.objects.all()
    serializer_class = ClothingSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, 
        IsOwnerOrReadOnly
        ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ClothingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Clothing.objects.all()
    serializer_class = ClothingSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, 
        IsOwnerOrReadOnly
        ]

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SignUpView(APIView):

    def post(self, request,format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentView(generics.CreateAPIView):

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            pay = serializer.save()
            if pay:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def clothing(self, pk):
        return get_object_or_404(Clothing, pk=pk)
    
    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            clothing = self.clothing
        )