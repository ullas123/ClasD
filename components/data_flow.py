import streamlit as st
import pandas as pd
from typing import Dict

def show_data_flow(relationships: Dict):
    """
    Display data flow information
    """
    st.header("Data Flow Analysis")
    
    # Show associations
    st.subheader("Class Associations")
    if relationships['associations']:
        df_associations = pd.DataFrame(relationships['associations'])
        st.dataframe(df_associations)
    else:
        st.info("No associations found")
    
    # Show dependencies
    st.subheader("Dependencies")
    if relationships['dependencies']:
        dependencies_list = [{"from": dep[0], "to": dep[1]} 
                           for dep in relationships['dependencies']]
        df_dependencies = pd.DataFrame(dependencies_list)
        st.dataframe(df_dependencies)
    else:
        st.info("No dependencies found")
    
    # Add metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Classes", 
                 len(set([rel['from'] for rel in relationships['associations']])))
    with col2:
        st.metric("Total Dependencies", 
                 len(relationships['dependencies']))
    with col3:
        st.metric("Total Relationships",
                 len(relationships['inheritance']) + 
                 len(relationships['implementation']))
