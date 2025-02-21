import javalang
from typing import Dict, List, Any
import re

def parse_javadoc(doc_str: str) -> Dict[str, str]:
    """
    Parse Javadoc comment into structured format
    """
    if not doc_str:
        return {
            'description': 'No documentation available',
            'params': {},
            'returns': '',
            'throws': []
        }

    # Clean up the comment
    doc_str = re.sub(r'\/\*+|\*+\/', '', doc_str)
    doc_str = re.sub(r'^\s*\*\s*', '', doc_str, flags=re.MULTILINE)

    # Initialize parsed data
    parsed = {
        'description': '',
        'params': {},
        'returns': '',
        'throws': []
    }

    # Extract different parts
    lines = doc_str.split('\n')
    current_section = 'description'
    description_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith('@param'):
            current_section = 'param'
            parts = line[6:].strip().split(maxsplit=1)
            if len(parts) > 1:
                parsed['params'][parts[0]] = parts[1]
            else:
                parsed['params'][parts[0]] = ''
        elif line.startswith('@return'):
            current_section = 'return'
            parsed['returns'] = line[7:].strip()
        elif line.startswith('@throws'):
            current_section = 'throws'
            parsed['throws'].append(line[7:].strip())
        else:
            if current_section == 'description':
                description_lines.append(line)
            elif current_section == 'param' and parsed['params']:
                last_param = list(parsed['params'].keys())[-1]
                parsed['params'][last_param] += ' ' + line
            elif current_section == 'return':
                parsed['returns'] += ' ' + line
            elif current_section == 'throws' and parsed['throws']:
                parsed['throws'][-1] += ' ' + line

    parsed['description'] = ' '.join(description_lines).strip()
    return parsed

def extract_documentation(parsed_data: Dict[str, Any]) -> Dict[str, List[Dict]]:
    """
    Extract and analyze documentation from Java files
    """
    documentation = {
        'classes': [],
        'methods': [],
        'packages': []
    }

    for filename, file_data in parsed_data.items():
        # Extract package info
        package_name = file_data.get('package', 'default')
        package_doc = {
            'name': package_name,
            'files': [filename],
            'description': 'Package containing Java source files'
        }
        documentation['packages'].append(package_doc)

        # Process classes
        for class_info in file_data.get('classes', []):
            # Extract class documentation
            class_doc = {
                'name': class_info['name'],
                'type': 'Class',
                'file': filename,
                'package': package_name,
                'extends': class_info.get('extends'),
                'implements': class_info.get('implements', []),
                'javadoc': parse_javadoc(class_info.get('documentation', '')),
                'annotations': []
            }

            documentation['classes'].append(class_doc)

            # Process methods
            for method in class_info.get('methods', []):
                method_doc = {
                    'name': method,
                    'class': class_info['name'],
                    'file': filename,
                    'package': package_name,
                    'javadoc': parse_javadoc(method.get('documentation', '')),
                    'parameters': method.get('parameters', []),
                    'return_type': method.get('return_type', 'void'),
                    'modifiers': method.get('modifiers', []),
                    'annotations': method.get('annotations', [])
                }

                documentation['methods'].append(method_doc)

    return documentation

def analyze_code_quality(documentation: Dict[str, List[Dict]]) -> Dict[str, Any]:
    """
    Analyze documentation quality and coverage
    """
    quality_metrics = {
        'total_classes': len(documentation['classes']),
        'total_methods': len(documentation['methods']),
        'documented_classes': 0,
        'documented_methods': 0,
        'documentation_coverage': {},
        'quality_scores': {}
    }

    # Analyze class documentation
    for class_doc in documentation['classes']:
        if class_doc['javadoc']['description'] != 'No documentation available':
            quality_metrics['documented_classes'] += 1

    # Analyze method documentation
    for method_doc in documentation['methods']:
        if method_doc['javadoc']['description'] != 'No documentation available':
            quality_metrics['documented_methods'] += 1

    # Calculate coverage percentages
    quality_metrics['documentation_coverage'] = {
        'classes': (quality_metrics['documented_classes'] / quality_metrics['total_classes'] * 100) if quality_metrics['total_classes'] > 0 else 0,
        'methods': (quality_metrics['documented_methods'] / quality_metrics['total_methods'] * 100) if quality_metrics['total_methods'] > 0 else 0
    }

    return quality_metrics