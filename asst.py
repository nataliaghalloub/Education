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
    return pd.read_csv('C:/Users/User/Desktop/325 V/Assigments/A1/education level.csv')

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
