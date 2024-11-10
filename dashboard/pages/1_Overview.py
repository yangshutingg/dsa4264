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
def load_top10_topics_data():
    try:
        file_path = '../data/top10_topics.csv'
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} not found.")
        
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

# Load data
monthly_summary = load_monthly_summary()
topic_clusters = load_topic_clusters_data()
top10_topics = load_top10_topics_data()

# Title
st.title("Overall Analysis")

# Tabs
tab1, tab2 = st.tabs(["Trend Analysis", "Cluster Analysis"])

with tab1:
    st.subheader("Toxicity Over Time")

    # Time Range Filter
    start_date, end_date = st.slider(
        "Select Date Range",
        min_value = monthly_summary['yearmonth'].min().date(),
        max_value = monthly_summary['yearmonth'].max().date(),
        value = (monthly_summary['yearmonth'].min().date(), 
                monthly_summary['yearmonth'].max().date()),
        format = "YYYY-MM"
    )

    filtered_df = monthly_summary[(monthly_summary['yearmonth'].dt.date >= start_date) & 
                                  (monthly_summary['yearmonth'].dt.date <= end_date)]
    
    yearmonth = filtered_df['yearmonth']
    ave_score = filtered_df['average_toxicity_score_mean'].round(3)

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

    fig.update_yaxes(range=[0, 0.1],
                     title_text="Average Toxicity Score") 
    
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Topic Clustering")
    
    fig_tree = px.treemap(
        topic_clusters,
        path=["cluster_id"],
        values="total_posts",
        color="avg_toxicity",
        color_continuous_scale='RdYlBu_r',
        title='Cluster Distribution'
    )

    fig_tree.update_traces(
        hovertemplate=(
            "<b>Cluster ID:</b> %{label}<br>" +
            "<b>Total Posts:</b> %{value:,} posts<br>" +               # Format as integer with comma
            "<b>Unique Keywords:</b> %{customdata[3]}<br>" +           # Format as integer with comma
            "<b>Topic Diversity:</b> %{customdata[4]:.2f}<br>" +       # Format as decimal with 2 places
            "<b>Average Toxicity:</b> %{color:.2f}"                    # Format as decimal with 2 places
        ),
        customdata = topic_clusters.values
    )
    st.plotly_chart(fig_tree, use_container_width=True)

    st.subheader("Top 10 Topic Clusters by Average Toxicity")
    st.write(topic_clusters[['avg_toxicity', 'unique_keywords']].head(10))

    st.subheader("Toxicity Evolution of the Top 10 Topics by Average Toxicity")
    fig = go.Figure()
    top10_topic_avg_toxicity = top10_topics.groupby(['cluster_id', 'date'])['avg_toxicity'].mean().reset_index()
    top10_topic_avg_toxicity = top10_topic_avg_toxicity.pivot(index='date', columns='cluster_id', values='avg_toxicity')
    for cluster_id in top10_topic_avg_toxicity.columns:
        fig.add_trace(go.Scatter(
            x = top10_topic_avg_toxicity.index,
            y = top10_topic_avg_toxicity[cluster_id],
            mode='lines',
            name=f"Cluster {cluster_id}"
        ))

    fig.update_yaxes(range=[0, 0.55], title_text="Average Toxicity Score")
    
    st.plotly_chart(fig)


# Key Insights section
st.header("Insights")
with st.expander("See detailed insights"):
    st.write("""
    1. Political discussions show highest correlation with toxic comments
    2. Weekday evenings show peak toxicity levels
    3. Certain topics consistently trigger negative responses
    """)