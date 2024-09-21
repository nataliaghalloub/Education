import streamlit as st
import pandas as pd
import plotly.express as px

# Title for the app
st.title("Interactive Educational Insights for Lebanese Towns")

# Sidebar for navigation
page = st.sidebar.selectbox("Select a page:", ["Introduction", "Visualizations"])

# Load the dataset
@st.cache_data  # Changed to st.cache_data to avoid deprecation warning
def load_data():
    return pd.read_csv('education level.csv')

data = load_data()

# Page 1: Introduction
if page == "Introduction":
    st.header("Introduction")
    
    # Brief description
    st.subheader("Explore Educational Data Across Lebanese Towns")
    st.write("""
        This app provides interactive insights into the educational levels across various towns in Lebanon.
        You will be able to explore university education levels, school dropout rates, and other educational metrics 
        across regions. The following pages will allow you to interact with the data through visualizations.
    """)
        # Explanation of the Visualizations
    st.subheader("Description of Visualizations")
    
    st.write("""
        **1. Stacked Bar Chart: "Top 10 Towns by Selected Education Levels"**
        
        - **Goal**: This chart helps users explore the top towns with the highest levels of university-educated residents, along with other educational categories such as secondary, intermediate, elementary, and vocational education. 
        It provides a comparative view of how the selected educational levels are distributed among the top towns.
        
        - **Interactivity**: 
          - Users can **select the number of top towns** to display (from 5 to 20).
          - Users can also **choose specific educational levels** to visualize in the chart, such as university, secondary, or vocational education. 
          - The stacked bar chart allows users to compare the education levels within each town side by side.
        
        **2. Pie Chart: "Education Levels Distribution in Selected Town"**
        
        - **Goal**: This visualization provides a detailed breakdown of the education levels within a specific town. Users can focus on individual towns and see the proportional distribution of education categories (such as intermediate, university, or elementary).
        
        - **Interactivity**:
          - Users can **select a specific town** from the dropdown list, and the pie chart updates to display the education level distribution for that town. This provides a detailed view, complementing the broader overview provided by the bar chart.
    """)
    # Display dataset information
    st.write("Here is a preview of the dataset used:")
    st.write(data.head())  # Show the first few rows of the dataset
    
    # Display the columns
    st.write("Dataset columns:", data.columns)

    # Author and class details
    st.subheader("Natalia Ghalloub, 202473645, MSBA 325 Class")

# Page 2: Visualizations
elif page == "Visualizations":
    st.header("Educational Visualizations for Lebanese Towns")

    st.write("Use the slider to explore towns with the highest percentage of university-educated residents.")
    
    # Allow the user to select the educational level(s) to display
    education_levels = st.multiselect(
        "Select the educational level(s) to display:",
        ['PercentageofEducationlevelofresidents-university',
         'PercentageofEducationlevelofresidents-secondary',
         'PercentageofEducationlevelofresidents-intermediate',
         'PercentageofEducationlevelofresidents-elementary',
         'PercentageofEducationlevelofresidents-vocational',
         'PercentageofEducationlevelofresidents-highereducation'],
        default=['PercentageofEducationlevelofresidents-university']  # Set default selection
    )

    # Add a slider to allow the user to choose the number of top towns to display
    num_towns = st.slider('Select number of top towns to display', 5, 20, 10)

    # Filter the top towns based on the number of university-educated residents
    top_towns = data.nlargest(num_towns, 'PercentageofEducationlevelofresidents-university')

    # Create a stacked bar chart for the selected educational levels
    fig = px.bar(top_towns, x='Town',
                 y=education_levels,
                 title=f'Top {num_towns} Towns by Selected Education Levels',
                 labels={'value': 'Percentage of Residents (%)', 'variable': 'Educational Level'},
                 barmode='stack')

    # Adjust layout for better readability
    fig.update_layout(xaxis_tickangle=-45, height=600, width=1000)

    # Display the bar chart in Streamlit
    st.plotly_chart(fig)

    # Create a list of towns for selection
    towns = data['Town'].unique()

    # Allow the user to select a town
    selected_town = st.selectbox('Select a Town to visualize its education levels:', towns)

    # Filter the data for the selected town
    town_data = data[data['Town'] == selected_town].iloc[0]

    # Create the pie chart for the selected town
    fig = px.pie(
        names=['Illiterate', 'University', 'Secondary', 'Intermediate', 'Vocational', 'Elementary', 'Higher Education'],
        values=[town_data['PercentageofEducationlevelofresidents-illeterate'], 
                town_data['PercentageofEducationlevelofresidents-university'],
                town_data['PercentageofEducationlevelofresidents-secondary'],
                town_data['PercentageofEducationlevelofresidents-intermediate'],
                town_data['PercentageofEducationlevelofresidents-vocational'],
                town_data['PercentageofEducationlevelofresidents-elementary'],
                town_data['PercentageofEducationlevelofresidents-highereducation']],
        title=f'Education Levels Distribution in {selected_town}'
    )

    # Display the pie chart in Streamlit
    st.plotly_chart(fig)
