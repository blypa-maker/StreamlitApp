import os
import time
import uuid
from abc import ABC, abstractmethod

import streamlit as st
import numpy as np
import cv2
from PIL import Image
from streamlit_drawable_canvas import st_canvas

from src.Components.GPT_Generator import GPT_Generator, GPT_Vision
from src.Components.ComfyUIWorkflowFactory import WorkflowFactory
from src.UI.StreamlitChatImage import StreamlitChatImage, StreamlitChatImageCar


class ChatHistory(ABC):
    @abstractmethod
    def get_messages(self):
        pass

    @abstractmethod
    def add_message(self, role: str, content: str):
        pass


class ChatStream(ABC):
    @abstractmethod
    def stream_data(self, text: str):
        pass

 
class StreamlitChatHistory(ChatHistory):
     
    def __init__(self,chat_id:str)->None:
        self.chat_id = chat_id
        self.add_message('assistant',"Please provide an additional info")
    
    @st.cache_resource 
    def get_messages(_self):
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        return st.session_state.messages

    def add_message(self, role: str, content: str,   image_path:str = None     ):
        st.session_state.messages = self.get_messages()
        st.session_state.messages.append({"role": role, "content": content, 'image': image_path, 'chat_id': self.chat_id})

    
    def build_history_for_GPT(self):
        current_history  = self.get_messages()
        
        messeges_for_GPT = []

        if current_history:
            for message in current_history:
                if message['chat_id'] == self.chat_id:
                    messeges_for_GPT.append({key: message[key] for key in ["role","content"]} )

        return messeges_for_GPT

class SimpleChatStream(ChatStream):

    def stream_data(self, text: str):
        for word in text.split(" "):
            yield word + " "
            time.sleep(0.05)


class CarBotComponentFactory():

    def __init__(self, workflow: WorkflowFactory) -> None:
        self.workflow = workflow

    def getChatBotComponent(self):
        return CarBotComponent( self.workflow)

    
class CarBotComponent:

    def __init__(self,  factory: WorkflowFactory):
        self.chat_stream = SimpleChatStream()
        self.prompt_generator = GPT_Vision() ### Aggregation connection. When this is instance is die the GPT connection will die also.
        self.stable_diff = factory.get_workflow()

        self.chat_id = str(uuid.uuid4())
 
        self.history = StreamlitChatHistory(self.chat_id)
         

    def render_history(self):
        print(f"Rendering history for chat_id: {self.chat_id}")
        messages = self.history.get_messages()
         
        if messages:
            for message in messages:
                if message['chat_id'] == self.chat_id:
                    print(message)
                    with st.chat_message(message['role']):
                        st.write(message['content'])
                        if message['image']:
                             
                            self.display_images(message['image'], message['content'])
                
                
    def save_content(self, user:str, assistant:str, image_path:str = None): 
        self.history.add_message("user", user)
        self.history.add_message("assistant", assistant, image_path)
         

    def display_images(self, image_urls: list, text:str ): 
         
        for i, img_url in enumerate(image_urls):

                print("IMAGE HERE IS" , img_url)
                image = StreamlitChatImageCar(img_url,slogan= '' ,image_prompt= text)
                image.display(f"Image {i+1}")
                 
       


    def chat_form(self):
        base_dir, templates_dir = self.setup_directories()
        selected_transport, primary_image, mask_image = self.load_selected_transport(templates_dir)

        logo_file = st.file_uploader("Upload your logo", type=[ "png"])
        if logo_file:
            mask_image, overlay_image = self.process_logo(logo_file, primary_image, mask_image)
            
        wrap_style, services, slogan = self.get_user_inputs()
        self.render_history()

        prompt = st.chat_input("Say something")
        if prompt:
            image_id = str(uuid.uuid4())
            save_path = f'inpaint_inputs/{ image_id}.png'
            save_path_mask = f'inpaint_inputs/{ image_id}_{2}.png'
            logo_url = f'logos/logo_{image_id}.png'
            with open(logo_url, mode='wb') as w:
                w.write(logo_file.getvalue())

            Image.fromarray(overlay_image).save(save_path)
            Image.fromarray(mask_image).save(save_path_mask)
            
            self.process_prompt(prompt, wrap_style, services,selected_transport,logo_url, save_path_mask, save_path)


    def setup_directories(self):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        templates_dir = os.path.join(base_dir, "car_templates")
        return base_dir, templates_dir


    def load_selected_transport(self, templates_dir):
        transport_options = {
            "Chevrolete Silverado": ("Pickup.png", "Pickup_mask.png"),
            "Dodge RAM Pro Master": ("Van.png", "Van_mask.png")
        }

        selected_transport = st.selectbox("Select type of transport", list(transport_options.keys()))
        photo_file, mask_file = transport_options[selected_transport]

        photo_path = os.path.join(templates_dir, photo_file)
        mask_path = os.path.join(templates_dir, mask_file)

        primary_image = self.load_image(photo_path)
        mask_image = self.load_image(mask_path)

        return selected_transport, primary_image, mask_image


    def load_image(self, image_file):
        img = Image.open(image_file).convert("RGBA")
        return np.array(img)


    def process_logo(self, logo_file, primary_image, mask_image):
        logo_image = self.load_image(logo_file)
        logo_image, new_logo_width, new_logo_height = self.resize_logo(logo_image, primary_image)

        x, y, scale = self.get_logo_position_and_scale(primary_image, new_logo_width, new_logo_height)
        resized_logo = self.scale_logo(logo_image, new_logo_width, new_logo_height, scale)

        overlay_image = self.overlay_logo_on_image(primary_image, resized_logo, x, y)
        updated_mask = self.update_mask(mask_image, resized_logo, x, y)

        
        # Display updated images
        st.image(overlay_image, caption='Image with Logo', use_column_width=True)
        st.image(updated_mask, caption='Updated Mask', use_column_width=True)

        return updated_mask, overlay_image

    def resize_logo(self, logo_image, primary_image):
        logo_height, logo_width = logo_image.shape[:2]
        main_width = primary_image.shape[1]
        new_logo_width = main_width // 4
        scale_factor = new_logo_width / logo_width
        new_logo_height = int(logo_height * scale_factor)

        # Resize logo
        logo_image = Image.fromarray(logo_image).resize((new_logo_width, new_logo_height), Image.LANCZOS)
        return np.array(logo_image), new_logo_width, new_logo_height


    def get_logo_position_and_scale(self, primary_image, new_logo_width, new_logo_height):
        x = st.slider("X Position", 0, primary_image.shape[1] - new_logo_width, round((primary_image.shape[1] - new_logo_width) / 2))
        y = st.slider("Y Position", 0, primary_image.shape[0] - new_logo_height, round((primary_image.shape[0] - new_logo_height) / 2))
        scale = st.slider("Logo Scale", 0.1, 2.0, 1.0)
        return x, y, scale


    def scale_logo(self, logo_image, new_logo_width, new_logo_height, scale):
        return cv2.resize(logo_image, (int(new_logo_width * scale), int(new_logo_height * scale)))


    def overlay_logo_on_image(self, primary_image, resized_logo, x, y):
        overlay_image = primary_image.copy()
        alpha_s = resized_logo[:, :, 3] / 255.0  # Alpha channel
        alpha_l = 1.0 - alpha_s

        for c in range(0, 3):
            overlay_image[y:y + resized_logo.shape[0], x:x + resized_logo.shape[1], c] = (
                alpha_s * resized_logo[:, :, c] +
                alpha_l * overlay_image[y:y + resized_logo.shape[0], x:x + resized_logo.shape[1], c]
            )
        return overlay_image


    def update_mask(self, mask_image, resized_logo, x, y):
        updated_mask = mask_image.copy()
        mask_area = resized_logo[:, :, 3] > 0  # Non-transparent area of the logo
        updated_mask[y:y + resized_logo.shape[0], x:x + resized_logo.shape[1], :][mask_area] = [0, 0, 0, 0]
        return updated_mask


    def get_user_inputs(self):
        wrap_style = st.selectbox("Wrap style:", ["Clean and minimal", "Patriotic", "Photograph-feature",
                                                "Bright accent colors", "Edgy", "Nature graphics",
                                                "Camo graphics", "Illustration-feature", "Fun/quirky"])
        services = st.text_input("Provided services:")
        slogan = st.text_input("Provided slogan:")
        return wrap_style, services, slogan


    def process_prompt(self, prompt, wrap_style, services, car,logo_url, mask_image,overlay_image):
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            history = self.history.build_history_for_GPT()
            text = self.prompt_generator.Call_GPT_vision(car_name=car,wrap_style=wrap_style,services=services,logo=logo_url,add_info=prompt, history = history)

            st.write_stream(self.chat_stream.stream_data(text))
            with st.spinner("Generating images"):
                generated_image_path =[]
                for i in range(4):
                    generated_image_path.append(self.stable_diff.run_workflow(text, mask_image, overlay_image)[0])
                self.display_images(generated_image_path, text)

        self.save_content(prompt, text, generated_image_path)
