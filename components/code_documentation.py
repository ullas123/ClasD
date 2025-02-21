import streamlit as st
import pandas as pd
from utils.doc_analyzer import extract_documentation, analyze_code_quality
from typing import Dict

def show_documentation_quality(quality_metrics: Dict):
    """
    Display documentation quality metrics
    """
    st.subheader("Documentation Quality Metrics")

    # Create metrics display
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Classes", quality_metrics['total_classes'])
    with col2:
        st.metric("Documented Classes", quality_metrics['documented_classes'])
    with col3:
        st.metric("Total Methods", quality_metrics['total_methods'])
    with col4:
        st.metric("Documented Methods", quality_metrics['documented_methods'])

    # Show coverage percentages
    st.subheader("Documentation Coverage")
    coverage = quality_metrics['documentation_coverage']
    st.progress(coverage['classes'] / 100, text=f"Class Documentation: {coverage['classes']:.1f}%")
    st.progress(coverage['methods'] / 100, text=f"Method Documentation: {coverage['methods']:.1f}%")

def format_javadoc(javadoc: Dict) -> str:
    """
    Format Javadoc content for display
    """
    formatted = [f"**Description:** {javadoc['description']}"]

    if javadoc['params']:
        formatted.append("\n**Parameters:**")
        for param, desc in javadoc['params'].items():
            formatted.append(f"- `{param}`: {desc}")

    if javadoc['returns']:
        formatted.append(f"\n**Returns:** {javadoc['returns']}")

    if javadoc['throws']:
        formatted.append("\n**Throws:**")
        for exception in javadoc['throws']:
            formatted.append(f"- {exception}")

    return "\n".join(formatted)

def show_code_documentation(parsed_data: Dict):
    """
    Display code documentation in an organized format
    """
    st.header("Code Documentation")

    # Extract and analyze documentation
    documentation = extract_documentation(parsed_data)
    quality_metrics = analyze_code_quality(documentation)

    # Show quality metrics
    show_documentation_quality(quality_metrics)

    # Create tabs for different views
    package_tab, class_tab, method_tab = st.tabs(["Packages", "Classes", "Methods"])

    with package_tab:
        st.subheader("Package Documentation")
        if documentation['packages']:
            for package in documentation['packages']:
                with st.expander(f"📦 {package['name']}"):
                    st.write(f"**Files:** {', '.join(package['files'])}")
                    st.write(f"**Description:** {package['description']}")

    with class_tab:
        st.subheader("Class Documentation")
        if documentation['classes']:
            for class_doc in documentation['classes']:
                with st.expander(f"🔷 {class_doc['name']}"):
                    st.write(f"**Package:** {class_doc['package']}")
                    st.write(f"**File:** {class_doc['file']}")

                    if class_doc['extends']:
                        st.write(f"**Extends:** `{class_doc['extends']}`")

                    if class_doc['implements']:
                        st.write(f"**Implements:** {', '.join(f'`{impl}`' for impl in class_doc['implements'])}")

                    st.markdown("---")
                    st.markdown(format_javadoc(class_doc['javadoc']))

    with method_tab:
        st.subheader("Method Documentation")
        if documentation['methods']:
            # Group methods by class
            methods_by_class = {}
            for method in documentation['methods']:
                class_name = method['class']
                if class_name not in methods_by_class:
                    methods_by_class[class_name] = []
                methods_by_class[class_name].append(method)

            # Display methods grouped by class
            for class_name, methods in methods_by_class.items():
                st.markdown(f"### 📘 {class_name}")
                for method in methods:
                    with st.expander(f"🔸 {method['name']}"):
                        # Method signature
                        signature = f"{' '.join(method['modifiers'])} {method['return_type']} {method['name']}"
                        if method['parameters']:
                            params = [f"{param['type']} {param['name']}" for param in method['parameters']]
                            signature += f"({', '.join(params)})"
                        else:
                            signature += "()"

                        st.code(signature, language="java")

                        # Documentation
                        st.markdown(format_javadoc(method['javadoc']))

                        if method['annotations']:
                            st.markdown("**Annotations:**")
                            for annotation in method['annotations']:
                                st.code(f"@{annotation}", language="java")