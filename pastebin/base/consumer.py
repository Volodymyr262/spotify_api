import threading

from channels.generic.websocket import WebsocketConsumer
import json
from random import randint
from time import sleep


class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        threading.Thread(target=self.send_message).start()

    def disconnect(self, close_code):
        pass

    def send_message(self):
        while True:
            message = json.dumps({'message': randint(1, 100)})
            self.send(message)
            sleep(1)