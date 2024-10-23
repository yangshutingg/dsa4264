import streamlit as st
import pandas as pd
import numpy as np

# Set page config
st.set_page_config(
    page_title="Reddit Toxicity Analysis",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def process_metrics(filepath):
    """Process metrics from aggregated dataset"""
    try:
        # Read the aggregated dataset
        df = pd.read_csv(filepath)
        df['date'] = pd.to_datetime(df['date'])
        
        # Get latest month data
        latest_date = df['date'].max()
        current_month_data = df[df['date'] == latest_date]
        previous_month_data = df[df['date'] == latest_date - pd.DateOffset(months=1)]
        
        # Format month names for display
        current_month = latest_date.strftime('%B %Y')
        previous_month = (latest_date - pd.DateOffset(months=1)).strftime('%B %Y')
        
        metrics = {
            'dates': {
                'current_month': current_month,
                'previous_month': previous_month
            },
            'total_posts': {
                'value': current_month_data['post_count'].iloc[0],
                'previous': previous_month_data['post_count'].iloc[0],
                'change': ((current_month_data['post_count'].iloc[0] - 
                          previous_month_data['post_count'].iloc[0]) / 
                          previous_month_data['post_count'].iloc[0] * 100)
            },
            'average_toxicity': {
                'value': current_month_data['average_toxicity_score_mean'].iloc[0],
                'previous': previous_month_data['average_toxicity_score_mean'].iloc[0],
                'change': ((current_month_data['average_toxicity_score_mean'].iloc[0] - 
                          previous_month_data['average_toxicity_score_mean'].iloc[0]) / 
                          previous_month_data['average_toxicity_score_mean'].iloc[0] * 100)
            },
            'highest_model_score': {
                'value': max(
                    current_month_data['hatebert_toxicity_score_mean'].iloc[0],
                    current_month_data['hateXplain_toxicity_score_mean'].iloc[0],
                    current_month_data['toxicbert_toxicity_score_mean'].iloc[0]
                ),
                'model': max([
                    ('HateBERT', current_month_data['hatebert_toxicity_score_mean'].iloc[0]),
                    ('HateXplain', current_month_data['hateXplain_toxicity_score_mean'].iloc[0]),
                    ('ToxicBERT', current_month_data['toxicbert_toxicity_score_mean'].iloc[0])
                ], key=lambda x: x[1])[0]
            }
        }
        return metrics
        
    except Exception as e:
        st.error(f"Error processing data: {str(e)}")
        return None

# Load and process data
metrics = process_metrics('data/monthly_summary.csv')

st.title("🔍 Reddit Toxicity Analysis Dashboard")

# Current month display
st.subheader(f"Current Month: {metrics['dates']['current_month']}")

# Top row metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.info(
        "📊 **Total Posts**\n\n"
        f"{metrics['total_posts']['value']:,.0f}\n\n"
        f"vs {metrics['dates']['previous_month']}: {metrics['total_posts']['change']:+.1f}%"
    )

with col2:
    st.warning(
        "⚠️ **Average Toxicity Score**\n\n"
        f"{metrics['average_toxicity']['value']:.3f}\n\n"
        f"vs {metrics['dates']['previous_month']}: {metrics['average_toxicity']['change']:+.1f}%"
    )

with col3:
    st.error(
        "🎯 **Highest Model Score**\n\n"
        f"{metrics['highest_model_score']['value']:.3f}\n\n"
        f"Model: {metrics['highest_model_score']['model']}"
    )

# Topic Analysis Section (placeholder for now)
st.markdown("---")
st.subheader("Current Hot Topics")

# Hot Topics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🔥 Most Active Topic",
        value="Coming Soon",
        delta="Placeholder",
        help="Requires topic modeling"
    )

with col2:
    st.metric(
        label="⚠️ Highest Toxicity",
        value="Coming Soon",
        delta="Placeholder",
        delta_color="inverse",
        help="Requires topic analysis"
    )

with col3:
    st.metric(
        label="📈 Trending Topic",
        value="Coming Soon",
        delta="Placeholder",
        help="Requires topic modeling"
    )

with col4:
    st.metric(
        label="👥 Most Engaged",
        value="Coming Soon",
        delta="Placeholder",
        help="Requires additional analysis"
    )

# Topic Cards Section
st.markdown("---")
st.subheader("Topic Deep Dive")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("### 🚨 High Risk Topics")
        st.markdown("""
        Coming Soon
        (Requires topic modeling)
        """)

with col2:
    with st.container(border=True):
        st.markdown("### 💬 Most Active Discussions")
        st.markdown("""
        Coming Soon
        (Requires topic analysis)
        """)

# Bottom row metrics
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.error("🔍 **Peak Hours**\n\nComing Soon\n(Requires timestamp analysis)")

with col2:
    st.warning("📅 **Most Active Day**\n\nComing Soon\n(Requires timestamp analysis)")

with col3:
    st.success("✨ **Healthiest Topics**\n\nComing Soon\n(Requires topic analysis)")

# Navigation footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
Navigate to Detailed Analysis for in-depth insights
</div>
""", unsafe_allow_html=True)