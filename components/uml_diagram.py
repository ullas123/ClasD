import streamlit as st
import graphviz
from typing import Dict, List
import math

def create_class_node(dot, class_info: Dict, cluster_id: int = None) -> None:
    """
    Create a UML class node with attributes and methods
    """
    class_name = class_info['name']
    label = f'<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">\n'

    # Class name
    label += f'<TR><TD PORT="header"><B>{class_name}</B></TD></TR>\n'

    # Fields
    label += '<TR><TD ALIGN="LEFT" BALIGN="LEFT">'
    for field in class_info['fields']:
        label += f'+ {field}<BR/>'
    label += '</TD></TR>\n'

    # Methods
    label += '<TR><TD ALIGN="LEFT" BALIGN="LEFT">'
    for method in class_info['methods']:
        label += f'+ {method}()<BR/>'
    label += '</TD></TR>\n'

    label += '</TABLE>>'

    if cluster_id is not None:
        with dot.subgraph(name=f'cluster_{cluster_id}') as c:
            c.attr(label=f'Package {cluster_id}')
            c.node(class_name, label=label)
    else:
        dot.node(class_name, label=label)

def split_classes(classes: List[Dict], num_sections: int) -> List[List[Dict]]:
    """
    Split classes into sections for manageable visualization
    """
    section_size = math.ceil(len(classes) / num_sections)
    return [classes[i:i + section_size] for i in range(0, len(classes), section_size)]

def show_uml_diagram(relationships: Dict):
    """
    Display UML class diagram with zoom and split functionality
    """
    st.header("UML Class Diagram")

    # Controls for diagram layout
    col1, col2 = st.columns(2)
    with col1:
        num_sections = st.slider("Split diagram into sections", 1, 4, 1)
    with col2:
        zoom_level = st.slider("Zoom level", 50, 200, 100)

    # Get all classes from relationships
    all_classes = []
    for file_data in relationships.get('parsed_data', {}).values():
        all_classes.extend(file_data.get('classes', []))

    # Split classes into sections
    class_sections = split_classes(all_classes, num_sections)

    # Create tabs for each section
    tabs = st.tabs([f"Section {i+1}" for i in range(len(class_sections))])

    # Create diagram for each section
    for section_idx, (tab, section_classes) in enumerate(zip(tabs, class_sections)):
        with tab:
            dot = graphviz.Digraph()
            dot.attr(rankdir='BT')

            # Add class nodes
            for class_info in section_classes:
                create_class_node(dot, class_info)

            # Add relationships
            for rel in relationships['inheritance']:
                if any(c['name'] in [rel['from'], rel['to']] for c in section_classes):
                    dot.edge(rel['from'], rel['to'], arrowhead='empty')

            for rel in relationships['implementation']:
                if any(c['name'] in [rel['from'], rel['to']] for c in section_classes):
                    dot.edge(rel['from'], rel['to'], arrowhead='empty', style='dashed')

            # Apply zoom
            dot.attr(size=f"{zoom_level/100:.2f},0")

            # Render diagram
            st.graphviz_chart(dot)

            # Show section stats
            st.info(f"Section {section_idx + 1}: {len(section_classes)} classes")