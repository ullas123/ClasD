import os
import tempfile
from typing import List, Dict
import streamlit as st
import zipfile
import io
import chardet

def process_uploaded_files(uploaded_files) -> Dict[str, str]:
    """
    Process uploaded files and store their content.
    Supports both individual Java files and ZIP archives.
    """
    processed_files = {}

    for uploaded_file in uploaded_files:
        if uploaded_file.name.endswith('.zip'):
            # Process ZIP file
            with zipfile.ZipFile(io.BytesIO(uploaded_file.getvalue())) as z:
                for file_info in z.filelist:
                    if file_info.filename.endswith('.java'):
                        with z.open(file_info) as f:
                            content = f.read()
                            # Detect encoding
                            encoding = chardet.detect(content)['encoding'] or 'utf-8'
                            try:
                                decoded_content = content.decode(encoding)
                                processed_files[file_info.filename] = decoded_content
                            except UnicodeDecodeError:
                                st.warning(f"Could not decode {file_info.filename} with detected encoding {encoding}")
                                continue
        elif uploaded_file.name.endswith('.java'):
            # Process individual Java file
            content = uploaded_file.getvalue()
            # Detect encoding
            encoding = chardet.detect(content)['encoding'] or 'utf-8'
            try:
                decoded_content = content.decode(encoding)
                processed_files[uploaded_file.name] = decoded_content
            except UnicodeDecodeError:
                st.warning(f"Could not decode {uploaded_file.name} with detected encoding {encoding}")
                continue

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