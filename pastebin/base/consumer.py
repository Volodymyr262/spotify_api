from channels.generic.websocket import AsyncWebsocketConsumer
import json
from random import randint
import asyncio
from threading import Thread


class WSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("broadcast", self.channel_name)

        if not hasattr(self.channel_layer, '_broadcast_thread_running'):
            self.channel_layer._broadcast_thread_running = False

        if not self.channel_layer._broadcast_thread_running:
            self.channel_layer._broadcast_thread_running = True
            self.start_broadcast()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("broadcast", self.channel_name)

        # Clean up broadcast thread if no one is connected
        if not await self.is_any_client_connected():
            self.channel_layer._broadcast_thread_running = False

    async def receive(self, text_data=None, bytes_data=None):
        pass

    async def broadcast_message(self, event):
        message = event['message']
        await self.send(text_data=message)

    def start_broadcast(self):
        def broadcast_loop():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.send_message())
            loop.close()

        Thread(target=broadcast_loop, daemon=True).start()

    async def send_message(self):
        while self.channel_layer._broadcast_thread_running:
            message = json.dumps({'message': randint(1, 100)})
            await self.channel_layer.group_send(
                "broadcast",
                {
                    "type": "broadcast.message",
                    "message": message,
                }
            )
            await asyncio.sleep(1)

    async def is_any_client_connected(self):
        return bool(await self.channel_layer.group_channels("broadcast"))

