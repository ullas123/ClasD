import streamlit as st
import os
from utils.file_handler import process_uploaded_files
from utils.code_parser import parse_java_files
from utils.relationship_analyzer import analyze_relationships
from components.project_structure import show_project_structure
from components.class_relationships import show_class_relationships
from components.data_flow import show_data_flow

def main():
    st.set_page_config(page_title="Java Code Analyzer", layout="wide")
    
    st.title("Java Code Analyzer")
    st.write("Upload your Java project files to analyze class relationships and structure")

    # File upload section
    uploaded_files = st.file_uploader("Upload Java Files", 
                                    accept_multiple_files=True,
                                    type=['java'])

    if uploaded_files:
        try:
            # Process uploaded files
            processed_files = process_uploaded_files(uploaded_files)
            
            # Parse Java files
            parsed_data = parse_java_files(processed_files)
            
            # Analyze relationships
            relationships = analyze_relationships(parsed_data)
            
            # Create tabs for different views
            tab1, tab2, tab3 = st.tabs(["Project Structure", 
                                      "Class Relationships", 
                                      "Data Flow"])
            
            with tab1:
                show_project_structure(processed_files)
                
            with tab2:
                show_class_relationships(relationships)
                
            with tab3:
                show_data_flow(relationships)
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.error("Please ensure all files are valid Java source files.")

if __name__ == "__main__":
    main()
