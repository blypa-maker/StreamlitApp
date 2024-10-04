import streamlit as st
from abc import ABC, abstractmethod
from src.Components.ImageMaskService import ImageMaskService
from streamlit_drawable_canvas import st_canvas
import uuid
import io
from src.Components.ComfyUIWorkflowFactory import WorkflowFactoryInPaint
from src.Components.InPaintInputImage import InPaintInputImage
from PIL import Image,ImageDraw, ImageFont
from rembg import remove

class Tab(ABC):


    def __init__(self) -> None:

        pass

    @abstractmethod
    def renderUIElements(self, image_url:str):

        pass



class InPaintTab(Tab): 


    def __init__(self, image_url: str, image_prompt:str) -> None:
        self.image_url = image_url

        self.image_prompt = image_prompt
        self.workflow = WorkflowFactoryInPaint().get_workflow()
    

            
    def renderUIElements(self,):
        
        container = st.container()
        image = ImageMaskService().load_image(self.image_url)
         
        with container: 

            toolbar = st.container()

            with toolbar: 

                drawing_mode_col , stroke_width_col,prompt_col = st.columns([0.3,0.3,0.4])
                col1, col3 = st.columns([0.5,0.5])
                with drawing_mode_col: 
                    drawing_mode= st.selectbox(
                        "Figure", ( "freedraw", "line", "rect", "circle", "transform")
                    )
                
                
                with stroke_width_col:
                    stroke_width = st.slider("Stroke width: ", 1, 25, 3)

                 
            
                with prompt_col: 

                    prompt = st.text_area(label= 'Prompt' , value=self.image_prompt)

                    generate_button = st.button("Generate Image")

                    
             

            with col1: 
             
               
            # Create a drawable canvas for the mask
                st.write("Draw mask on the image")
                canvas_result = st_canvas(
                    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
                    stroke_width=stroke_width,
                    stroke_color='rgba(255, 0, 0, 1.0)',
                    background_image=image,
                    update_streamlit=True,
                    height=image.size[1],
                    width=image.size[0],
                    drawing_mode=drawing_mode,
           
                    key=f"canvas_{self.image_url}",
                    display_toolbar = True
                )
                 
                 
                # If there's drawing on the canvas, apply the mask
                if canvas_result.image_data is not None:
                   
                        masked_image = ImageMaskService().get_masked_image(canvas_result.image_data, image)

                        width, height = image.size

                        new_size = (width * 2, height * 2)
                        masked_image = masked_image.resize(new_size)
                        # st.write("Masked Image")
                        # st.image(masked_image, caption="Masked Image", use_column_width=True)

                        
        
            with col3: 

                st.write("Generated Image")
            


            if generate_button: 
                with col3: 
                           
                    with st.spinner("Generating image"):
                                
                                mask_input = InPaintInputImage(masked_image)
                                
                                generated_image_path = self.workflow.run_workflow(
                                    pos_prompt = prompt,
                                    mask = mask_input.getMaskPath()
                                )
                                 
                                st.image(generated_image_path)


class ApplyText(Tab): 


    def __init__(self, image_url: str, slogan:str, logo) -> None:
        self.image_url = image_url

        self.slogan = slogan
        self.logo = logo

    
    def renderUIElements(self ):
        
        # st.write(self.slogan)
        original_image = Image.open(self.image_url)

          # Білий текст     
        buffered = io.BytesIO()
        original_image.save(buffered, format="PNG")

        st.image(original_image, use_column_width=True)
            
        st.download_button("Download", buffered.getvalue(), file_name="final_image.png")