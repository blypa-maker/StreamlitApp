from openai import OpenAI
import base64
from src.Components.ThreadSafeSingletonDecorator import thread_safe_singleton
import os
import requests

@thread_safe_singleton
class GPT_Generator:
    def __init__(self):
        self.pipeline = OpenAI()

    def get_valid_prompt(self, text: str) -> str:
        dot_split = text.split('.')[0]
        n_split = text.split('\n')[0]

        return {
            len(dot_split) < len(n_split): dot_split,
            len(n_split) > len(dot_split): n_split,
            len(n_split) == len(dot_split): dot_split   
        }[True]
    
     
    def preprocess_user_input(self, user_text:str, history:list,wrap_style,services, slogan, prompt_stle) -> str:

        print("Using GPT4 for prompt generation!")
        history.insert(0, {"role": "system", "content": "You are an expert in Gen AI and Stable Diffusion."})


        if prompt_stle == 'Banner' :
            prompt = {
                                "role": "user",
                                "content": f"""You're a talented banner designer with extensive experience in creating visually striking banner design descriptions. You have a deep understanding of color schemes, styles, and how to encapsulate client visions in a way that inspires design creation.
                                Your task is to create a detailed textual description of a future banner design based on a user questionnaire. Here are the details you need to incorporate:
                                -Banner style: {wrap_style}.
                                -Services provided by the client: {services}.
                                -Client's company slogan: {slogan}.
                                -Client's design wishes: {user_text}.
                                Make sure the generated description adheres to the following guidelines:
                                -Use a suitable color scheme and style that aligns with the client's brand and vision.
                                -Omit any reference to text or additional slogans in your description.
                                -Follow the style of prompts for Stable Diffusion 3, ensuring that the description is evocative and creative. In response, give only a prompt that briefly describes the design, following the aesthetic guidelines for a cohesive banner image. The response should be brief, meaningful, and without unnecessary information."""
                        }
        if prompt_stle == "Logo" : 

            prompt = {
                                "role": "user",
                                "content": f"""You're a talented logo designer with extensive experience in creating visually striking logo design descriptions. You have a deep understanding of color schemes, styles, and how to encapsulate client visions in a way that inspires design creation.
                                Your task is to create a detailed textual description of a future logo design based on a user questionnaire. Here are the details you need to incorporate:
                                -Logo style: {wrap_style}.
                                -Services provided by the client: {services}.
                                -Client's company slogan: {slogan}.
                                -Client's design preferences: {user_text}.
                                Make sure the generated description adheres to the following guidelines:
                                -Use a suitable color scheme and style that aligns with the client's brand and vision.
                                -Omit any reference to text or slogans in your description.
                                -Focus on a single logo design.
                                -Ensure the logo is presented on a white or transparent background.
                                -Follow the style of prompts for Stable Diffusion 3, ensuring that the description is evocative and creative. In response, give only a prompt that briefly describes the logo-style design for Stable Diffusion 3. The response should be brief, meaningful, and without unnecessary information.
                                """
                        }
            
        print(prompt)
        history.append(prompt)
        
        print(history)
        text = self.pipeline.chat.completions.create(
                        model="gpt-4o",
                        messages=history
                    )
        
        return self.get_valid_prompt(text.choices[0].message.content)
    
@thread_safe_singleton
class GPT_Vision:

    def __init__(self) -> None:
        pass

    def Call_GPT_vision(self, car_name, wrap_style, services, logo, add_info, history, view="Driver"):

        print("Using GPT4 for prompt generation!")
    
        # prompt = f"""Design a high-quality car wrap design template for {view} of the {car_name} for a service provider {services}. 
        #       Please analyze the provided logo and extract the following design elements: * Color Palette: What are the dominant colors in the logo, including shades and hues? * 
        #       Background Composition: What is the logo background's texture, pattern, or solid color. Avoid any text and human or animals description? 
        #       Consider the following wrap style: {wrap_style}. {'' if add_info else f"Take into account user prefferencess: {add_info}"}  Using the extracted design elements, generate a car wrap design template that incorporates the service provider's logo in a harmonious and visually appealing way. 
        #       Please provide a detailed description of the design composition, including the use of color and background elements, to ensure a high-quality output.Avoid any markdown elements in the response. As output provide only prompt in the following pattern. 
        #       Generate a car wrap design tample for {car_name}. [Descibe the backround elements taking into account provided logo and user prefferencess].[Describe the design style taking into account wrap style and color pallete]"""
        prompt = f"""Design a high-quality car wrap design template for {view} side of the {car_name} for a service provider of {services}.
Image provided is a customer logo, use it to extract color palette, background composition, etc.
Consider the following wrap style: {wrap_style}.
Additional user preferences: {'' if not add_info else add_info}.
Using the extracted design elements, generate a car wrap design template that incorporates the service provider's logo in a harmonious and visually appealing way.
Please provide a detailed description of the design composition, including the use of color and background elements, to ensure a high-quality output.
Assume that the client logo is already placed on the car and you don't need to describe it.
Try to avoid using any abstract phrases as generative model is worse at generating output with such prompt.
Avoid any markdown elements in the response, return only prompt in the following one-paragraph pattern.
Generate a car wrap design for {car_name}. [Descibe the background elements taking into account the provided logo and user preference. You can describe the design in details]"""
        def encode_image(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')

        API_KEY = os.environ['OPENAI_API_KEY']

        base64_image = encode_image(logo)

        headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
        }
        print("LEN HISTORY", len(history))
        if len(history) == 1: 
            payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a professional designer and is proficient in using diffusion generative models. You have to create a design based on user input and provide a prompt for diffusion generative model to produce such design.\nYou have to design a car wrap based on user preferences."
                },
                {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": prompt
                    },
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                    }
                ]
                }
            ],
            "max_tokens": 1000
            }

            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        else : 
            history.insert(0, {"role": "system", "content": "You are a professional designer and is proficient in using diffusion generative models. You have to create a design based on user input and provide a prompt for diffusion generative model to produce such design.\nYou have to design a car wrap based on user preferences."})
            payload = {
            "model": "gpt-4o",
            "messages": history,
            "max_tokens": 1000
            }

            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        return response.json()['choices'][0]['message']['content']
