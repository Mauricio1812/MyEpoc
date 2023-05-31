from rest_framework import serializers
from .models import T_Vs_t, P_info, P_command

class Patient_serializer(serializers.ModelSerializer): #POST (ESP32)

    class Meta:
        model = P_info
        fields=["name", "humidity", "temperature"]

class Patient_serializer2(serializers.ModelSerializer):
    class Meta:
        model = P_info
        fields=["name", "humidity", "temperature", "date"]

# class Command_serializer2(serializers.ModelSerializer):
#     class Meta:
#         model = P_command
#         fields=["name", "oxygenflow", 'date']

class Temp_serializer(serializers.ModelSerializer):# GET

    class Meta:
        model = T_Vs_t
        fields =["TEMPERATURA"]

class Temp_serializer2(serializers.ModelSerializer):# GET

    class Meta:
        model = T_Vs_t
        fields =["TEMPERATURA", "FECHA"]