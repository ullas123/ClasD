import streamlit as st
from utils.file_handler import get_file_structure
from typing import Dict

def show_project_structure(files: Dict[str, str]):
    """
    Display project structure in a tree-like format
    """
    st.header("Project Structure")
    
    structure = get_file_structure(files)
    
    def render_structure(struct, level=0):
        for key, value in struct.items():
            prefix = "    " * level
            if isinstance(value, dict):
                st.markdown(f"`{prefix}📁 {key}`")
                render_structure(value, level + 1)
            else:
                st.markdown(f"`{prefix}📄 {key}`")
    
    render_structure(structure)
