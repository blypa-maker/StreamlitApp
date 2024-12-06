from src.Components.ComfyUIWorkflowManager import WorkflowManager, WorkflowManagerInPaint, WorkflowManagerInPaintCarMask
import uuid


class WorkflowFactory:
    def __init__(self, server_address="18.222.44.79:8188", workflow_parh="workflow/workflow_api_SD3.json", model_type="FLUX"):
        self.server_address = server_address
        self.prompt_file_path = workflow_parh
        self.model_type = model_type

    def get_workflow(self):
        return WorkflowManager(self.server_address, self.prompt_file_path, self.model_type)


class WorkflowFactoryInPaint:
    def __init__(self, server_address="18.222.44.79:8188", workflow_parh="workflow/workflow_api_SD3_inpainting.json", model_type="FLUX"):
        self.server_address = server_address
        self.prompt_file_path = workflow_parh
        self.model_type = model_type

    def get_workflow(self):
        return WorkflowManagerInPaint(self.server_address, self.prompt_file_path, self.model_type)


class WorkflowFactoryInPaintCars:
    def __init__(self, server_address="18.222.44.79:8188", workflow_parh="workflow/SD3_Car_with_mask_api.json", model_type="FLUX"):
        self.server_address = server_address
        self.prompt_file_path = workflow_parh
        self.model_type = model_type

    def get_workflow(self):
        return WorkflowManagerInPaintCarMask(self.server_address, self.prompt_file_path, self.model_type)
