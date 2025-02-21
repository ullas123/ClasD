import javalang
from typing import Dict, List, Any
import streamlit as st

def parse_java_files(files: Dict[str, str]) -> Dict[str, Any]:
    """
    Parse Java files and extract class information including API calls
    """
    parsed_data = {}

    for filename, content in files.items():
        try:
            tree = javalang.parse.parse(content)

            class_info = {
                'classes': [],
                'interfaces': [],
                'imports': [],
                'package': None,
                'api_calls': []  # New field for API calls
            }

            # Extract package
            if tree.package:
                class_info['package'] = tree.package.name

            # Extract imports
            class_info['imports'] = [imp.path for imp in tree.imports]

            # Extract classes and interfaces
            for path, node in tree.filter(javalang.tree.TypeDeclaration):
                if isinstance(node, javalang.tree.ClassDeclaration):
                    # Extract REST/SOAP annotations and methods
                    api_methods = []
                    for method in node.methods:
                        annotations = [a.name for a in method.annotations] if method.annotations else []

                        # Check for REST annotations
                        rest_annotations = ['GET', 'POST', 'PUT', 'DELETE', 'RequestMapping']
                        if any(annot in rest_annotations for annot in annotations):
                            api_methods.append({
                                'type': 'REST',
                                'method': method.name,
                                'annotations': annotations,
                                'parameters': [
                                    {
                                        'name': param.name,
                                        'type': param.type.name if hasattr(param.type, 'name') else str(param.type)
                                    } for param in method.parameters
                                ]
                            })

                        # Check for SOAP annotations
                        soap_annotations = ['WebService', 'WebMethod']
                        if any(annot in soap_annotations for annot in annotations):
                            api_methods.append({
                                'type': 'SOAP',
                                'method': method.name,
                                'annotations': annotations,
                                'parameters': [
                                    {
                                        'name': param.name,
                                        'type': param.type.name if hasattr(param.type, 'name') else str(param.type)
                                    } for param in method.parameters
                                ]
                            })

                    class_info['classes'].append({
                        'name': node.name,
                        'extends': node.extends.name if node.extends else None,
                        'implements': [impl.name for impl in node.implements] if node.implements else [],
                        'methods': [method.name for method in node.methods],
                        'fields': [field.declarators[0].name for field in node.fields],
                        'api_methods': api_methods  # Add API methods to class info
                    })
                elif isinstance(node, javalang.tree.InterfaceDeclaration):
                    class_info['interfaces'].append({
                        'name': node.name,
                        'extends': [ext.name for ext in node.extends] if node.extends else [],
                        'methods': [method.name for method in node.methods]
                    })

            parsed_data[filename] = class_info

        except Exception as e:
            st.warning(f"Error parsing {filename}: {str(e)}")
            continue

    return parsed_data