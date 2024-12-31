import os
import streamlit as st
import pandas as pd
import google.generativeai as genai
import plotly.express as px
from dotenv import load_dotenv

# Load environment variables and configure API
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

class ProjectAnalytics:
    def __init__(self, df):
        self.df = df
        self.model = model

    def analyze_timeline(self, project_id):
        project_data = self.df[self.df['Project_ID'] == project_id]
        
        prompt = f"""
        Analyze this project timeline data:
        Tasks: {project_data['Task_Name'].tolist()}
        Estimated Days: {project_data['Estimated_Days'].tolist()}
        Actual Days: {project_data['Actual_Days'].tolist()}
        
        Provide:
        1. Timeline prediction based on historical data
        2. Potential delays and bottlenecks
        3. Schedule optimization suggestions
        """
        
        response = self.model.generate_content(prompt)
        return response.text

    def optimize_resources(self, project_id):
        project_data = self.df[self.df['Project_ID'] == project_id]
        
        prompt = f"""
        Analyze resource data:
        Resources: {project_data['Resource_Allocated'].tolist()}
        Efficiency: {project_data['Efficiency'].tolist()}
        Idle Time: {project_data['Idle_Time'].tolist()}
        
        Provide:
        1. Resource utilization recommendations
        2. How to minimize idle time
        3. Efficiency improvement suggestions
        """
        
        response = self.model.generate_content(prompt)
        return response.text

    def assess_risks(self, project_id):
        project_data = self.df[self.df['Project_ID'] == project_id]
        
        prompt = f"""
        Analyze project risks:
        Risk Types: {project_data['Risk_Type'].tolist()}
        Likelihood: {project_data['Likelihood'].tolist()}
        Impact: {project_data['Impact_Level'].tolist()}
        
        Provide:
        1. Risk assessment summary
        2. Mitigation strategies
        3. Priority recommendations
        """
        
        response = self.model.generate_content(prompt)
        return response.text

def load_data():
    try:
        df = pd.read_csv('project_data.csv')
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def main():
    st.title("Project Management Analytics")
    
    df = load_data()
    if df is None:
        st.stop()
    
    analytics = ProjectAnalytics(df)
    
    analysis_type = st.sidebar.selectbox(
        "Select Analysis",
        ["Predictive Scheduling", "Resource Optimization", "Risk Assessment"]
    )
    
    selected_project = st.selectbox("Select Project", df['Project_ID'].unique())
    
    if analysis_type == "Predictive Scheduling":
        st.header("Predictive Scheduling")
        if st.button("Analyze Timeline"):
            with st.spinner("Analyzing..."):
                # Timeline visualization
                project_df = df[df['Project_ID'] == selected_project]
                fig = px.bar(project_df, 
                           x='Task_Name',
                           y=['Estimated_Days', 'Actual_Days'],
                           title="Task Duration Analysis",
                           barmode='group')
                st.plotly_chart(fig)
                
                # AI Analysis
                analysis = analytics.analyze_timeline(selected_project)
                st.subheader("AI Insights")
                st.write(analysis)
    
    elif analysis_type == "Resource Optimization":
        st.header("Resource Optimization")
        if st.button("Optimize Resources"):
            with st.spinner("Analyzing..."):
                project_df = df[df['Project_ID'] == selected_project]
                
                # Resource efficiency visualization
                fig = px.scatter(project_df,
                               x='Efficiency',
                               y='Idle_Time',
                               color='Resource_Allocated',
                               title="Resource Utilization Analysis")
                st.plotly_chart(fig)
                
                # AI Recommendations
                optimization = analytics.optimize_resources(selected_project)
                st.subheader("Optimization Recommendations")
                st.write(optimization)
    
    else:  # Risk Assessment
        st.header("Risk Assessment")
        if st.button("Assess Risks"):
            with st.spinner("Analyzing..."):
                project_df = df[df['Project_ID'] == selected_project]
                
                # Risk matrix
                fig = px.scatter(project_df,
                               x='Likelihood',
                               y='Impact_Level',
                               color='Risk_Type',
                               title="Risk Matrix")
                st.plotly_chart(fig)
                
                # AI Risk Analysis
                risk_analysis = analytics.assess_risks(selected_project)
                st.subheader("Risk Assessment")
                st.write(risk_analysis)

if __name__ == "__main__":
    main()