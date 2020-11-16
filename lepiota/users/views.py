from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.http import HttpResponse
from oauth2_provider.contrib.rest_framework import (TokenHasReadWriteScope,
                                                    TokenHasScope)
from oauth2_provider.views.generic import ProtectedResourceView
from rest_framework import generics, permissions

from .serializers import UserSerializer, GroupSerializer


user = get_user_model()

class UserDetails(generics.RetrieveAPIView):
    
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = user.objects.all()
    serializer_class = UserSerializer


class GroupList(generics.ListAPIView):
    
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
