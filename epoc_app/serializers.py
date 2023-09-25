from rest_framework import serializers
from .models import Patient, P_info, P_command

class Patient_serializer(serializers.ModelSerializer): #POST (ESP32)

    class Meta:
        model = P_info
        fields=["name", "spo2", "flow_real"]

class Patient_serializer2(serializers.ModelSerializer): #Visualizar en http
    class Meta:
        model = P_info
        fields=["name", "spo2", "date"]

class P_serializer(serializers.ModelSerializer): #Comandar a ESP32
    class Meta:
        model = Patient
        fields=["name", "spo2", "command", "date"]