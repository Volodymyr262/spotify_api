# consumer.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Room, TextSnippet
from asgiref.sync import sync_to_async

class WSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'editor_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Load the latest text from the database
        room, _ = await sync_to_async(Room.objects.get_or_create)(room_id=self.room_name)
        text_snippet, _ = await sync_to_async(TextSnippet.objects.get_or_create)(room=room)
        await self.send(text_data=json.dumps({
            'message': text_snippet.text
        }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Save the text to the database
        room = await sync_to_async(Room.objects.get)(room_id=self.room_name)
        text_snippet, _ = await sync_to_async(TextSnippet.objects.get_or_create)(room=room)
        text_snippet.text = message
        await sync_to_async(text_snippet.save)()

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'editor_message',
                'message': message
            }
        )

    async def editor_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
