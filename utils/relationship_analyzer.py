import networkx as nx
from typing import Dict, Any

def analyze_relationships(parsed_data: Dict[str, Any]) -> Dict:
    """
    Analyze relationships between classes including API dependencies
    """
    relationships = {
        'inheritance': [],
        'implementation': [],
        'associations': [],
        'dependencies': set(),
        'parsed_data': parsed_data  # Include parsed data for API information
    }

    # Create a graph for class relationships
    graph = nx.DiGraph()

    for filename, file_data in parsed_data.items():
        # Analyze class inheritance and implementation
        for class_info in file_data['classes']:
            class_name = class_info['name']

            # Add inheritance relationships
            if class_info['extends']:
                relationships['inheritance'].append({
                    'from': class_name,
                    'to': class_info['extends']
                })
                graph.add_edge(class_name, class_info['extends'], type='inheritance')

            # Add implementation relationships
            for interface in class_info['implements']:
                relationships['implementation'].append({
                    'from': class_name,
                    'to': interface
                })
                graph.add_edge(class_name, interface, type='implementation')

            # Analyze field types for associations
            for field in class_info['fields']:
                relationships['associations'].append({
                    'from': class_name,
                    'field': field
                })

            # Add dependencies based on imports
            for imp in file_data['imports']:
                relationships['dependencies'].add((class_name, imp.split('.')[-1]))

            # Add API dependencies
            for api_method in class_info.get('api_methods', []):
                for param in api_method['parameters']:
                    param_type = param['type']
                    if param_type not in ['String', 'int', 'long', 'boolean', 'double', 'float']:
                        relationships['dependencies'].add((class_name, param_type))

    relationships['graph'] = graph
    return relationships