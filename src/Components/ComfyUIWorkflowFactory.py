from src.Components.ComfyUIWorkflowManager import WorkflowManager, WorkflowManagerInPaint, WorkflowManagerInPaintCarMask
import uuid 


class WorkflowFactory:


    def __init__(self, server_address: str ="18.222.44.79:8188", workflow_parh:str = "workflow/workflow_api_SD3.json" ) -> None:
        self.server_address = server_address
         


        self.prompt_file_path = workflow_parh

        
    def get_workflow(self):

        return  WorkflowManager(self.server_address, self.prompt_file_path)
         

class WorkflowFactoryInPaint: 

    def __init__(self, server_address: str ="18.222.44.79:8188",  workflow_parh:str = "workflow/workflow_api_SD3_inpaintingi.json" ) -> None:
        self.server_address = server_address
         


        self.prompt_file_path = workflow_parh

        
    def get_workflow(self):

        return  WorkflowManagerInPaint(self.server_address, self.prompt_file_path)
    
class WorkflowFactoryInPaintCars: 

    def __init__(self, server_address: str ="18.222.44.79:8188",  workflow_parh:str = "workflow/SD3_Car_with_mask_api.json" ) -> None:
        self.server_address = server_address
         


        self.prompt_file_path = workflow_parh

        
    def get_workflow(self):

        return  WorkflowManagerInPaintCarMask(self.server_address, self.prompt_file_path)