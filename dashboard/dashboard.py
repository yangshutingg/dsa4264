import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Set page config
st.set_page_config(
    page_title="Reddit Toxicity Analysis",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("Reddit Toxicity Analysis Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
time_range = st.sidebar.selectbox(
    "Time Range",
    ["Last 6 months", "Last 1 year", "Last 2 years", "All time"]
)
subreddit = st.sidebar.multiselect(
    "Subreddit",
    ["r/Singapore", "r/SingaporeRaw", "r/SingaporeHappenings"],
    default=["r/Singapore"]
)

# Create three columns for metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Overall Toxicity Trend",
        value="+23%",
        delta="2.1%"
    )

with col2:
    st.metric(
        label="Most Active Topics",
        value="Politics",
        delta="34% of discussions"
    )

with col3:
    st.metric(
        label="High Risk Topics",
        value="3 detected",
        delta="Foreign Policy, Race Relations, COVID"
    )

# Tabs using streamlit
tab1, tab2, tab3 = st.tabs(["Timeline Analysis", "Topic Analysis", "Correlation Analysis"])

with tab1:
    st.subheader("Toxicity Over Time")
    # Sample data - replace with your actual data
    dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='M')
    data = pd.DataFrame({
        'date': dates,
        'toxicity_score': np.random.rand(len(dates)) * 0.5 + 0.2,
        'political_posts': np.random.randint(100, 200, size=len(dates))
    })
    
    # Create line chart using plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['toxicity_score'],
        name='Toxicity Score'
    ))
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['political_posts']/1000,
        name='Political Posts (K)',
        yaxis='y2'
    ))
    
    fig.update_layout(
        title='Toxicity Score vs Political Posts',
        yaxis=dict(title='Toxicity Score'),
        yaxis2=dict(title='Political Posts (K)', overlaying='y', side='right')
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Topic Distribution")
    # Add your topic analysis visualizations here
    
with tab3:
    st.subheader("Correlation Analysis")
    # Add your correlation analysis visualizations here

# Additional sections can be added below
st.header("Key Insights")
with st.expander("See detailed insights"):
    st.write("""
    1. Political discussions show highest correlation with toxic comments
    2. Weekday evenings show peak toxicity levels
    3. Certain topics consistently trigger negative responses
    """)