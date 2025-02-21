import javalang
from typing import Dict, List, Any
import re

def extract_documentation(parsed_data: Dict[str, Any]) -> Dict[str, List[Dict]]:
    """
    Extract and analyze documentation from Java files
    """
    documentation = {
        'classes': [],
        'methods': []
    }
    
    for filename, file_data in parsed_data.items():
        # Process classes
        for class_info in file_data.get('classes', []):
            class_doc = {
                'name': class_info['name'],
                'type': 'Class',
                'file': filename,
                'description': 'A Java class',  # Default description
                'annotations': []
            }
            
            # Extract class documentation from source
            if hasattr(class_info, '_position'):
                class_doc['description'] = extract_javadoc(class_info)
            
            documentation['classes'].append(class_doc)
            
            # Process methods
            for method in class_info.get('methods', []):
                method_doc = {
                    'name': f"{class_info['name']}.{method}",
                    'class': class_info['name'],
                    'method': method,
                    'description': 'A Java method',  # Default description
                    'parameters': []
                }
                
                # Add to methods list
                documentation['methods'].append(method_doc)
    
    return documentation

def extract_javadoc(node) -> str:
    """
    Extract Javadoc comments from a node
    """
    if hasattr(node, 'documentation') and node.documentation:
        # Clean up the comment
        doc = node.documentation
        # Remove /** and */ and clean up whitespace
        doc = re.sub(r'\/\*+|\*+\/', '', doc)
        # Remove leading asterisks and whitespace
        doc = re.sub(r'^\s*\*\s*', '', doc, flags=re.MULTILINE)
        # Clean up extra whitespace
        doc = ' '.join(doc.split())
        return doc
    return "No documentation available"
