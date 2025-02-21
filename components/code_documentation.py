import streamlit as st
import pandas as pd
from utils.doc_analyzer import extract_documentation
from typing import Dict

def show_code_documentation(parsed_data: Dict):
    """
    Display code documentation in tabular format
    """
    st.header("Code Documentation")
    
    # Extract documentation
    documentation = extract_documentation(parsed_data)
    
    # Create tabs for different views
    class_tab, method_tab = st.tabs(["Classes", "Methods"])
    
    with class_tab:
        st.subheader("Class Documentation")
        if documentation['classes']:
            df_classes = pd.DataFrame(documentation['classes'])
            st.dataframe(
                df_classes,
                column_config={
                    "name": st.column_config.TextColumn("Class Name", width="medium"),
                    "type": st.column_config.TextColumn("Type", width="small"),
                    "file": st.column_config.TextColumn("Source File", width="medium"),
                    "description": st.column_config.TextColumn("Description", width="large"),
                },
                hide_index=True
            )
        else:
            st.info("No class documentation found")
    
    with method_tab:
        st.subheader("Method Documentation")
        if documentation['methods']:
            df_methods = pd.DataFrame(documentation['methods'])
            st.dataframe(
                df_methods,
                column_config={
                    "name": st.column_config.TextColumn("Full Name", width="large"),
                    "class": st.column_config.TextColumn("Class", width="medium"),
                    "method": st.column_config.TextColumn("Method", width="medium"),
                    "description": st.column_config.TextColumn("Description", width="large"),
                },
                hide_index=True
            )
        else:
            st.info("No method documentation found")
