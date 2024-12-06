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
from src.Components.StableDiffusionManager import PromptExecutionManager
import requests
import random
 
class WorkflowManager:
    def __init__(self, server_address, prompt_file_path, model_type):
        self.server_address = server_address
        self.client_id = str(uuid.uuid4())
        self.prompt_file_path = prompt_file_path
        self.model_type = model_type

        # Initialize services using composition aggregation
        self.ws_client = WebSocketClient(self.server_address, self.client_id)
        self.prompt_service = PromptService(self.server_address, self.client_id)
        self.image_service = ImageService(self.server_address)
        self.execution_manager = PromptExecutionManager(self.ws_client, self.prompt_service, self.image_service)

    def run_workflow(self, pos_prompt, neg_prompt= None):
        # Connect to WebSocket
        self.ws_client.connect()

        # Read the prompt from the file
        prompt = self.read_prompt_from_file(self.prompt_file_path)

        # Modify the prompt text
        prompt["6"]["inputs"]["text"] = pos_prompt

        # Execute the prompt and retrieve images
        images = self.execution_manager.get_images(prompt)

        # Save the images and return the file path of the last image saved
        saved_image_path = self.save_images(images)

        # Close WebSocket connection
        self.ws_client.close()

        return saved_image_path

    def read_prompt_from_file(self, file_path):

        with open(file_path, 'r') as file:
            prompt_text = json.load(file)
        return prompt_text

    def save_images(self, images):
         
        last_image_path = None 
        images_list = []  
        for node_id, image_list in images.items():
            print(f"Saving images for node: {node_id}")
             
            for i, image_data in enumerate(image_list):
                img_id = str(uuid.uuid4())
                last_image_path = f"outputs/img_{node_id}_{i}_{img_id}.png"
                ImageSaver.save_image(image_data, last_image_path)
                images_list.append(last_image_path)    
                
        print(images_list)
        return images_list

class WorkflowManagerInPaint(WorkflowManager): 

    def __init__(self, server_address, prompt_file_path, model_type):
        super().__init__(server_address, prompt_file_path, model_type)
        
     
    def upload_mask_to_comfy(self,image_path:str): 
        url = f"http://{self.server_address}/upload/image"
            
        files = {'image': open(image_path, 'rb')}
        data = {
            'overwrite': 'true',  # or 'true'/'1' if you want to allow overwriting
            'subfolder': '',  # your subfolder, if needed
            'type': 'input'  # or appropriate type
        }

        # Send the POST request
        response = requests.post(url, files=files, data=data)


        return response.json()['name']


    def run_workflow(self, pos_prompt:str,mask:str , neg_prompt= None):
        # Connect to WebSocket
        self.ws_client.connect()

        prompt = self.read_prompt_from_file(self.prompt_file_path)
        mask = self.upload_mask_to_comfy(mask)

        # Modify the prompt text
        print("Loaded prompt:", prompt)
        prompt["6"]["inputs"]["text"] = pos_prompt
        prompt['273']['inputs']['image'] = mask
        images = self.execution_manager.get_images(prompt)

        # Save the images and return the file path of the last image saved
        saved_image_path = self.save_images(images)

        # Close WebSocket connection
        self.ws_client.close()

        return saved_image_path
    

class WorkflowManagerInPaintCarMask(WorkflowManager): 

    def __init__(self, server_address, prompt_file_path, model_type):
        super().__init__(server_address, prompt_file_path, model_type)
     

    def upload_mask_to_comfy(self,image_path:str): 

        url = f"http://{self.server_address}/upload/image"
        files = {'image': open(image_path, 'rb')}
        data = {
            'overwrite': 'true',  # or 'true'/'1' if you want to allow overwriting
            'subfolder': '',  # your subfolder, if needed
            'type': 'input'  # or appropriate type
        }

        # Send the POST request
        response = requests.post(url, files=files, data=data)

        return response.json()['name']


    # def run_workflow(self, pos_prompt:str,mask:str, car_image:str, neg_prompt= None):
    def run_workflow(self, pos_prompt: str, mask: str, car_image: str, neg_prompt=None):
        # Connect to WebSocket
        self.ws_client.connect()
        seed = random.randint(1,1000000000)
        # Read the prompt from the file
        prompt = self.read_prompt_from_file(self.prompt_file_path)
        mask = self.upload_mask_to_comfy(mask)
        car_image = self.upload_mask_to_comfy(car_image)
     
        # Modify the prompt text
        prompt["6"]["inputs"]["text"] = pos_prompt
        
        if self.model_type == "FLUX":
            prompt["27"]["inputs"]["text"] = neg_prompt if neg_prompt else "text, watermarks, blurry, horror, car elements"
            prompt['29']['inputs']['image'] = car_image
            prompt['30']['inputs']['image'] = mask
            prompt['36']['inputs']['seed'] = seed
        elif self.model_type == "SD3":
            prompt["71"]["inputs"]["text"] = neg_prompt if neg_prompt else "text, watermarks, blurry, horror, car elements"
            prompt['273']['inputs']['image'] = car_image
            prompt['279']['inputs']['image'] = mask
            prompt['271']['inputs']['seed'] = seed

        images = self.execution_manager.get_images(prompt)

        # Save the images and return the file path of the last image saved
        saved_image_path = self.save_images(images)

        # Close WebSocket connection
        self.ws_client.close()

        return saved_image_path
    

class ImageSaver:
    @staticmethod
    def save_image(image_data, filename):
        # """Saves image data to a specified file."""
        image = Image.open(io.BytesIO(image_data))
        image.save(filename)