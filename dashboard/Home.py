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
    
@st.cache_data
def load_time_metrics(processed_data_dir='data'):
    """Load preprocessed time metrics"""
    try:
        hourly_metrics = pd.read_csv(f"{processed_data_dir}/hourly_metrics.csv")
        daily_metrics = pd.read_csv(f"{processed_data_dir}/daily_metrics.csv")
        peak_hours = pd.read_csv(f"{processed_data_dir}/peak_hours.csv")
        
        return {
            'hourly': hourly_metrics,
            'daily': daily_metrics,
            'peaks': peak_hours
        }
    except Exception as e:
        st.error(f"Error loading time metrics: {str(e)}")
        return None

# Load and process data
metrics = process_metrics('data/monthly_summary.csv')
time_metrics = load_time_metrics()

# Load and process data
metrics = process_metrics('data/monthly_summary.csv')
time_metrics = load_time_metrics()

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

if time_metrics:
    # Peak Hours
    peak_posts = time_metrics['peaks'][time_metrics['peaks']['metric'] == 'posts'].iloc[0]
    with col1:
        st.error(
            f"🔍 **Peak Hours**\n\n"
            f"Most Active: {int(peak_posts['peak_hour']):02d}:00  \n"
            f"Posts: {int(peak_posts['peak_value']):,}\n\n"
            f"Least Active: {int(peak_posts['lowest_hour']):02d}:00  \n"
            f"Posts: {int(peak_posts['lowest_value']):,}"
        )

    # Most Active Day
    most_active_day = time_metrics['daily'].loc[time_metrics['daily']['post_count'].idxmax()]
    with col2:
        st.warning(
            f"📅 **Most Active Day**\n\n"
            f"{most_active_day['day']}  \n"
             "\n"
            f"Posts: {int(most_active_day['post_count']):,}  \n"
             "\n"
            f"({most_active_day['post_percent']:.1f}% of total posts)"
        )

    # Add time-based toxicity insights
    peak_toxicity = time_metrics['peaks'][time_metrics['peaks']['metric'] == 'toxicity'].iloc[0]
    with col3:
        st.success(
            f"⏰ **Activity Patterns**\n\n"
            f"Highest Toxicity: {int(peak_toxicity['peak_hour']):02d}:00  \n"
            f"Score: {peak_toxicity['peak_value']:.3f}\n\n"
            f"Lowest Toxicity: {int(peak_toxicity['lowest_hour']):02d}:00  \n"
            f"Score: {peak_toxicity['lowest_value']:.3f}"
        )

else:
    # Fallback if time metrics aren't available
    with col1:
        st.error("🔍 **Peak Hours**\n\nData not available")
    with col2:
        st.warning("📅 **Most Active Day**\n\nData not available")
    with col3:
        st.success("⏰ **Activity Patterns**\n\nData not available")
        
# Navigation footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
Navigate to Detailed Analysis for in-depth insights
</div>
""", unsafe_allow_html=True)