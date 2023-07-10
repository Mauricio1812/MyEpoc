from django.db import models

from accounts.models import User

class Message(models.Model):
    body = models.TextField()
    sent_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    ## models.SET_NULL means that when user is deleted the message remains but without a connection

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.sent_by}'
    

class Room(models.Model):
    WAITING = 'waiting'
    ATTENDED = 'attended'
    CHOICES_STATUS = {
        (WAITING, 'Waiting'),
        (ATTENDED, 'Attended'),
    }

    uuid = models.CharField(max_length=255)     #Unique id for fronted (js id)
    client = models.CharField(max_length=255)   #User on frontend
    agent = models.ForeignKey(User, related_name='rooms', blank=True, null=True, on_delete=models.SET_NULL)
    messages = models.ManyToManyField(Message, blank=True) #Blank in case no message
    url = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20, choices=CHOICES_STATUS, default=WAITING)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.client} - {self.uuid}'


