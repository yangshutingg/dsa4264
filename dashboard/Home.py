import streamlit as st
import pandas as pd
import numpy as np
import json

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
        
        # Set January 2023 as current month
        target_date = pd.Timestamp('2023-01-01')  # January 2023
        previous_date = pd.Timestamp('2022-12-01')  # December 2022
        
        # Get data for current and previous months
        current_month_data = df[df['date'] == target_date].groupby('date').agg({
            'post_count': 'sum',
            'hatebert_toxicity_score_mean': 'mean',
            'hateXplain_toxicity_score_mean': 'mean',
            'toxicbert_toxicity_score_mean': 'mean',
            'average_toxicity_score_mean': 'mean'
        }).reset_index()

        previous_month_data = df[df['date'] == previous_date].groupby('date').agg({
            'post_count': 'sum',
            'hatebert_toxicity_score_mean': 'mean',
            'hateXplain_toxicity_score_mean': 'mean',
            'toxicbert_toxicity_score_mean': 'mean',
            'average_toxicity_score_mean': 'mean'
        }).reset_index()
        
        # Format month names for display
        current_month = target_date.strftime('%B %Y')
        previous_month = previous_date.strftime('%B %Y')
        
        # Check if we found data for the requested months
        if current_month_data.empty:
            st.error(f"Data not found for {current_month}")
            return None
        if previous_month_data.empty:
            st.error(f"Data not found for {previous_month}")
            return None
            
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
@st.cache_data
def load_time_metrics(hourly_filepath='data/hourly_metrics.csv', 
                      daily_filepath='data/daily_metrics.csv', 
                      peaks_filepath='data/peak_hours.csv'):
    """Calculate time metrics from CSV files."""
    try:
        # Load hourly metrics
        hourly_metrics = pd.read_csv(hourly_filepath)
        
        # Ensure the hour column is numeric
        hourly_metrics['hour'] = pd.to_numeric(hourly_metrics['hour'], errors='coerce').fillna(0).astype(int)
        
        # Load daily metrics
        daily_metrics = pd.read_csv(daily_filepath)
        
        # Load peaks data
        peaks = pd.read_csv(peaks_filepath)

        # Ensure proper formatting for peaks data
        peaks['peak_hour'] = peaks['peak_hour'].astype(int)
        peaks['lowest_hour'] = peaks['lowest_hour'].astype(int)

        return {
            'hourly': hourly_metrics,
            'daily': daily_metrics,
            'peaks': peaks
        }
    except Exception as e:
        st.error(f"Error calculating time metrics: {str(e)}")
        return None
    

@st.cache_data
def load_topic_metrics():
    """Load preprocessed topic metrics for dashboard"""
    try:
        with open('data/dashboard_topic_metrics.json', 'r') as f:
            metrics = json.load(f)
        return metrics
    except Exception as e:
        st.error(f"Error loading topic metrics: {str(e)}")
        return None

# Load and process data
metrics = process_metrics('data/monthly_summary.csv')
time_metrics = load_time_metrics()
topic_metrics = load_topic_metrics()

st.title("🔍 Reddit Toxicity Analysis Dashboard")

# Current month display
st.subheader(f"Current Month: {metrics['dates']['current_month']}")

# Top row metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.info(
        "📈 **Total Posts**\n\n"
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
    health_score = 100 - metrics['average_toxicity']['value']*100
    health_change = -metrics['average_toxicity']['change']
    st.success(
        "📊 **Community Health Score**\n\n"
        f"{health_score:.1f}/100\n\n"
        f"vs {metrics['dates']['previous_month']}: {health_change:+.1f}%"
    )

# Add footnote explaining Community Health Score
st.markdown("""
<div style='font-size: 0.8em; color: gray; margin-top: -10px; text-align: right;'>
* Community Health Score: Higher score indicates healthier discussions. Score above 70 indicates a healthy community.
</div>
""", unsafe_allow_html=True)

# Topic Analysis Section (placeholder for now)
st.markdown("---")
st.subheader("Current Hot Topics")

# Hot Topics row
col1, col2, col3, col4 = st.columns(4)

if topic_metrics:
    with col1:
        st.metric(
            label="🔥 Most Active Topic",
            value=", ".join(topic_metrics['most_active']['topic'][:2]),
            delta=f"{topic_metrics['most_active']['change']:+.1f}%",
            help=(f"Current activity: {topic_metrics['most_active']['posts']:.0f} posts\n"
                  f"Previous month: {topic_metrics['most_active']['previous_posts']:.0f} posts\n"
                  f"Shows topic with highest current activity")
        )

    with col2:
        st.metric(
            label="⚠️ Highest Toxicity",
            value=", ".join(topic_metrics['highest_toxicity']['topic'][:2]),
            delta=f"{topic_metrics['highest_toxicity']['change']:+.1f}%",
            delta_color="inverse",
            help=(f"Current toxicity: {topic_metrics['highest_toxicity']['score']:.3f}\n"
                  f"Previous month: {topic_metrics['highest_toxicity']['previous_score']:.3f}\n"
                  f"Topics that might need attention")
        )

    with col3:
        st.metric(
            label="📈 Trending Topic",
            value=", ".join(topic_metrics['trending']['topic'][:2]),
            delta=f"{topic_metrics['trending']['change']:+.1f}%",
            help=(f"Current posts: {topic_metrics['trending']['posts']:.0f}\n"
                  f"Previous month: {topic_metrics['trending']['previous_posts']:.0f}\n"
                  f"Topic with fastest growth")
        )

    with col4:
        st.metric(
            label="👥 Most Engaged",
            value=", ".join(topic_metrics['most_engaged']['topic'][:2]),
            delta=f"{topic_metrics['most_engaged']['change']:+.1f}%",
            help=(f"Current activity: {topic_metrics['most_engaged']['posts']:.0f} posts\n"
                  f"Previous month: {topic_metrics['most_engaged']['previous_posts']:.0f} posts\n"
                  f"Topic with highest sustained engagement")
        )

    # Topic Deep Dive Section
    st.markdown("---")
    st.subheader("Topic Deep Dive")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("### 🚨 High Risk Topics")
            for topic in topic_metrics['high_risk_topics']:
                st.markdown(
                    f"""<div style='background-color: rgba(255, 240, 240, 0.2); padding: 20px; border-radius: 8px; margin: 15px 0;'>
                    <div style='font-size: 1.1em; font-weight: 600; margin-bottom: 15px; padding: 0 10px;'>
                        {', '.join(topic['keywords'])}
                    </div>
                    <table style='width: 100%; border-collapse: separate; border-spacing: 0 8px;'>
                        <tr>
                            <td style='padding: 8px 15px; white-space: nowrap; width: 100px;'><strong>Toxicity:</strong></td>
                            <td style='padding: 8px 15px;'>{topic['current_toxicity']:.3f}</td>
                        </tr>
                        <tr>
                            <td style='padding: 8px 15px; white-space: nowrap;'><strong>Posts:</strong></td>
                            <td style='padding: 8px 15px;'>{topic['current_posts']:.0f}</td>
                        </tr>
                        <tr>
                            <td style='padding: 8px 15px; white-space: nowrap;'><strong>Change:</strong></td>
                            <td style='padding: 8px 15px; color: {"red" if topic["toxicity_change"] > 0 else "green"};'>
                                {topic["toxicity_change"]:+.1f}%
                            </td>
                        </tr>
                    </table>
                    </div>""",
                    unsafe_allow_html=True
                )

    with col2:
        with st.container(border=True):
            st.markdown("### 💬 Most Active Discussions")
            for topic in topic_metrics['active_discussions']:
                st.markdown(
                    f"""<div style='background-color: rgba(240, 242, 246, 0.2); padding: 20px; border-radius: 8px; margin: 15px 0;'>
                    <div style='font-size: 1.1em; font-weight: 600; margin-bottom: 15px; padding: 0 10px;'>
                        {', '.join(topic['keywords'])}
                    </div>
                    <table style='width: 100%; border-collapse: separate; border-spacing: 0 8px;'>
                        <tr>
                            <td style='padding: 8px 15px; white-space: nowrap; width: 100px;'><strong>Posts:</strong></td>
                            <td style='padding: 8px 15px;'>{topic['current_posts']:.0f}</td>
                        </tr>
                        <tr>
                            <td style='padding: 8px 15px; white-space: nowrap;'><strong>Change:</strong></td>
                            <td style='padding: 8px 15px; color: {"red" if topic["post_change"] > 0 else "green"};'>
                                {topic["post_change"]:+.1f}%
                            </td>
                        </tr>
                        <tr>
                            <td style='padding: 8px 15px; white-space: nowrap;'><strong>Toxicity:</strong></td>
                            <td style='padding: 8px 15px;'>{topic['current_toxicity']:.3f}</td>
                        </tr>
                    </table>
                    </div>""",
                    unsafe_allow_html=True
                )
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