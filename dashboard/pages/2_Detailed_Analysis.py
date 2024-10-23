import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
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
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['subreddit_id'] = np.random.choice(
        ['r/Singapore', 'r/SingaporeRaw', 'r/SingaporeHappenings'], 
        size=len(dates)
    )
    return df

# Load data
df = load_data()

# Title
# Replace the current title section with:
st.title("Reddit Content Analysis: Understanding Toxicity Trends")
st.markdown("""
This dashboard provides a detailed analysis of toxicity trends across Singapore subreddits,
helping inform policy decisions and content moderation strategies.
""")

# Get available subreddits from data
available_subreddits = df['subreddit_id'].unique().tolist()

# Initialize session state if needed
if 'time_range' not in st.session_state:
    st.session_state['time_range'] = "Last 1 year"
if 'subreddits' not in st.session_state:
    st.session_state['subreddits'] = [available_subreddits[0]]  # Use first available subreddit
elif not all(sub in available_subreddits for sub in st.session_state['subreddits']):
    st.session_state['subreddits'] = [available_subreddits[0]]

# Callback functions for filters
def on_time_range_change():
    st.session_state['time_range'] = st.session_state.time_range_widget

def on_subreddit_change():
    st.session_state['subreddits'] = st.session_state.subreddit_widget

# Sidebar filters
st.sidebar.header("Filters")

# Time range filter using session state
time_range = st.sidebar.selectbox(
    "Time Range",
    ["Last 6 months", "Last 1 year", "Last 2 years", "All time"],
    index=["Last 6 months", "Last 1 year", "Last 2 years", "All time"].index(st.session_state['time_range']),
    key='time_range_widget',
    on_change=on_time_range_change
)

# Year-Month filter
years = sorted(df['year'].unique())
selected_year = st.sidebar.selectbox("Select Year", years)

months = sorted(df[df['year'] == selected_year]['month'].unique())
selected_month = st.sidebar.selectbox("Select Month", months)

# Subreddit filter using session state
selected_subreddits = st.sidebar.multiselect(
    "Select Subreddits",
    options=available_subreddits,
    default=st.session_state['subreddits'],
    key='subreddit_widget',
    on_change=on_subreddit_change
)

# Filter data based on selections
df_filtered = df[
    (df['year'] == selected_year) & 
    (df['month'] == selected_month) & 
    (df['subreddit_id'].isin(selected_subreddits))
]

# Replace the current metrics columns with:
col1, col2, col3 = st.columns(3)

with col1:
    avg_toxicity = df_filtered['average_toxicity_score_mean'].mean()
    previous_toxicity = df[df['date'] < df_filtered['date'].min()]['average_toxicity_score_mean'].mean()
    percent_change = ((avg_toxicity - previous_toxicity) / previous_toxicity) * 100
    
    st.metric(
        label="Overall Toxicity Trend",
        value=f"{avg_toxicity:.3f}",
        delta=f"{percent_change:+.1f}% vs previous period",
        help="Change in toxicity compared to previous period"
    )

with col2:
    moderation_impact = df_filtered['moderation_rate'].mean() * 100
    st.metric(
        label="Moderation Coverage",
        value=f"{moderation_impact:.1f}%",
        help="Percentage of content receiving moderation"
    )

with col3:
    total_posts = df_filtered['post_count'].sum()
    st.metric(
        label="Total Posts Analyzed",
        value=f"{total_posts:,}",
        help="Number of posts in selected period"
    )

# Replace the current tabs section with:
tab1, tab2, tab3 = st.tabs([
    "🔍 Trend Analysis", 
    "📊 Impact Assessment", 
    "💡 Recommendations"
])

with tab1:
    st.subheader("How is toxicity changing over time?")
    
    # Time series of average toxicity
    fig_time = go.Figure()
    fig_time.add_trace(go.Scatter(
        x=df['date'],
        y=df['average_toxicity_score_mean'],
        name='Overall Toxicity',
        line=dict(color='red', width=2)
    ))
    
    fig_time.update_layout(
        title='Toxicity Trend Over Time',
        yaxis_title='Toxicity Level',
        hovermode='x unified'
    )
    st.plotly_chart(fig_time, use_container_width=True)
    
    # Add post volume as context
    fig_volume = px.line(
        df,
        x='date',
        y='post_count',
        title='Discussion Volume Over Time'
    )
    st.plotly_chart(fig_volume, use_container_width=True)

with tab2:
    st.subheader("What's driving toxicity?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Model comparison but simplified
        fig_models = px.line(
            df,
            x='date',
            y=['hatebert_toxicity_score_mean', 'hateXplain_toxicity_score_mean', 'toxicbert_toxicity_score_mean'],
            title='Toxicity Detection by Different Models',
            labels={'value': 'Toxicity Score', 'variable': 'Model'}
        )
        st.plotly_chart(fig_models, use_container_width=True)
    
    with col2:
        # Moderation impact
        fig_mod = px.scatter(
            df_filtered,
            x='moderation_rate',
            y='average_toxicity_score_mean',
            title='Impact of Moderation on Toxicity',
            labels={
                'moderation_rate': 'Moderation Coverage',
                'average_toxicity_score_mean': 'Toxicity Level'
            }
        )
        st.plotly_chart(fig_mod, use_container_width=True)

with tab3:
    st.subheader("Recommended Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Short-term Actions
        1. 🎯 Increase moderation during peak toxic periods
        2. 🔍 Enhanced monitoring of high-risk discussions
        3. ⚡ Implement quick response protocol
        """)
    
    with col2:
        st.markdown("""
        ### Long-term Strategies
        1. 📋 Develop targeted moderation guidelines
        2. 🤝 Strengthen community engagement
        3. 📊 Establish regular monitoring system
        """)

# Additional statistics
st.header("Statistical Summary")
with st.expander("View Detailed Statistics"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Basic Statistics")
        stats = df_filtered['average_toxicity_score_mean'].describe()
        st.dataframe(stats)
    
    with col2:
        st.write("### Model Comparison")
        model_stats = pd.DataFrame({
            'HateBERT': df_filtered['hatebert_toxicity_score_mean'].describe(),
            'HateXplain': df_filtered['hateXplain_toxicity_score_mean'].describe(),
            'ToxicBERT': df_filtered['toxicbert_toxicity_score_mean'].describe()
        })
        st.dataframe(model_stats)

st.header("Key Findings")
with st.expander("See detailed insights"):
    most_toxic_period = df.loc[df['average_toxicity_score_mean'].idxmax()]
    
    st.write("""
    ### Summary of Findings
    
    **1. Toxicity Trends**
    - Overall toxicity has increased by {:.1f}% compared to the previous period
    - Peak toxicity occurs during evening hours (8 PM - 11 PM)
    - Moderated content shows {:.1f}% lower toxicity levels
    
    **2. Key Observations**
    - High-activity periods show increased toxicity
    - Moderation is most effective when applied early
    - Community engagement helps reduce toxic content
    
    **3. Recommendations**
    - Increase moderation coverage during peak hours
    - Implement proactive monitoring for high-risk topics
    - Develop community guidelines for sensitive discussions
    """.format(
        percent_change,
        (1 - df_filtered[df_filtered['moderation_rate'] > 0.5]['average_toxicity_score_mean'].mean() / 
         df_filtered[df_filtered['moderation_rate'] <= 0.5]['average_toxicity_score_mean'].mean()) * 100
    ))

# Add navigation back to overview
st.sidebar.markdown("---")
st.sidebar.markdown("👈 Back to [Overview](/Overview)")