import streamlit as st
from src.UI.MainView import render, chat_form
from src.Components.ComfyUIWorkflowFactory import WorkflowFactory, WorkflowFactoryInPaint, WorkflowFactoryInPaintCars

def main():

    st.sidebar.title("Model Selection")
    model_option = st.sidebar.selectbox(
        "Choose a Model",
        options=["FLUX", "SD3"],
        index=0
    )

    if model_option == "FLUX":
        paths = {
            "workflow_path": "workflow/workflow_api_Flux.json",
            "inpaint_path": "workflow/workflow_api_Flux_inpainting.json",
            "inpaint_cars_path": "workflow/Flux_Car_with_mask_api.json"
        }

    elif model_option == "SD3":
        paths = {
            "workflow_path": "workflow/workflow_api_SD3.json",
            "inpaint_path": "workflow/workflow_api_SD3_inpainting.json",
            "inpaint_cars_path": "workflow/SD3_Car_with_mask_api.json"
        }



    factory = WorkflowFactory(workflow_parh=paths["workflow_path"], model_type=model_option)
    factory_inpaint = WorkflowFactoryInPaint(workflow_parh=paths["inpaint_path"], model_type=model_option)
    factory_inpaint_cars = WorkflowFactoryInPaintCars(workflow_parh=paths["inpaint_cars_path"], model_type=model_option)

    render()

    chat_form(workflow=factory, inpaint_workflow=factory_inpaint, inpaint_cars_workflow=factory_inpaint_cars)

if __name__ == "__main__":
    main()
