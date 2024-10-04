import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from src.UI.TabComponents import InPaintTab, ApplyText
import time 
from PIL import Image, ImageDraw, ImageFont
from rembg import remove
import io 

class ImageWorkflow : 

    def __init__(self, image_path:str, image_prompt:str, slogan, logo) -> None:
         
        self.image_path = image_path
        self.image_prompt = image_prompt
        self.slogan = slogan
        self.logo = logo
        self.InPaintTab = InPaintTab(image_path, self.image_prompt)
        self.AppTextTab = ApplyText(self.image_path, self.slogan, self.logo)
         

    @st.dialog('Image Workflow', width='large')
    def render(self):
        with stylable_container(
            key="Upload_Data",
            css_styles="""
            div{
                display: flex;
                justify-content: flex-end;
                width: 100%;
            }
            """
        ):
            button = st.button("Close")

            if button:
                    st.rerun(scope='app')


        container = st.container()

        col1, col2 = st.columns([0.3,0.7])

         
 
        with container:
            
               
            with col1 : 
                
                st.write("Original Image")
                st.image(self.image_path,use_column_width = True )

            with col2 :
                tab1, tab2, tab3 = st.tabs(["In painting", "Wrap the car", "Apply text"])

                with tab1:
                    st.header("In painting Toolbar")
                    self.InPaintTab.renderUIElements()

                with tab2:
                    st.header("Wrap the car")
                     
                with tab3:
                    st.header("Apply text")
                    self.AppTextTab.renderUIElements()

class StreamlitChatImageCar() : 

    def __init__(self, image_path:str,slogan, image_prompt:str = 'Transparent') -> None:
        
        self.image_path = image_path 
        
        self.workflowUI = ImageWorkflow(self.image_path, image_prompt,slogan,None)
        self.image_prompt = image_prompt
        self.slogan = slogan
 
   
    def textsize(self, text, font):
        im = Image.new(mode="P", size=(0, 0))
        draw = ImageDraw.Draw(im)
        _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
        return width, height

    def display(self,caption:str):

        col1, col2 = st.columns([4, 1])   
        with col1:
            st.image(self.image_path)

        with col2:
            with stylable_container(
                key="container_with_border",
                css_styles=r"""
                    button div:before {
                        font-family: 'Font Awesome 5 Free';
                        content: '\f085';
                        display: inline-block;
                        padding-right: 3px;
                        vertical-align: middle;
                        font-weight: 900;
                        border-radius: 50%!important;
                    }
                    """,
                ):
                
                if st.button(" ", key=self.image_path):
                     
                    self.workflowUI.render()

class StreamlitChatImage() : 

    def __init__(self, image_path:str,slogan,logo, image_prompt:str = 'Transparent') -> None:
        
        self.image_path = image_path
        self.workflowUI = ImageWorkflow(self.image_path, image_prompt,slogan,logo)
        self.image_prompt = image_prompt
        self.slogan = slogan
        self.logo = logo
   
    def textsize(self, text, font):
        im = Image.new(mode="P", size=(0, 0))
        draw = ImageDraw.Draw(im)
        _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
        return width, height
            
    def display(self,caption:str):

        
        col1, col2 = st.columns([4, 1])   
        with col1:

            original_image = Image.open(self.image_path)

            if self.logo: 
            
 
    
                image = Image.open(self.logo)
                image = image.resize((200,200))


                img_bytes = io.BytesIO()
                image.save(img_bytes, format='PNG')
                img_bytes = img_bytes.getvalue()
    
                output = remove(img_bytes)
                
                img_without_bg = Image.open(io.BytesIO(output))
    
                original_width, original_height = original_image.size
    
                img_without_bg_width, img_without_bg_height = img_without_bg.size

            
                position = (original_width - img_without_bg_width, original_height - img_without_bg_height)

                
                original_image.paste(img_without_bg, position, img_without_bg)

                draw = ImageDraw.Draw(original_image)
                file = open("ArialMT.ttf", "rb")
                bytes_font = io.BytesIO(file.read())
                 
                font = ImageFont.truetype(bytes_font, 60) 
                text =self.slogan
                    
                text_width, text_height =  self.textsize(text, font)
                text_position = ((original_width - text_width) // 2, 10)  # 10 - відступ від верху
                    
                
                draw.text(text_position, text, font=font, fill=(255, 255, 255), )
                 
            st.image(original_image,use_column_width = True,caption=caption )
            
        with col2:
            with stylable_container(
                key="container_with_border",
                css_styles=r"""
                    button div:before {
                        font-family: 'Font Awesome 5 Free';
                        content: '\f085';
                        display: inline-block;
                        padding-right: 3px;
                        vertical-align: middle;
                        font-weight: 900;
                        border-radius: 50%!important;
                    }
                    """,
                ):
                
                if st.button(" ", key=self.image_path):
                     
                    self.workflowUI.render()
  