from channels.generic.websocket import AsyncWebsocketConsumer
import json 
from random import randint
from time import sleep
from epoc_app.models import P_info
from channels.db import database_sync_to_async


class DashboardConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.patient = self.scope['url_route']['kwargs']['patient_name']                      

        await self.accept()

        res = await database_sync_to_async(self.get_info(self.patient))()
        await self.send(json.dumps(res))
        

    def get_info(self, p_name):
       return P_info.objects.filter(name=p_name).order_by('-date')

    async def disconnect(self, code):
        print(f'connection closed with: {code}')

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']

        print(message,sender)

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }
        ))
