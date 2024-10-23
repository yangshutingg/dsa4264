import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate sample data for demonstration
@st.cache_data
def generate_sample_data():
    # Date range
    dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='M')
    
    # Sample topics
    topics = ['Politics', 'Housing', 'Education', 'COVID', 'Economy', 'Transportation']
    
    # Create sample data
    data = pd.DataFrame({
        'date': dates,
        'toxicity_score': np.random.rand(len(dates)) * 0.5 + 0.2,
        'political_posts': np.random.randint(100, 200, size=len(dates)),
        'total_posts': np.random.randint(500, 1000, size=len(dates))
    })
    
    # Create topic distribution
    topic_data = pd.DataFrame({
        'topic': topics,
        'percentage': np.random.dirichlet(np.ones(len(topics))) * 100,
        'toxicity': np.random.rand(len(topics)) * 0.5 + 0.2
    })
    
    return data, topic_data

# Load sample data
data, topic_data = generate_sample_data()

# Title is already set in Home.py
st.title("Overview Dashboard")

# Sidebar filters
st.sidebar.header("Filters")

# Time range filter
# Modify the time range selection part
# Instead of setting session state after selection, initialize it first

# Initialize session state if needed
if 'time_range' not in st.session_state:
    st.session_state['time_range'] = "Last 1 year"
if 'subreddits' not in st.session_state:
    st.session_state['subreddits'] = ["r/Singapore"]

# Use session state in the selectbox
time_range = st.sidebar.selectbox(
    "Time Range",
    ["Last 6 months", "Last 1 year", "Last 2 years", "All time"],
    index=["Last 6 months", "Last 1 year", "Last 2 years", "All time"].index(st.session_state['time_range'])
)

# Update session state through callback
if time_range != st.session_state['time_range']:
    st.session_state['time_range'] = time_range

# Similarly for subreddit selection
subreddit = st.sidebar.multiselect(
    "Subreddit",
    ["r/Singapore", "r/SingaporeRaw", "r/SingaporeHappenings"],
    default=st.session_state['subreddits']
)

if subreddit != st.session_state['subreddits']:
    st.session_state['subreddits'] = subreddit

# Store in session state for other pages
st.session_state['time_range'] = time_range


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
        yaxis2=dict(title='Posts (K)', overlaying='y', side='right')
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Topic Distribution")
    
    # Create a treemap for topic distribution
    fig_tree = px.treemap(
        topic_data,
        path=['topic'],
        values='percentage',
        color='toxicity',
        color_continuous_scale='RdYlBu_r',
        title='Topic Distribution and Toxicity'
    )
    st.plotly_chart(fig_tree, use_container_width=True)

with tab3:
    st.subheader("Correlation Analysis")
    
    # Create correlation heatmap
    correlation_data = pd.DataFrame({
        'Toxicity': np.random.rand(100),
        'Post Length': np.random.rand(100),
        'Comments': np.random.rand(100),
        'Time of Day': np.random.rand(100)
    })
    
    fig_corr = px.imshow(
        correlation_data.corr(),
        title='Feature Correlations',
        color_continuous_scale='RdBu'
    )
    st.plotly_chart(fig_corr, use_container_width=True)

# Key Insights section
st.header("Key Insights")
with st.expander("See detailed insights"):
    st.write("""
    1. Political discussions show highest correlation with toxic comments
    2. Weekday evenings show peak toxicity levels
    3. Certain topics consistently trigger negative responses
    """)

# Add a link to the detailed analysis
st.sidebar.markdown("---")
st.sidebar.markdown("👉 Check out the [Detailed Analysis](/Detailed_Analysis) for more insights!")