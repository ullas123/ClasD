import streamlit as st
import os
from utils.file_handler import process_uploaded_files
from utils.code_parser import parse_java_files
from utils.relationship_analyzer import analyze_relationships
from components.project_structure import show_project_structure
from components.class_relationships import show_class_relationships
from components.data_flow import show_data_flow
from components.uml_diagram import show_uml_diagram
from components.code_documentation import show_code_documentation

def main():
    st.set_page_config(page_title="Java Code Analyzer", layout="wide")

    st.title("Java Code Analyzer")
    st.markdown("### Developed by Ullas")
    st.write("Upload your Java project files to analyze class relationships and structure")

    # Upload instructions
    st.markdown("""
    ### Upload Instructions:
    - Upload individual `.java` files
    - Or upload a `.zip` file containing your Java project
    - The analyzer will automatically process all Java files
    """)

    # File upload section
    uploaded_files = st.file_uploader(
        "Upload Java Files or ZIP Archive", 
        accept_multiple_files=True,
        type=['java', 'zip'],
        help="You can upload multiple Java files or a ZIP archive containing your Java project"
    )

    if uploaded_files:
        try:
            with st.spinner('Processing files...'):
                # Process uploaded files
                processed_files = process_uploaded_files(uploaded_files)

                if not processed_files:
                    st.warning("No Java files found in the upload. Please ensure you've uploaded Java source files.")
                    return

                # Show number of files processed
                st.success(f"Successfully processed {len(processed_files)} Java files")

                # Parse Java files
                parsed_data = parse_java_files(processed_files)

                # Analyze relationships
                relationships = analyze_relationships(parsed_data)

                # Create tabs for different views
                tab1, tab2, tab3, tab4, tab5 = st.tabs([
                    "Project Structure", 
                    "Class Relationships", 
                    "Data Flow",
                    "UML Diagram",
                    "Documentation"
                ])

                with tab1:
                    show_project_structure(processed_files)

                with tab2:
                    show_class_relationships(relationships)

                with tab3:
                    show_data_flow(relationships)

                with tab4:
                    show_uml_diagram(relationships)

                with tab5:
                    show_code_documentation(parsed_data)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.error("Please ensure all files are valid Java source files.")

if __name__ == "__main__":
    main()