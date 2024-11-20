import streamlit as st
from src.UI.ChatBotComponent import ChatBotComponent, ChatBotComponentFactory
from src.UI.CarSanbox import CarBotComponent, CarBotComponentFactory

class Sidebar: 

    def __init__(self, chats_factory: ChatBotComponentFactory, cars: CarBotComponentFactory) -> None:
      
        self.chats_factory = chats_factory
        self.cars_factory = cars

    @st.cache_resource
    def get_chat_state(_self): 
        if 'chats' not in st.session_state:
            st.session_state.chats = {}

        return st.session_state.chats

    def render(self):

        st.sidebar.title("Workspaces")

        st.session_state.chats = self.get_chat_state()
            
        selected_workspace = st.sidebar.selectbox("Select a workspace", options=["Car", "Logo", "Banner"])

        
        if st.button("Clear history"):
                st.cache_data.clear()
                st.session_state.chats.clear() 
                st.rerun()

        if selected_workspace not in st.session_state.chats:
                if selected_workspace == 'Car':
                     st.session_state.chats["Car"] = self.cars_factory.getChatBotComponent()
            
                else:
                    if selected_workspace == 'Banner' : 
                        gpt_prompt = "Banner"
                    else : 
                        gpt_prompt = "Logo"
                    st.session_state.chats[selected_workspace] = self.chats_factory.getChatBotComponent(gpt_prompt)
    
        st.title(f"Selected workspace is: {selected_workspace}")

        current_bot_component = st.session_state.chats[selected_workspace]

        current_bot_component.chat_form()


 