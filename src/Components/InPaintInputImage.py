from PIL import Image
import uuid 


class InPaintInputImage():

    def __init__(self, image : Image) -> None:
        

        self.image = image

        self.save_path = f"inpaint_inputs/{str(uuid.uuid4())}.png"


    def getMaskPath(self)->str: 

        self.image.save(self.save_path)

        return self.save_path
    
    #### TODO: Implement image deletion. 
    



