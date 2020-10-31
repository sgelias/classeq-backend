from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers


user = get_user_model()


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ("name", )


class UserSerializer(serializers.ModelSerializer):
    
    groups = GroupSerializer()
    
    class Meta:
        model = user
        fields = ('username', 'email', "first_name", "last_name", "groups")
