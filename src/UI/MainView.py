import streamlit as st
import time 
from src.UI.ChatBotComponent import SimpleChatStream, StreamlitChatHistory, ChatBotComponentFactory
from src.Components.ComfyUIWorkflowFactory import WorkflowFactory, WorkflowFactoryInPaintCars
from src.UI.CarSanbox import CarBotComponentFactory
from src.UI.Sidebar import Sidebar
def render():
    st.title('Image Generator with AI')
    st.write('Describe an image, and I will generate it for you!')
    st.logo('https://wrapmate.com/assets/logo-black.svg')
    st.markdown("""
    <style>
        .stApp[data-teststate=running] .stChatInput textarea {
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""
            <style>
            div[aria-label="dialog"] {
                width: 100%;
                height:100%;
                 
                border: 2px solid black;
            }

            button[aria-label="Close"] {
                display:none;
            }

            </style>
            """, unsafe_allow_html=True)
    st.markdown(
            '''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"/>
                <style>
                button[title="View fullscreen"]{
                    visibility: hidden;}
                </style>''',
            unsafe_allow_html=True,
        )
    
        

def chat_form(workflow, inpaint_workflow, inpaint_cars_workflow):
     
         
    # chat_factory = ChatBotComponentFactory(workflow)
    # cars_factory = CarBotComponentFactory(WorkflowFactoryInPaintCars())
    # sidebar = Sidebar(chat_factory,cars_factory)
     
    # sidebar.render()
     
    chat_factory = ChatBotComponentFactory(workflow)
    cars_factory = CarBotComponentFactory(inpaint_cars_workflow)

    # Ініціалізуємо та рендеримо сайдбар
    sidebar = Sidebar(chat_factory, cars_factory)
    sidebar.render()
    
        