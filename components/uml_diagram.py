import streamlit as st
from typing import Dict, List
import math
import plantuml
import io
import base64
from typing import Dict, List

def generate_plantuml_class(class_info: Dict) -> str:
    """
    Generate PlantUML class definition
    """
    uml = []
    # Class definition
    if class_info.get('implements'):
        uml.append(f'class {class_info["name"]} implements {",".join(class_info["implements"])} {{')
    else:
        uml.append(f'class {class_info["name"]} {{')

    # Fields
    for field in class_info.get('fields', []):
        uml.append(f'    + {field}')

    # Methods
    for method in class_info.get('methods', []):
        uml.append(f'    + {method}()')

    uml.append('}')

    return '\n'.join(uml)

def split_classes(classes: List[Dict], num_sections: int) -> List[List[Dict]]:
    """
    Split classes into sections for manageable visualization
    """
    section_size = math.ceil(len(classes) / num_sections)
    return [classes[i:i + section_size] for i in range(0, len(classes), section_size)]

def show_uml_diagram(relationships: Dict):
    """
    Display UML class diagram with interactive zoom functionality
    """
    st.header("UML Class Diagram")

    with st.container():
        # Controls for diagram layout
        col1, col2 = st.columns(2)
        with col1:
            num_sections = st.slider("Split diagram into sections", 1, 8, 1, 
                                   help="Split the diagram into multiple sections for better visibility")
        with col2:
            zoom_level = st.slider("Zoom level", 50, 400, 100, step=10, 
                                help="Adjust diagram size (50% to 400%)")

        # Get all classes from relationships
        all_classes = []
        for file_data in relationships.get('parsed_data', {}).values():
            all_classes.extend(file_data.get('classes', []))

        # Split classes into sections
        class_sections = split_classes(all_classes, num_sections)

        # Create tabs for each section
        tabs = st.tabs([f"Section {i+1}" for i in range(len(class_sections))])

        # Initialize PlantUML
        plantuml_server = plantuml.PlantUML(url='http://www.plantuml.com/plantuml/svg/')

        # Create diagram for each section
        for section_idx, (tab, section_classes) in enumerate(zip(tabs, class_sections)):
            with tab:
                # Generate PlantUML code
                uml_code = [
                    "@startuml", 
                    "skinparam monochrome true", 
                    "skinparam shadowing false",
                    "skinparam classFontSize 14",
                    "skinparam defaultFontSize 12",
                    f"title Section {section_idx + 1} - {len(section_classes)} Classes"
                ]

                # Add classes
                for class_info in section_classes:
                    uml_code.append(generate_plantuml_class(class_info))

                # Add relationships
                for rel in relationships['inheritance']:
                    if any(c['name'] in [rel['from'], rel['to']] for c in section_classes):
                        uml_code.append(f"{rel['from']} --|> {rel['to']}")

                for rel in relationships['implementation']:
                    if any(c['name'] in [rel['from'], rel['to']] for c in section_classes):
                        uml_code.append(f"{rel['from']} ..|> {rel['to']}")

                uml_code.append("@enduml")

                # Generate SVG
                svg_diagram = plantuml_server.processes('\n'.join(uml_code))

                # Display SVG with zoom control
                st.markdown(f"""
                    <div style="width: 100%; overflow: auto;">
                        <div style="width: {zoom_level}%;">
                            {svg_diagram.decode()}
                        </div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )

                # Show section info
                st.caption(f"Displaying {len(section_classes)} classes in section {section_idx + 1}")