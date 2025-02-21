import streamlit as st
from utils.file_handler import get_file_structure
from typing import Dict, List
import os

def extract_file_info(files: Dict[str, str]) -> List[Dict]:
    """
    Extract detailed file information for tabular display
    """
    file_info = []
    for filepath, content in files.items():
        # Get file details
        filename = os.path.basename(filepath)
        directory = os.path.dirname(filepath)
        file_size = len(content.encode('utf-8'))

        # Determine file type based on content analysis
        file_type = "Java Class"
        if "interface" in content.lower():
            file_type = "Java Interface"
        elif "enum" in content.lower():
            file_type = "Java Enum"

        # Count lines of code
        loc = len(content.splitlines())

        file_info.append({
            "File Name": filename,
            "Directory": directory if directory else "Root",
            "Type": file_type,
            "Size (bytes)": file_size,
            "Lines of Code": loc,
            "Full Path": filepath
        })

    return file_info

def show_project_structure(files: Dict[str, str]):
    """
    Display project structure in both tree and table formats
    """
    st.header("Project Structure")

    # Create tabs for different views
    tree_tab, table_tab = st.tabs(["Tree View", "Detailed View"])

    with tree_tab:
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

    with table_tab:
        # Create detailed table view
        file_info = extract_file_info(files)

        # Add project summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Files", len(file_info))
        with col2:
            total_loc = sum(info["Lines of Code"] for info in file_info)
            st.metric("Total Lines of Code", total_loc)
        with col3:
            total_size = sum(info["Size (bytes)"] for info in file_info)
            st.metric("Total Size (KB)", f"{total_size/1024:.2f}")

        # Show detailed table
        st.subheader("File Details")
        st.dataframe(
            file_info,
            column_config={
                "File Name": st.column_config.TextColumn("File Name", width="medium"),
                "Directory": st.column_config.TextColumn("Directory", width="medium"),
                "Type": st.column_config.TextColumn("Type", width="small"),
                "Size (bytes)": st.column_config.NumberColumn("Size (bytes)", format="%d"),
                "Lines of Code": st.column_config.NumberColumn("Lines of Code", format="%d"),
                "Full Path": st.column_config.TextColumn("Full Path", width="large")
            },
            hide_index=True
        )