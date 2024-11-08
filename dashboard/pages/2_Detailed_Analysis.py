import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# Load your processed data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('../data/processed/monthly_summary.csv')
        df['date'] = pd.to_datetime(df['date'])
        return df
    except:
        # Generate sample data if file not found
        return generate_sample_data()

def generate_sample_data():
    dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
    df = pd.DataFrame({
        'date': dates,
        'hatebert_toxicity_score_mean': np.random.rand(len(dates)) * 0.5,
        'hateXplain_toxicity_score_mean': np.random.rand(len(dates)) * 0.5,
        'toxicbert_toxicity_score_mean': np.random.rand(len(dates)) * 0.5,
        'average_toxicity_score_mean': np.random.rand(len(dates)) * 0.5,
        'post_count': np.random.randint(100, 1000, size=len(dates)),
        'moderation_rate': np.random.rand(len(dates)) * 0.3,
    })
    return df

# Load data
df = load_data()

# Title and description
st.title("Reddit Content Analysis: Understanding Toxicity Trends")
st.markdown("""
This dashboard provides a detailed analysis of toxicity trends across Singapore subreddits,
helping inform policy decisions and content moderation strategies.
""")

# Sidebar for Detailed Analysis options with "Police" as the default
st.sidebar.header("Detailed Analysis")
page_selection = st.sidebar.selectbox("Choose a topic for detailed analysis:", ["Police", "LGBTQ"], index=0)

# Layout setup based on selected topic
if page_selection == "Police":
    st.header("Detailed Analysis: Police-related Topics")
    st.markdown("In-depth analysis focusing on toxicity trends around police-related discussions.")
    
    # Technical Terms Explanation (at the top)
    with st.expander("Technical Terms Explanation"):
        st.write("""
        **Toxicity Score**: The toxicity score represents the likelihood of toxic content within discussions. 
        Higher scores indicate higher levels of toxic language.
        
        **Moderation Rate**: Percentage of content that has been flagged or moderated to maintain community standards.
        """)
    
    # Create two main columns: one for stacked graphs and one for recommendations
    left_col, right_col = st.columns([3, 1])  # Left column wider than right column
    
    with left_col:
        # Graph 1: Toxicity Trend Over Time
        fig1 = px.line(df, x="date", y="hatebert_toxicity_score_mean", title="Police Topic Toxicity Trend Over Time")
        st.plotly_chart(fig1, use_container_width=True)

        # Graph 2: Discussion Volume Over Time
        fig2 = px.line(df, x="date", y="post_count", title="Police Topic Discussion Volume Over Time")
        st.plotly_chart(fig2, use_container_width=True)
    
    with right_col:
        # Recommendations section on the right
        st.subheader("Recommendations for Police-related Discussions")
        st.markdown("""
        1. **Increase moderation** during peak hours to manage potential surges in toxicity.
        2. **Monitor specific keywords** that frequently appear in toxic discussions to enable proactive moderation.
        3. **Engage community leaders** to promote respectful discussions, especially during sensitive events.
        """)

elif page_selection == "LGBTQ":
    st.header("Detailed Analysis: LGBTQ-related Topics")
    st.markdown("In-depth analysis focusing on toxicity trends around LGBTQ-related discussions.")
    
    # Technical Terms Explanation (at the top)
    with st.expander("Technical Terms Explanation"):
        st.write("""
        **Toxicity Score**: The toxicity score represents the likelihood of toxic content within discussions. 
        Higher scores indicate higher levels of toxic language.
        
        **Moderation Rate**: Percentage of content that has been flagged or moderated to maintain community standards.
        """)
    
    # Create two main columns: one for stacked graphs and one for recommendations
    left_col, right_col = st.columns([3, 1])  # Left column wider than right column
    
    with left_col:
        # Graph 1: Toxicity Trend Over Time
        fig1 = px.line(df, x="date", y="toxicbert_toxicity_score_mean", title="LGBTQ Topic Toxicity Trend Over Time")
        st.plotly_chart(fig1, use_container_width=True)

        # Graph 2: Discussion Volume Over Time
        fig2 = px.line(df, x="date", y="post_count", title="LGBTQ Topic Discussion Volume Over Time")
        st.plotly_chart(fig2, use_container_width=True)
    
    with right_col:
        # Recommendations section on the right
        st.subheader("Recommendations for LGBTQ-related Discussions")
        st.markdown("""
        1. **Increase visibility** of supportive resources and organizations for LGBTQ topics.
        2. **Identify high-risk keywords** associated with hateful language to improve content moderation accuracy.
        3. **Encourage community support** by highlighting positive interactions and constructive discussions.
        """)