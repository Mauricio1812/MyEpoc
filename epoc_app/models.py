# -*- coding: utf-8 -*-
from django.db import models
from accounts.models import User
    
class Patient(models.Model):
    name=models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    spo2=models.FloatField()
    flow=models.FloatField()
    date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s: %s - %s' %(self.name, self.spo2, self.flow,)
    
class P_info(models.Model): #receive 'patient' information (SPO2)
    name=models.TextField()
    spo2=models.FloatField()
    flow_real=models.FloatField(default=0)
    date=models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return f"{self.name}: {self.spo2} ({self.date:%H:%M:%S %B %d, %Y})"

class P_command(models.Model): #send commands to epoc device
    name=models.TextField()
    flow=models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return '%s: %s' %(self.name, self.flow,)