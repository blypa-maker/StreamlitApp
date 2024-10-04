import websocket
import uuid
import json
import urllib.request
import urllib.parse
from PIL import Image
import io


class WebSocketClient:
    def __init__(self, server_address, client_id):
        self.server_address = server_address
        self.client_id = client_id
        self.ws = websocket.WebSocket()

    def connect(self):
        self.ws.connect(f"ws://{self.server_address}/ws?clientId={self.client_id}")

    def receive_message(self):
        return self.ws.recv()

    def close(self):
        self.ws.close()