import streamlit as st
import pandas as pd
from typing import Dict

def show_data_flow(relationships: Dict):
    """
    Display data flow information including API endpoints
    """
    st.header("Data Flow Analysis")

    # Show associations
    st.subheader("Class Associations")
    if relationships['associations']:
        df_associations = pd.DataFrame(relationships['associations'])
        st.dataframe(df_associations)
    else:
        st.info("No associations found")

    # Show dependencies
    st.subheader("Dependencies")
    if relationships['dependencies']:
        dependencies_list = [{"from": dep[0], "to": dep[1]} 
                           for dep in relationships['dependencies']]
        df_dependencies = pd.DataFrame(dependencies_list)
        st.dataframe(df_dependencies)
    else:
        st.info("No dependencies found")

    # Show API Endpoints
    st.subheader("API Endpoints")

    # REST API Tab
    tab1, tab2 = st.tabs(["REST API Endpoints", "SOAP Services"])

    with tab1:
        rest_endpoints = []
        for file_data in relationships.get('parsed_data', {}).values():
            for class_info in file_data.get('classes', []):
                for api_method in class_info.get('api_methods', []):
                    if api_method['type'] == 'REST':
                        rest_endpoints.append({
                            'Class': class_info['name'],
                            'Endpoint': api_method['method'],
                            'HTTP Method': next((a for a in api_method['annotations'] 
                                               if a in ['GET', 'POST', 'PUT', 'DELETE']), 'N/A'),
                            'Parameters': ', '.join([f"{p['name']}: {p['type']}" 
                                                   for p in api_method['parameters']])
                        })

        if rest_endpoints:
            st.dataframe(pd.DataFrame(rest_endpoints))
        else:
            st.info("No REST endpoints found")

    with tab2:
        soap_services = []
        for file_data in relationships.get('parsed_data', {}).values():
            for class_info in file_data.get('classes', []):
                for api_method in class_info.get('api_methods', []):
                    if api_method['type'] == 'SOAP':
                        soap_services.append({
                            'Service Class': class_info['name'],
                            'Operation': api_method['method'],
                            'Parameters': ', '.join([f"{p['name']}: {p['type']}" 
                                                   for p in api_method['parameters']])
                        })

        if soap_services:
            st.dataframe(pd.DataFrame(soap_services))
        else:
            st.info("No SOAP services found")

    # Add metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Classes", 
                 len(set([rel['from'] for rel in relationships['associations']])))
    with col2:
        st.metric("Total Dependencies", 
                 len(relationships['dependencies']))
    with col3:
        st.metric("Total Relationships",
                 len(relationships['inheritance']) + 
                 len(relationships['implementation']))
    with col4:
        total_apis = len(rest_endpoints) + len(soap_services)
        st.metric("Total API Endpoints", total_apis)