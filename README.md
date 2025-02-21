# Java Code Analyzer

A comprehensive Java code analysis tool built with Streamlit that provides advanced visualization and documentation capabilities for software developers.

## Developer
Developed by Ullas

## Description
This tool helps developers analyze Java projects by providing:
- Interactive UML class diagrams
- Class relationship visualization
- API endpoint documentation
- Code documentation analysis
- Project structure visualization

## Installation Steps
1. **Environment Setup**
   - Make sure you have Python 3.8 or higher installed
   - Required Python packages: `streamlit`, `javalang`, `plantuml`, `networkx`, `pandas`, `plotly`
   - Install dependencies using: 
     ```bash
     pip install streamlit javalang plantuml networkx pandas plotly
     ```

2. **Running the Application**
   - Clone the repository
   - Navigate to the project directory
   - Run: `streamlit run java_analyzer.py`
   - Access the application at `http://localhost:5000`

## Usage Instructions
1. **File Upload**
   - Upload individual `.java` files or
   - Upload a `.zip` file containing your Java project
   - The analyzer supports both single files and complete projects

2. **Available Features**
   - **Project Structure**: View hierarchical file organization
   - **Class Relationships**: Analyze inheritance and dependencies
   - **Data Flow**: Examine API endpoints and data connections
   - **UML Diagram**: Interactive class diagrams with zoom
   - **Documentation**: Browse Javadoc with quality metrics

3. **Best Practices**
   - Ensure Java files have proper package declarations
   - Include Javadoc comments for better documentation analysis
   - For large projects, use ZIP upload for better organization

## Key Technologies
- Streamlit web interface
- PlantUML for diagram generation
- Local Javadoc parsing
- Interactive code visualization components
- NLP-powered documentation extraction

## Features
1. **Project Structure Analysis**
   - Hierarchical file view
   - File statistics and metrics
   - Package organization

2. **Class Relationship Visualization**
   - Inheritance hierarchies
   - Interface implementations
   - Dependency graphs

3. **API Documentation**
   - REST endpoint detection
   - SOAP service documentation
   - Parameter analysis

4. **Code Documentation Analysis**
   - Javadoc coverage metrics
   - Documentation quality assessment
   - Method and class documentation

5. **UML Visualization**
   - Interactive class diagrams
   - Relationship mapping
   - Customizable views
