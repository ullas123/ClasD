import streamlit as st
import pandas as pd
from utils.visualizer import create_relationship_graph

def show_class_relationships(relationships):
    """
    Display class relationships in both tabular and graph format
    """
    st.header("Class Relationships")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Show inheritance relationships
        st.subheader("Inheritance Relationships")
        if relationships['inheritance']:
            df_inheritance = pd.DataFrame(relationships['inheritance'])
            st.dataframe(df_inheritance)
        else:
            st.info("No inheritance relationships found")
            
        # Show implementation relationships
        st.subheader("Implementation Relationships")
        if relationships['implementation']:
            df_implementation = pd.DataFrame(relationships['implementation'])
            st.dataframe(df_implementation)
        else:
            st.info("No implementation relationships found")
    
    with col2:
        # Show visualization
        st.subheader("Relationship Graph")
        fig = create_relationship_graph(relationships)
        st.plotly_chart(fig, use_container_width=True)
