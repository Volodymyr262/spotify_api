import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
import time


class WSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'room_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Send the current state of the room to the new client
        room_text = cache.get(self.room_group_name) or ""
        await self.send(text_data=json.dumps({
            'message': room_text
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        message = json.loads(text_data)['message']

        # Save the message to Redis via Django cache
        cache.set(self.room_group_name, message, timeout=None)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
