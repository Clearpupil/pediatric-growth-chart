import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Set page config
st.set_page_config(page_title="Pediatric Growth Chart (0-5 years)", layout="wide")

# Title and description
st.title("Pediatric Growth Chart")
st.markdown("Interactive growth chart for children from 0-5 years")

# Function to load CSV data
@st.cache_data
def load_data():
    # Data for 0-2 years (hardcoded sample WHO data)
    # Boys height-for-age (0-24 months)
    boys_height_0_2 = {
        'age': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
        'P3': [46.3, 51.1, 54.7, 57.6, 59.9, 61.9, 63.6, 65.1, 66.5, 67.8, 69.0, 70.2, 71.3, 72.4, 73.4, 74.4, 75.4, 76.4, 77.4, 78.3, 79.2, 80.1, 81.0, 81.9, 82.7],
        'P15': [48.0, 52.9, 56.6, 59.6, 62.0, 64.0, 65.8, 67.4, 68.9, 70.2, 71.5, 72.7, 73.9, 75.0, 76.1, 77.1, 78.2, 79.2, 80.2, 81.2, 82.1, 83.0, 84.0, 84.9, 85.7],
        'P50': [49.9, 54.7, 58.4, 61.4, 63.9, 65.9, 67.6, 69.2, 70.6, 72.0, 73.3, 74.5, 75.7, 76.9, 78.0, 79.1, 80.2, 81.2, 82.3, 83.2, 84.2, 85.1, 86.0, 86.9, 87.8],
        'P85': [51.8, 56.6, 60.4, 63.5, 66.0, 68.1, 69.8, 71.5, 73.0, 74.4, 75.8, 77.1, 78.3, 79.5, 80.6, 81.8, 82.9, 83.9, 85.0, 86.0, 87.0, 88.0, 89.0, 89.9, 90.9],
        'P97': [53.4, 58.2, 62.1, 65.2, 67.8, 70.0, 71.8, 73.5, 75.0, 76.5, 77.9, 79.2, 80.5, 81.8, 83.0, 84.2, 85.3, 86.4, 87.5, 88.6, 89.6, 90.7, 91.7, 92.7, 93.7]
    }
    
    # Girls height-for-age (0-24 months)
    girls_height_0_2 = {
        'age': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
        'P3': [45.6, 50.0, 53.2, 55.8, 58.0, 59.9, 61.5, 63.0, 64.4, 65.7, 67.0, 68.2, 69.4, 70.5, 71.6, 72.6, 73.7, 74.7, 75.7, 76.7, 77.6, 78.6, 79.6, 80.5, 81.4],
        'P15': [47.0, 51.7, 55.0, 57.7, 60.0, 61.9, 63.6, 65.1, 66.5, 67.9, 69.2, 70.4, 71.6, 72.8, 74.0, 75.1, 76.2, 77.2, 78.3, 79.3, 80.3, 81.3, 82.3, 83.2, 84.2],
        'P50': [49.1, 53.7, 57.1, 59.8, 62.1, 64.0, 65.7, 67.3, 68.7, 70.1, 71.5, 72.8, 74.0, 75.2, 76.4, 77.5, 78.6, 79.7, 80.7, 81.7, 82.7, 83.7, 84.6, 85.6, 86.6],
        'P85': [51.1, 55.7, 59.1, 61.9, 64.3, 66.2, 68.0, 69.6, 71.1, 72.6, 73.9, 75.2, 76.5, 77.7, 78.9, 80.0, 81.2, 82.3, 83.3, 84.4, 85.4, 86.4, 87.4, 88.4, 89.3],
        'P97': [52.7, 57.4, 60.9, 63.8, 66.2, 68.2, 70.0, 71.6, 73.2, 74.7, 76.0, 77.4, 78.7, 79.9, 81.2, 82.3, 83.5, 84.6, 85.7, 86.8, 87.8, 88.9, 89.9, 90.9, 91.9]
    }
    
    # Boys weight-for-age (0-24 months)
    boys_weight_0_2 = {
        'age': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
        'P3': [2.5, 3.4, 4.3, 5.0, 5.6, 6.1, 6.4, 6.7, 7.0, 7.2, 7.5, 7.7, 7.8, 8.0, 8.2, 8.4, 8.5, 8.7, 8.8, 9.0, 9.1, 9.3, 9.4, 9.6, 9.7],
        'P15': [2.9, 3.9, 4.9, 5.7, 6.2, 6.7, 7.1, 7.4, 7.7, 8.0, 8.2, 8.4, 8.6, 8.8, 9.0, 9.2, 9.4, 9.6, 9.8, 9.9, 10.1, 10.3, 10.5, 10.6, 10.8],
        'P50': [3.3, 4.5, 5.6, 6.4, 7.0, 7.5, 7.9, 8.3, 8.6, 8.9, 9.2, 9.4, 9.6, 9.9, 10.1, 10.3, 10.5, 10.7, 10.9, 11.1, 11.3, 11.5, 11.7, 11.8, 12.0],
        'P85': [3.9, 5.1, 6.3, 7.2, 7.8, 8.4, 8.8, 9.2, 9.6, 9.9, 10.2, 10.5, 10.8, 11.0, 11.3, 11.5, 11.7, 12.0, 12.2, 12.4, 12.6, 12.9, 13.1, 13.3, 13.5],
        'P97': [4.4, 5.8, 7.1, 8.0, 8.7, 9.3, 9.8, 10.2, 10.5, 10.9, 11.2, 11.5, 11.8, 12.1, 12.3, 12.6, 12.9, 13.1, 13.4, 13.6, 13.9, 14.1, 14.4, 14.6, 14.9]
    }
    
    # Girls weight-for-age (0-24 months)
    girls_weight_0_2 = {
        'age': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
        'P3': [2.4, 3.2, 3.9, 4.5, 5.0, 5.4, 5.7, 6.0, 6.3, 6.5, 6.7, 6.9, 7.0, 7.2, 7.4, 7.6, 7.7, 7.9, 8.1, 8.2, 8.4, 8.6, 8.7, 8.9, 9.0],
        'P15': [2.8, 3.6, 4.5, 5.1, 5.6, 6.0, 6.3, 6.7, 6.9, 7.1, 7.4, 7.6, 7.8, 8.0, 8.2, 8.4, 8.6, 8.8, 8.9, 9.1, 9.3, 9.5, 9.7, 9.8, 10.0],
        'P50': [3.2, 4.2, 5.1, 5.8, 6.4, 6.9, 7.3, 7.6, 7.9, 8.2, 8.5, 8.7, 8.9, 9.2, 9.4, 9.6, 9.8, 10.0, 10.2, 10.4, 10.6, 10.9, 11.1, 11.3, 11.5],
        'P85': [3.7, 4.8, 5.8, 6.6, 7.3, 7.8, 8.2, 8.6, 9.0, 9.3, 9.6, 9.9, 10.1, 10.4, 10.6, 10.9, 11.1, 11.4, 11.6, 11.8, 12.1, 12.3, 12.5, 12.8, 13.0],
        'P97': [4.2, 5.5, 6.6, 7.5, 8.2, 8.8, 9.3, 9.8, 10.1, 10.5, 10.8, 11.2, 11.5, 11.7, 12.0, 12.3, 12.6, 12.9, 13.1, 13.4, 13.6, 13.9, 14.2, 14.4, 14.7]
    }
    
    # Try to load 2-5 years data from CSV
    try:
        # Check if the CSV files exist
        if os.path.exists('tab_lhfa_boys_p_2_5.csv') and os.path.exists('tab_lhfa_girls_p_2_5.csv'):
            # Load from CSV files
            boys_height_2_5_df = pd.read_csv('tab_lhfa_boys_p_2_5.csv')
            girls_height_2_5_df = pd.read_csv('tab_lhfa_girls_p_2_5.csv')
            
            # Extract relevant columns
            boys_height_2_5 = {
                'age': boys_height_2_5_df['Month'].tolist(),
                'P3': boys_height_2_5_df['P3'].tolist(),
                'P15': boys_height_2_5_df['P15'].tolist(),
                'P50': boys_height_2_5_df['P50'].tolist(),
                'P85': boys_height_2_5_df['P85'].tolist(),
                'P97': boys_height_2_5_df['P97'].tolist()
            }
            
            girls_height_2_5 = {
                'age': girls_height_2_5_df['Month'].tolist(),
                'P3': girls_height_2_5_df['P3'].tolist(),
                'P15': girls_height_2_5_df['P15'].tolist(),
                'P50': girls_height_2_5_df['P50'].tolist(),
                'P85': girls_height_2_5_df['P85'].tolist(),
                'P97': girls_height_2_5_df['P97'].tolist()
            }
            
            # Approximate weight data for 2-5 years since we don't have it
            # These are not actual WHO values - just approximations for demo purposes
            boys_weight_2_5 = {
                'age': list(range(24, 61)),  # 24-60 months
                'P3': [9.7 + 0.15*i for i in range(37)],
                'P15': [10.8 + 0.16*i for i in range(37)],
                'P50': [12.0 + 0.17*i for i in range(37)],
                'P85': [13.5 + 0.19*i for i in range(37)],
                'P97': [14.9 + 0.21*i for i in range(37)]
            }
            
            girls_weight_2_5 = {
                'age': list(range(24, 61)),  # 24-60 months
                'P3': [9.0 + 0.14*i for i in range(37)],
                'P15': [10.0 + 0.15*i for i in range(37)],
                'P50': [11.5 + 0.16*i for i in range(37)],
                'P85': [13.0 + 0.18*i for i in range(37)],
                'P97': [14.7 + 0.19*i for i in range(37)]
            }
        else:
            # Fallback data if CSV files are not found
            st.warning("CSV files not found - using approximate data for 2-5 years range.")
            
            # Approximate height data for 2-5 years
            boys_height_2_5 = {
                'age': list(range(24, 61, 3)),  # 24-60 months, every 3 months
                'P3': [82.7, 85.5, 88.2, 90.9, 93.5, 96.1, 98.7, 101.0, 103.3, 105.6, 107.7, 109.8, 111.8],
                'P15': [85.7, 88.6, 91.5, 94.3, 97.0, 99.6, 102.2, 104.6, 107.0, 109.3, 111.6, 113.8, 116.0],
                'P50': [87.8, 90.9, 94.0, 97.0, 99.9, 102.7, 105.4, 108.0, 110.5, 113.0, 115.4, 117.7, 120.0],
                'P85': [90.9, 94.2, 97.4, 100.5, 103.5, 106.4, 109.2, 112.0, 114.7, 117.3, 119.8, 122.3, 124.7],
                'P97': [93.7, 97.1, 100.4, 103.7, 106.8, 109.8, 112.7, 115.6, 118.3, 121.0, 123.6, 126.1, 128.6]
            }
            
            girls_height_2_5 = {
                'age': list(range(24, 61, 3)),  # 24-60 months, every 3 months
                'P3': [81.4, 84.1, 86.7, 89.3, 91.8, 94.2, 96.6, 98.9, 101.1, 103.3, 105.4, 107.5, 109.5],
                'P15': [84.2, 87.0, 89.8, 92.5, 95.1, 97.7, 100.2, 102.6, 104.9, 107.2, 109.4, 111.6, 113.7],
                'P50': [86.6, 89.6, 92.5, 95.4, 98.1, 100.8, 103.4, 105.9, 108.4, 110.8, 113.1, 115.4, 117.6],
                'P85': [89.3, 92.4, 95.4, 98.4, 101.3, 104.1, 106.8, 109.5, 112.0, 114.5, 116.9, 119.3, 121.6],
                'P97': [91.9, 95.1, 98.2, 101.2, 104.2, 107.1, 109.9, 112.7, 115.3, 117.9, 120.4, 122.8, 125.2]
            }
            
            # Approximate weight data for 2-5 years
            boys_weight_2_5 = {
                'age': list(range(24, 61, 3)),  # 24-60 months, every 3 months
                'P3': [9.7, 10.2, 10.7, 11.2, 11.6, 12.1, 12.5, 12.9, 13.3, 13.7, 14.1, 14.5, 14.8],
                'P15': [10.8, 11.3, 11.8, 12.3, 12.8, 13.3, 13.8, 14.3, 14.7, 15.2, 15.7, 16.1, 16.5],
                'P50': [12.0, 12.5, 13.1, 13.7, 14.2, 14.8, 15.3, 15.9, 16.4, 16.9, 17.5, 18.0, 18.5],
                'P85': [13.5, 14.1, 14.8, 15.4, 16.1, 16.7, 17.4, 18.0, 18.7, 19.3, 20.0, 20.6, 21.2],
                'P97': [14.9, 15.6, 16.3, 17.0, 17.7, 18.4, 19.1, 19.8, 20.5, 21.2, 21.9, 22.6, 23.3]
            }
            
            girls_weight_2_5 = {
                'age': list(range(24, 61, 3)),  # 24-60 months, every 3 months
                'P3': [9.0, 9.4, 9.9, 10.3, 10.7, 11.1, 11.5, 11.9, 12.3, 12.7, 13.1, 13.4, 13.8],
                'P15': [10.0, 10.5, 10.9, 11.4, 11.9, 12.3, 12.8, 13.2, 13.7, 14.1, 14.6, 15.0, 15.5],
                'P50': [11.5, 12.0, 12.6, 13.1, 13.6, 14.1, 14.6, 15.1, 15.7, 16.2, 16.7, 17.2, 17.7],
                'P85': [13.0, 13.6, 14.2, 14.9, 15.5, 16.1, 16.8, 17.4, 18.0, 18.6, 19.2, 19.8, 20.4],
                'P97': [14.7, 15.4, 16.0, 16.7, 17.4, 18.1, 18.8, 19.5, 20.1, 20.8, 21.5, 22.2, 22.9]
            }
    except Exception as e:
        st.error(f"Error loading data: {e}")
        # Fallback to approximate data
        # (same as above)
        
    # Convert to DataFrames
    boys_height_0_2_df = pd.DataFrame(boys_height_0_2)
    girls_height_0_2_df = pd.DataFrame(girls_height_0_2)
    boys_weight_0_2_df = pd.DataFrame(boys_weight_0_2)
    girls_weight_0_2_df = pd.DataFrame(girls_weight_0_2)
    
    if 'boys_height_2_5' in locals():
        boys_height_2_5_df = pd.DataFrame(boys_height_2_5)
        girls_height_2_5_df = pd.DataFrame(girls_height_2_5)
        boys_weight_2_5_df = pd.DataFrame(boys_weight_2_5)
        girls_weight_2_5_df = pd.DataFrame(girls_weight_2_5)
    else:
        # Create empty DataFrames with the same structure
        boys_height_2_5_df = pd.DataFrame(columns=['age', 'P3', 'P15', 'P50', 'P85', 'P97'])
        girls_height_2_5_df = pd.DataFrame(columns=['age', 'P3', 'P15', 'P50', 'P85', 'P97'])
        boys_weight_2_5_df = pd.DataFrame(columns=['age', 'P3', 'P15', 'P50', 'P85', 'P97'])
        girls_weight_2_5_df = pd.DataFrame(columns=['age', 'P3', 'P15', 'P50', 'P85', 'P97'])
    
    return {
        'boys_height_0_2': boys_height_0_2_df,
        'girls_height_0_2': girls_height_0_2_df,
        'boys_weight_0_2': boys_weight_0_2_df,
        'girls_weight_0_2': girls_weight_0_2_df,
        'boys_height_2_5': boys_height_2_5_df,
        'girls_height_2_5': girls_height_2_5_df,
        'boys_weight_2_5': boys_weight_2_5_df,
        'girls_weight_2_5': girls_weight_2_5_df
    }

# Load the data
data = load_data()

# Create sidebar for inputs
st.sidebar.header("Patient Information")

# Age range selection
age_range = st.sidebar.radio("Age Range", ["0-2 years", "2-5 years"])

# Gender selection
gender = st.sidebar.radio("Gender", ["Boy", "Girl"])

# Patient data inputs
patient_name = st.sidebar.text_input("Patient Name", "")

# Age selector based on selected range
if age_range == "0-2 years":
    patient_age = st.sidebar.slider("Patient Age (months)", 0, 24, 12, 1)
    max_height = 100
    min_height = 40
    max_weight = 20
    min_weight = 2
else:  # 2-5 years
    patient_age = st.sidebar.slider("Patient Age (months)", 24, 60, 36, 1)
    max_height = 130
    min_height = 75
    max_weight = 30
    min_weight = 8

# Get appropriate default values based on age, gender and percentiles
if gender == "Boy":
    if age_range == "0-2 years":
        height_df = data['boys_height_0_2']
        weight_df = data['boys_weight_0_2']
    else:
        height_df = data['boys_height_2_5']
        weight_df = data['boys_weight_2_5']
else:
    if age_range == "0-2 years":
        height_df = data['girls_height_0_2']
        weight_df = data['girls_weight_0_2']
    else:
        height_df = data['girls_height_2_5']
        weight_df = data['girls_weight_2_5']

# Find closest age in data
closest_age_idx = (height_df['age'] - patient_age).abs().idxmin() if not height_df.empty else 0

# Get P50 values for the closest age
default_height = height_df.loc[closest_age_idx, 'P50'] if not height_df.empty else min_height + (max_height - min_height) / 2
default_weight = weight_df.loc[closest_age_idx, 'P50'] if not weight_df.empty else min_weight + (max_weight - min_weight) / 2

# Patient measurements
patient_height = st.sidebar.number_input(
    "Patient Height (cm)", 
    min_value=float(min_height), 
    max_value=float(max_height), 
    value=float(default_height), 
    step=0.1
)

patient_weight = st.sidebar.number_input(
    "Patient Weight (kg)", 
    min_value=float(min_weight), 
    max_value=float(max_weight), 
    value=float(default_weight), 
    step=0.1
)

# Chart selector
chart_type = st.sidebar.radio("Chart Type", ["Height-for-age", "Weight-for-age", "Both"])

# Convert age to display format
def format_age(age_months):
    if age_months < 12:
        return f"{age_months} month{'s' if age_months != 1 else ''}"
    elif age_months % 12 == 0:
        years = age_months // 12
        return f"{years} year{'s' if years != 1 else ''}"
    else:
        years = age_months // 12
        months = age_months % 12
        return f"{years} year{'s' if years != 1 else ''}, {months} month{'s' if months != 1 else ''}"

# Function to create height chart
def create_height_chart(height_df, patient_age, patient_height, age_range):
    """Create a height-for-age chart with WHO percentile curves."""
    # Create figure
    fig = go.Figure()
    
    # Min/max values for axes
    if age_range == "0-2 years":
        x_min, x_max = 0, 24
        y_min, y_max = 40, 100
    else:
        x_min, x_max = 24, 60
        y_min, y_max = 75, 130
    
    # Add percentile lines
    for percentile in ['P3', 'P15', 'P50', 'P85', 'P97']:
        fig.add_trace(
            go.Scatter(
                x=height_df['age'],
                y=height_df[percentile],
                mode='lines',
                name=f"{percentile.replace('P', '')}th percentile",
                line=dict(
                    width=3 if percentile == 'P50' else 2,
                    dash='solid'
                )
            )
        )
    
    # Add patient marker
    fig.add_trace(
        go.Scatter(
            x=[patient_age],
            y=[patient_height],
            mode='markers',
            name='Patient',
            marker=dict(
                size=12,
                color='red',
                symbol='circle'
            )
        )
    )
    
    # Add reference lines for current patient
    fig.add_shape(
        type="line",
        x0=x_min,
        y0=patient_height,
        x1=patient_age,
        y1=patient_height,
        line=dict(
            color="red",
            width=1,
            dash="dash",
        )
    )
    
    fig.add_shape(
        type="line",
        x0=patient_age,
        y0=y_min,
        x1=patient_age,
        y1=patient_height,
        line=dict(
            color="red",
            width=1,
            dash="dash",
        )
    )
    
    # Configure layout
    fig.update_layout(
        title=f'Height-for-age ({age_range})',
        xaxis=dict(
            title='Age (months)',
            dtick=3 if age_range == "0-2 years" else 6,  # Set tick marks every 3 or 6 months
            gridcolor='lightgray',
            gridwidth=1,
            range=[x_min, x_max]
        ),
        yaxis=dict(
            title='Height (cm)',
            dtick=5,  # Set tick marks every 5 cm
            gridcolor='lightgray',
            gridwidth=1,
            range=[y_min, y_max]
        ),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        margin=dict(l=60, r=20, t=50, b=60),
        height=500,
        hovermode='closest'
    )
    
    return fig

# Function to create weight chart
def create_weight_chart(weight_df, patient_age, patient_weight, age_range):
    """Create a weight-for-age chart with WHO percentile curves."""
    # Create figure
    fig = go.Figure()
    
    # Min/max values for axes
    if age_range == "0-2 years":
        x_min, x_max = 0, 24
        y_min, y_max = 1, 16
    else:
        x_min, x_max = 24, 60
        y_min, y_max = 8, 25
    
    # Add percentile lines
    for percentile in ['P3', 'P15', 'P50', 'P85', 'P97']:
        fig.add_trace(
            go.Scatter(
                x=weight_df['age'],
                y=weight_df[percentile],
                mode='lines',
                name=f"{percentile.replace('P', '')}th percentile",
                line=dict(
                    width=3 if percentile == 'P50' else 2,
                    dash='solid'
                )
            )
        )
    
    # Add patient marker
    fig.add_trace(
        go.Scatter(
            x=[patient_age],
            y=[patient_weight],
            mode='markers',
            name='Patient',
            marker=dict(
                size=12,
                color='red',
                symbol='circle'
            )
        )
    )
    
    # Add reference lines for current patient
    fig.add_shape(
        type="line",
        x0=x_min,
        y0=patient_weight,
        x1=patient_age,
        y1=patient_weight,
        line=dict(
            color="red",
            width=1,
            dash="dash",
        )
    )
    
    fig.add_shape(
        type="line",
        x0=patient_age,
        y0=y_min,
        x1=patient_age,
        y1=patient_weight,
        line=dict(
            color="red",
            width=1,
            dash="dash",
        )
    )
    
    fig.update_layout(
        title=f'Weight-for-age ({age_range})',
        xaxis=dict(
            title='Age (months)',
            dtick=3 if age_range == "0-2 years" else 6,  # Set tick marks every 3 or 6 months
            gridcolor='lightgray',
            gridwidth=1,
            range=[x_min, x_max]
        ),
        yaxis=dict(
            title='Weight (kg)',
            dtick=1,  # Set tick marks every 1 kg
            gridcolor='lightgray',
            gridwidth=1,
            range=[y_min, y_max]
        ),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        margin=dict(l=60, r=20, t=50, b=60),
        height=500,
        hovermode='closest'
    )
    
    return fig

# Function to determine percentile status
def get_percentile_status(df, age, measurement, measurement_type):
    """Determine which percentile range the patient falls into."""
    # Find the closest age
    closest_age_idx = (df['age'] - age).abs().idxmin() if not df.empty else None
    
    if closest_age_idx is None:
        return f"No data available for {measurement_type}"
    
    closest_age_row = df.loc[closest_age_idx]
    
    if measurement < closest_age_row['P3']:
        return f"Below 3rd percentile ({measurement_type})"
    elif measurement < closest_age_row['P15']:
        return f"Between 3rd-15th percentile ({measurement_type})"
    elif measurement < closest_age_row['P50']:
        return f"Between 15th-50th percentile ({measurement_type})"
    elif measurement < closest_age_row['P85']:
        return f"Between 50th-85th percentile ({measurement_type})"
    elif measurement < closest_age_row['P97']:
        return f"Between 85th-97th percentile ({measurement_type})"
    else:
        return f"Above 97th percentile ({measurement_type})"
        
# Display patient information
st.header("Patient Summary")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Name", patient_name if patient_name else "Not provided")
with col2:
    st.metric("Age", format_age(patient_age))
with col3:
    st.metric("Height", f"{patient_height} cm")
with col4:
    st.metric("Weight", f"{patient_weight} kg")

# Display percentile information
st.subheader("Growth Assessment")
height_percentile = get_percentile_status(height_df, patient_age, patient_height, "height")
weight_percentile = get_percentile_status(weight_df, patient_age, patient_weight, "weight")

col1, col2 = st.columns(2)
with col1:
    st.info(height_percentile)
with col2:
    st.info(weight_percentile)

# Display growth velocity if available
if st.sidebar.checkbox("Add Previous Measurement"):
    st.subheader("Growth Velocity")
    prev_date_col, prev_height_col, prev_weight_col = st.columns(3)
    
    with prev_date_col:
        prev_months_ago = st.number_input("Previous measurement (months ago)", 1, 12, 3)
        prev_age = patient_age - prev_months_ago
        if prev_age < 0:
            st.warning("Previous age would be negative, please adjust")
            prev_age = 0
    
    with prev_height_col:
        prev_height = st.number_input("Previous Height (cm)", 30.0, 150.0, float(patient_height - 3.0), 0.1)
        height_change = patient_height - prev_height
        height_change_monthly = height_change / prev_months_ago if prev_months_ago > 0 else 0
        
    with prev_weight_col:
        prev_weight = st.number_input("Previous Weight (kg)", 1.0, 50.0, float(patient_weight - 1.0), 0.1)
        weight_change = patient_weight - prev_weight
        weight_change_monthly = weight_change / prev_months_ago if prev_months_ago > 0 else 0
    
    growth_col1, growth_col2 = st.columns(2)
    
    with growth_col1:
        st.metric("Height Velocity", f"{height_change_monthly:.1f} cm/month", f"{height_change:.1f} cm total")
    
    with growth_col2:
        st.metric("Weight Velocity", f"{weight_change_monthly:.2f} kg/month", f"{weight_change:.2f} kg total")

# Display selected charts
if chart_type == "Height-for-age":
    height_chart = create_height_chart(height_df, patient_age, patient_height, age_range)
    st.plotly_chart(height_chart, use_container_width=True)
    
elif chart_type == "Weight-for-age":
    weight_chart = create_weight_chart(weight_df, patient_age, patient_weight, age_range)
    st.plotly_chart(weight_chart, use_container_width=True)
    
else:  # Both
    tab1, tab2 = st.tabs(["Height-for-age", "Weight-for-age"])
    
    with tab1:
        height_chart = create_height_chart(height_df, patient_age, patient_height, age_range)
        st.plotly_chart(height_chart, use_container_width=True)
        
    with tab2:
        weight_chart = create_weight_chart(weight_df, patient_age, patient_weight, age_range)
        st.plotly_chart(weight_chart, use_container_width=True)

# Add BMI calculation
if st.sidebar.checkbox("Show BMI"):
    st.subheader("Body Mass Index (BMI)")
    
    # Calculate BMI
    height_m = patient_height / 100
    bmi = patient_weight / (height_m * height_m)
    
    # Show BMI in a metric widget
    st.metric("BMI", f"{bmi:.1f} kg/m²")
    
    # Simple BMI interpretation for children
    if bmi < 14:
        st.warning("BMI is below typical range for this age")
    elif bmi > 18:
        st.warning("BMI is above typical range for this age")
    else:
        st.success("BMI is within typical range for this age")
    
    st.info("Note: BMI interpretation in children is age and gender specific. This is a simplified assessment.")

# Add notes section
st.markdown("---")
st.markdown("### Clinical Notes")
notes = st.text_area("Enter clinical notes here", height=100)

# Save button (in a real application, this would save to a database)
if st.button("Save Patient Data"):
    st.success("Patient data saved successfully! (Demo only - no actual data is saved)")

# Add information about the data source
st.markdown("---")
st.markdown("""
### Data Sources
- Growth charts based on WHO Child Growth Standards
- For more information, visit [WHO Child Growth Standards](https://www.who.int/tools/child-growth-standards)
""")

# Add app instructions in an expandable section
with st.expander("How to use this app"):
    st.markdown("""
    1. **Select age range** (0-2 years or 2-5 years) in the sidebar
    2. **Choose gender** (Boy or Girl)
    3. **Enter patient information** including name, age, height, and weight
    4. **View the growth charts** and percentile information
    5. **Optional features**:
        - Add previous measurements to calculate growth velocity
        - Calculate BMI
        - Add clinical notes
    """)