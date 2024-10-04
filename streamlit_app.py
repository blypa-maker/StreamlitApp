import streamlit as st
import os
import sys
from  src.UI.MainView import render, chat_form
from src.Components.ComfyUIWorkflowFactory import WorkflowFactory 

 

def main():
     

     
    render()

    factory = WorkflowFactory()
    chat_form(workflow=factory)

    
 


if __name__ == "__main__":
    main()