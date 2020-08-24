from rest_framework import serializers
from .models import Drug, Vaccination
from django.contrib.auth.models import User

class DrugSerializer(serializers.ModelSerializer):
    class Meta:
      model = Drug
      fields = ('id', 'name', 'code', 'description')


class VaccinationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Vaccination
    fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user