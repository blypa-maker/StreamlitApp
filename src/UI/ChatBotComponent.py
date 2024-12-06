import streamlit as st
import time
from src.Components.GPT_Generator import GPT_Generator
import uuid
from abc import ABC, abstractmethod
from src.Components.ComfyUIWorkflowFactory import WorkflowFactory
from src.UI.StreamlitChatImage import StreamlitChatImage

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
        self.add_message('assistant',"Please  provide an additional info")
    

    @st.cache_resource 
    def get_messages(_self):
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        return st.session_state.messages


    def add_message(self, role: str, content: str,   image_path:str = None):
        st.session_state.messages = self.get_messages()
        st.session_state.messages.append({"role": role, "content": content, 'image': image_path, 'chat_id': self.chat_id})

    
    def build_history_for_GPT(self):
        current_history  = self.get_messages()
        
        messeges_for_GPT = []

        if current_history:
            for message in current_history:
                if message['chat_id'] == self.chat_id:
                    messeges_for_GPT.append(message)

        return messeges_for_GPT

class SimpleChatStream(ChatStream):

    def stream_data(self, text: str):
        for word in text.split(" "):
            yield word + " "
            time.sleep(0.05)


class ChatBotComponentFactory():

    def __init__(self, workflow: WorkflowFactory) -> None:       
        self.workflow = workflow

    def getChatBotComponent(self,prompt):   
        return ChatBotComponent( self.workflow, prompt)

    
class ChatBotComponent:

    def __init__(self,  factory: WorkflowFactory, prompt:str):
        self.chat_stream = SimpleChatStream()
        self.prompt_generator = GPT_Generator() ### Aggregation connection. When this is instance is die the GPT connection will die also.
        self.stable_diff = factory.get_workflow()

        self.chat_id = str(uuid.uuid4())
        self.chat_gpt_prompt = prompt
        self.history = StreamlitChatHistory(self.chat_id)
         

    def render_history(self):
        messages = self.history.get_messages()
        if not messages:
            st.write("No messages yet.") 
            
            for message in messages:
                if message['chat_id'] == self.chat_id:
                    with st.chat_message(message['role']):
                        st.write(message['content'])
                        if message['image']:
                            self.display_images(message['image'], message['content'])
                

    def save_content(self, user:str, assistant:str, image_path:str = None): 
        self.history.add_message("user", user)
        self.history.add_message("assistant", assistant, image_path)
         

    def display_images(self, image_urls: list, text:str ): 
        row1 = st.columns(2)  
        row2 = st.columns(2)
        print(text)
        for i, img_url in enumerate(image_urls[:2]):
            with row1[i]: 
                # image = StreamlitChatImage(image_path=img_url, image_prompt=text, logo=self.logo, slogan=self.slogan)
                image = StreamlitChatImage(image_path=img_url, image_prompt=text, slogan=self.slogan)

  
                image.display(f"Image {i+1}")
                 
        for i, img_url in enumerate(image_urls[2:]):
            with row2[i]:
                image = StreamlitChatImage(image_path=img_url, image_prompt=text, slogan=self.slogan)
 
                image.display(f"Image {i+3}")


            
    def chat_form(self):
        wrap_style = st.selectbox("Wrap style:", ["Clean and minimal", "Patriotic", "Photograph-feature", 
                                              "Bright accent colors", "Edgy", "Nature graphics", 
                                              "Camo graphics", "Illustration-feature", "Fun/quirky"])
        services = st.text_input("Provided services: ")

        self.slogan = st.text_input("Provided slogan: ")
        
        self.render_history()
      
        prompt = st.chat_input("Say something")
         
        if prompt:
             
            with st.chat_message("user"):
                st.write(prompt)
            
            with st.chat_message("assistant"):
                history = self.history.build_history_for_GPT()
                text = self.prompt_generator.preprocess_user_input(prompt,history,wrap_style,services,self.slogan, self.chat_gpt_prompt)
                 
                st.write_stream(self.chat_stream.stream_data(text))
                with st.spinner("Generating images"):
                    generated_image_path = self.stable_diff.run_workflow(text)
                    self.display_images(generated_image_path, text)

            self.save_content(prompt,text,generated_image_path)
