from PIL import Image, ImageDraw
import numpy as np

import streamlit as st
import torch 

class ImageMaskService: 

    def __init__(self) -> None:
        pass
    
     
    def load_image(self, image_file):

        print(image_file)
        img = Image.open(image_file)
         
        width, height = img.size

        new_size = (width // 2, height // 2)
        resized_img = img.resize(new_size)

        return resized_img

    def apply_mask_to_image(self, original_image:Image, mask_image:Image)-> Image:
        original_image = original_image.convert("RGBA")
        original_tensor = torch.from_numpy(np.array(original_image)).permute(2, 0, 1)  # Convert to CxHxW
        mask_tensor = torch.from_numpy(np.array(mask_image)).permute(2, 0, 1)

        # Create the output tensor
        output_tensor = original_tensor.clone()

        # Set alpha channel based on the mask
        red_channel = mask_tensor[0]  # Get the red channel from the mask
        output_tensor[3] = torch.where(red_channel == 255, torch.tensor(0), original_tensor[3])  # Set alpha to 0 where the mask is red

        # Convert output tensor back to an image
        output_image = Image.fromarray(output_tensor.permute(1, 2, 0).byte().numpy(), mode='RGBA')

        return output_image
    

    def get_masked_image(self, image_data, image) : 

        
        mask = Image.fromarray((image_data).astype(np.uint8))
         
        masked_image = self.apply_mask_to_image(image, mask)

        return masked_image