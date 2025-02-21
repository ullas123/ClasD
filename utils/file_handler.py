import os
import tempfile
from typing import List, Dict
import streamlit as st

def process_uploaded_files(uploaded_files) -> Dict[str, str]:
    """
    Process uploaded files and store their content
    """
    processed_files = {}
    
    for uploaded_file in uploaded_files:
        if uploaded_file.name.endswith('.java'):
            content = uploaded_file.getvalue().decode('utf-8')
            processed_files[uploaded_file.name] = content
            
    return processed_files

def get_file_structure(files: Dict[str, str]) -> Dict:
    """
    Create a hierarchical structure of the files
    """
    structure = {}
    
    for file_path in files.keys():
        parts = file_path.split('/')
        current = structure
        
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
            
        current[parts[-1]] = "file"
        
    return structure
