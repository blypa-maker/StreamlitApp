import websocket
import uuid
import json
import urllib.request
import urllib.parse
from PIL import Image
import io
from src.Components.WebSocketService import WebSocketClient
from src.Components.StableDiffusionPromptService import PromptService
from src.Components.StableDiffusionImageService import ImageService


class PromptExecutionManager:
    def __init__(self, ws_client: WebSocketClient, prompt_service: PromptService, image_service: ImageService):
        self.ws_client = ws_client
        self.prompt_service = prompt_service
        self.image_service = image_service

    def get_images(self, prompt):
        # Queue the prompt and get its ID
        prompt_id = self.prompt_service.queue_prompt(prompt)['prompt_id']
        output_images = {}

        # Wait for the execution to complete
        while True:
            message = self.ws_client.receive_message()
            if isinstance(message, str):
                message_data = json.loads(message)
                if message_data['type'] == 'executing':
                    data = message_data['data']
                    if data['node'] is None and data['prompt_id'] == prompt_id:
                        break  # Execution is done
            else:
                continue  # Skip binary data (previews)

        # Retrieve images after execution
        history = self.prompt_service.get_history(prompt_id)[prompt_id]
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            images_output = []
            if 'images' in node_output:
                for image in node_output['images']:
                    image_data = self.image_service.get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
            output_images[node_id] = images_output

        return output_images


 
 
 