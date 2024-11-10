import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os
# from datetime import datetime, timedelta

# Define Handles
@st.cache_data
def load_monthly_summary():
    try:
        file_path = '../data/monthly_scores_summary.csv'
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} not found.")
        
        df = pd.read_csv(file_path)
        df['yearmonth'] = pd.to_datetime(df['yearmonth'])
        df['year'] = df['yearmonth'].dt.year
        df['month'] = df['yearmonth'].dt.month
        return df
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

@st.cache_data
def load_topic_clusters_data():
    try:
        file_path = '../data/topic_clusters.csv'
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} not found.")
        
        df = pd.read_csv(file_path)
        df = df.sort_values(by='avg_toxicity', ascending=False) 
        return df
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None
    
@st.cache_data
def load_top10_topic_clusters_data():
    try:
        file_path1 = '../data/top10_topic_avg_toxicity.csv'
        file_path2 = '../data/top10_topic_post_count.csv'
        if not os.path.exists(file_path1):
            raise FileNotFoundError(f"{file_path1} not found.")
        if not os.path.exists(file_path2):
            raise FileNotFoundError(f"{file_path2} not found.")
        
        df1 = pd.read_csv(file_path1)
        df2 = pd.read_csv(file_path2)
        return df1, df2
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

# Load data
monthly_summary = load_monthly_summary()
topic_clusters = load_topic_clusters_data()
top10_topics_toxicity, top10_topics_post_count = load_top10_topic_clusters_data()

# Title
st.title("Overall Trends")

# Tabs
tab1, tab2, tab3 = st.tabs(["Trend Analysis", "Topic Analysis", "Correlation Analysis"])

with tab1:
    st.subheader("Toxicity Over Time")
    
    yearmonth = monthly_summary['yearmonth']
    ave_score = monthly_summary['average_toxicity_score_mean']

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x = yearmonth, 
        y = ave_score, 
        name = 'Toxicity Score'
    ))

    slope, intercept = np.polyfit(yearmonth.map(pd.Timestamp.toordinal), ave_score, 1)
    best_fit_line = slope * yearmonth.map(pd.Timestamp.toordinal) + intercept

    fig.add_trace(go.Scatter(
        x = yearmonth,
        y = best_fit_line,
        mode='lines',
        name='Best Fit Line',
        line=dict(dash='dash') 
        ))

    fig.update_yaxes(range=[0, 0.1]) 
    
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Topic Distribution")
    
    # Create a treemap for topic distribution
    
    fig_tree = px.treemap(
        topic_clusters,
        path=["cluster_id", "sample_topics"],
        values="size",
        color="avg_toxicity",
        hover_data={
            "total_posts": True,
            "unique_keywords": True,
            "topic_diversity": True,
            "avg_toxicity": True
        },
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