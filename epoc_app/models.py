# -*- coding: utf-8 -*-
from django.db import models
    
class Patient(models.Model):
    name= models.TextField()
    spo2=models.FloatField()
    flow=models.FloatField()
    date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s: %s - %s' %(self.name, self.spo2, self.flow,)
    
class P_info(models.Model): #receive 'patient' information
    name=models.TextField()
    spo2=models.FloatField()
    date=models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return '%s: %s ' %(self.name, self.spo2, )

class P_command(models.Model): #send commands to epoc device
    name=models.TextField()
    flow=models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return '%s: %s' %(self.name, self.flow,)