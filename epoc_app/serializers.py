from rest_framework import serializers
from .models import Patient, P_info, P_command

class Patient_serializer(serializers.ModelSerializer): #POST (ESP32)

    class Meta:
        model = P_info
        fields=["name", "spo2"]

class Patient_serializer2(serializers.ModelSerializer):
    class Meta:
        model = P_info
        fields=["name", "spo2", "date"]

class P_serializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields=["name", "spo2", "command", "date"]