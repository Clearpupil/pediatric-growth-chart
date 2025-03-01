import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page config
st.set_page_config(page_title="Pediatric Growth Chart", layout="wide")

# Title and description
st.title("Pediatric Growth Chart")
st.markdown("Interactive growth chart for infants from 0-24 months")

# Sample WHO data for boys height-for-age (0-24 months)
# Format: age in months, P3, P15, P50, P85, P97
boys_height_data = {
    'age': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
    'P3': [46.3, 51.1, 54.7, 57.6, 59.9, 61.9, 63.6, 65.1, 66.5, 67.8, 69.0, 70.2, 71.3, 72.4, 73.4, 74.4, 75.4, 76.4, 77.4, 78.3, 79.2, 80.1, 81.0, 81.9, 82.7],
    'P15': [48.0, 52.9, 56.6, 59.6, 62.0, 64.0, 65.8, 67.4, 68.9, 70.2, 71.5, 72.7, 73.9, 75.0, 76.1, 77.1, 78.2, 79.2, 80.2, 81.2, 82.1, 83.0, 84.0, 84.9, 85.7],
    'P50': [49.9, 54.7, 58.4, 61.4, 63.9, 65.9, 67.6, 69.2, 70.6, 72.0, 73.3, 74.5, 75.7, 76.9, 78.0, 79.1, 80.2, 81.2, 82.3, 83.2, 84.2, 85.1, 86.0, 86.9, 87.8],
    'P85': [51.8, 56.6, 60.4, 63.5, 66.0, 68.1, 69.8, 71.5, 73.0, 74.4, 75.8, 77.1, 78.3, 79.5, 80.6, 81.8, 82.9, 83.9, 85.0, 86.0, 87.0, 88.0, 89.0, 89.9, 90.9],
    'P97': [53.4, 58.2, 62.1, 65.2, 67.8, 70.0, 71.8, 73.5, 75.0, 76.5, 77.9, 79.2, 80.5, 81.8, 83.0, 84.2, 85.3, 86.4, 87.5, 88.6, 89.6, 90.7, 91.7, 92.7, 93.7]
}

# Sample WHO data for boys weight-for-age (0-24 months)
boys_weight_data = {
    'age': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
    'P3': [2.5, 3.4, 4.3, 5.0, 5.6, 6.1, 6.4, 6.7, 7.0, 7.2, 7.5, 7.7, 7.8, 8.0, 8.2, 8.4, 8.5, 8.7, 8.8, 9.0, 9.1, 9.3, 9.4, 9.6, 9.7],
    'P15': [2.9, 3.9, 4.9, 5.7, 6.2, 6.7, 7.1, 7.4, 7.7, 8.0, 8.2, 8.4, 8.6, 8.8, 9.0, 9.2, 9.4, 9.6, 9.8, 9.9, 10.1, 10.3, 10.5, 10.6, 10.8],
    'P50': [3.3, 4.5, 5.6, 6.4, 7.0, 7.5, 7.9, 8.3, 8.6, 8.9, 9.2, 9.4, 9.6, 9.9, 10.1, 10.3, 10.5, 10.7, 10.9, 11.1, 11.3, 11.5, 11.7, 11.8, 12.0],
    'P85': [3.9, 5.1, 6.3, 7.2, 7.8, 8.4, 8.8, 9.2, 9.6, 9.9, 10.2, 10.5, 10.8, 11.0, 11.3, 11.5, 11.7, 12.0, 12.2, 12.4, 12.6, 12.9, 13.1, 13.3, 13.5],
    'P97': [4.4, 5.8, 7.1, 8.0, 8.7, 9.3, 9.8, 10.2, 10.5, 10.9, 11.2, 11.5, 11.8, 12.1, 12.3, 12.6, 12.9, 13.1, 13.4, 13.6, 13.9, 14.1, 14.4, 14.6, 14.9]
}

# Convert to DataFrames
boys_height_df = pd.DataFrame(boys_height_data)
boys_weight_df = pd.DataFrame(boys_weight_data)

# Create sidebar for inputs
st.sidebar.header("Patient Information")

# Gender selection
gender = st.sidebar.radio("Gender", ["Boy", "Girl"])

# Patient data inputs
patient_name = st.sidebar.text_input("Patient Name", "")
patient_age = st.sidebar.slider("Patient Age (months)", 0, 24, 12, 1)
patient_height = st.sidebar.number_input("Patient Height (cm)", 40.0, 100.0, 75.7, 0.1)  # Default to P50 at 12 months
patient_weight = st.sidebar.number_input("Patient Weight (kg)", 2.0, 20.0, 9.6, 0.1)  # Default to P50 at 12 months

# Chart selector
chart_type = st.sidebar.radio("Chart Type", ["Height-for-age", "Weight-for-age", "Both"])

# Function to create height chart
def create_height_chart(height_df, patient_age, patient_height):
    # Create figure
    fig = go.Figure()
    
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
        x0=0,
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
        y0=40,
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
        title='Height-for-age (0-24 months)',
        xaxis=dict(
            title='Age (months)',
            dtick=1,  # Set tick marks every 1 month
            gridcolor='lightgray',
            gridwidth=1,
            range=[0, 24]
        ),
        yaxis=dict(
            title='Height (cm)',
            dtick=2,  # Set tick marks every 2 cm
            gridcolor='lightgray',
            gridwidth=1,
            range=[40, 100]
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
def create_weight_chart(weight_df, patient_age, patient_weight):
    fig = go.Figure()
    
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
        x0=0,
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
        y0=0,
        x1=patient_age,
        y1=patient_weight,
        line=dict(
            color="red",
            width=1,
            dash="dash",
        )
    )
    
    fig.update_layout(
        title='Weight-for-age (0-24 months)',
        xaxis=dict(
            title='Age (months)',
            dtick=1,  # Set tick marks every 1 month
            gridcolor='lightgray',
            gridwidth=1,
            range=[0, 24]
        ),
        yaxis=dict(
            title='Weight (kg)',
            dtick=1,  # Set tick marks every 1 kg
            gridcolor='lightgray',
            gridwidth=1,
            range=[2, 16]
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
    # Find the closest age
    closest_age_row = df.iloc[(df['age'] - age).abs().argsort()[:1]]
    
    if measurement < closest_age_row['P3'].values[0]:
        return f"Below 3rd percentile ({measurement_type})"
    elif measurement < closest_age_row['P15'].values[0]:
        return f"Between 3rd-15th percentile ({measurement_type})"
    elif measurement < closest_age_row['P50'].values[0]:
        return f"Between 15th-50th percentile ({measurement_type})"
    elif measurement < closest_age_row['P85'].values[0]:
        return f"Between 50th-85th percentile ({measurement_type})"
    elif measurement < closest_age_row['P97'].values[0]:
        return f"Between 85th-97th percentile ({measurement_type})"
    else:
        return f"Above 97th percentile ({measurement_type})"

# Display patient information
st.header("Patient Summary")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Name", patient_name if patient_name else "Not provided")
with col2:
    st.metric("Age", f"{patient_age} months")
with col3:
    st.metric("Height", f"{patient_height} cm")
with col4:
    st.metric("Weight", f"{patient_weight} kg")

# Display percentile information
st.subheader("Growth Assessment")
height_percentile = get_percentile_status(boys_height_df, patient_age, patient_height, "height")
weight_percentile = get_percentile_status(boys_weight_df, patient_age, patient_weight, "weight")

col1, col2 = st.columns(2)
with col1:
    st.info(height_percentile)
with col2:
    st.info(weight_percentile)

# Display selected charts
if chart_type == "Height-for-age":
    height_chart = create_height_chart(boys_height_df, patient_age, patient_height)
    st.plotly_chart(height_chart, use_container_width=True)
    
elif chart_type == "Weight-for-age":
    weight_chart = create_weight_chart(boys_weight_df, patient_age, patient_weight)
    st.plotly_chart(weight_chart, use_container_width=True)
    
else:  # Both
    tab1, tab2 = st.tabs(["Height-for-age", "Weight-for-age"])
    
    with tab1:
        height_chart = create_height_chart(boys_height_df, patient_age, patient_height)
        st.plotly_chart(height_chart, use_container_width=True)
        
    with tab2:
        weight_chart = create_weight_chart(boys_weight_df, patient_age, patient_weight)
        st.plotly_chart(weight_chart, use_container_width=True)

# Add notes section
st.markdown("---")
st.markdown("### Clinical Notes")
notes = st.text_area("Enter clinical notes here", height=100)

# Save button (in a real application, this would save to a database)
if st.button("Save Patient Data"):
    st.success("Patient data saved successfully! (Demo only - no actual data is saved)")