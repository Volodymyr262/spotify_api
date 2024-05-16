from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from random import randint
from time import sleep
import threading

class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)("broadcast", self.channel_name)
        if not hasattr(self.channel_layer, '_broadcast_thread'):
            self.start_broadcast()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("broadcast", self.channel_name)

    def send_message(self):
        while True:
            message = json.dumps({'message': randint(1, 100)})
            async_to_sync(self.channel_layer.group_send)(
                "broadcast",
                {
                    "type": "broadcast.message",
                    "message": message,
                }
            )
            sleep(1)

    def receive(self, text_data=None, bytes_data=None):
        pass

    def broadcast_message(self, event):
        message = event['message']
        self.send(text_data=message)

    def start_broadcast(self):
        def broadcast_loop():
            while True:
                message = json.dumps({'message': randint(1, 100)})
                async_to_sync(self.channel_layer.group_send)(
                    "broadcast",
                    {
                        "type": "broadcast.message",
                        "message": message,
                    }
                )
                sleep(1)

        self.channel_layer._broadcast_thread = threading.Thread(target=broadcast_loop)
        self.channel_layer._broadcast_thread.start()
