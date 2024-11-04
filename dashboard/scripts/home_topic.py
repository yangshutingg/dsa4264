import pandas as pd
import json
from pathlib import Path
import ast
from datetime import datetime

def get_month_metrics(temporal_dict, toxicity_dict, target_date, previous_date):
    """Get metrics for specific month from temporal and toxicity evolution data"""
    try:
        if isinstance(temporal_dict, str):
            temporal_dict = ast.literal_eval(temporal_dict)
        if isinstance(toxicity_dict, str):
            toxicity_dict = ast.literal_eval(toxicity_dict)
            
        target_year = str(target_date.year)
        target_month = target_date.strftime('%Y-%m')
        prev_month = previous_date.strftime('%Y-%m')
        
        # Get posts from temporal_evolution for both months
        current_year_posts = temporal_dict.get(target_year, 0)
        prev_year_posts = temporal_dict.get(str(previous_date.year), 0)
        
        # Get toxicity and post metrics from toxicity_evolution
        current_metrics = toxicity_dict.get(target_year, {}).get(target_month, {})
        prev_metrics = toxicity_dict.get(str(previous_date.year), {}).get(prev_month, {})
        
        # Extract values with defaults
        current_stats = {
            'post_count': float(current_metrics.get('post_count', current_year_posts/12)),
            'avg_toxicity': float(current_metrics.get('avg_toxicity', 0))
        }
        
        prev_stats = {
            'post_count': float(prev_metrics.get('post_count', prev_year_posts/12)),
            'avg_toxicity': float(prev_metrics.get('avg_toxicity', 0))
        }
        
        # Calculate changes
        post_change = ((current_stats['post_count'] - prev_stats['post_count']) / 
                      prev_stats['post_count'] * 100) if prev_stats['post_count'] else 0
        toxicity_change = ((current_stats['avg_toxicity'] - prev_stats['avg_toxicity']) / 
                          prev_stats['avg_toxicity'] * 100) if prev_stats['avg_toxicity'] else 0
            
        return (current_stats['post_count'], prev_stats['post_count'], post_change,
                current_stats['avg_toxicity'], prev_stats['avg_toxicity'], toxicity_change)
        
    except Exception as e:
        print(f"Error processing data for {target_month}: {e}")
        return 0, 0, 0, 0, 0, 0



def calculate_topic_metrics(topics_df, target_date='2023-01-01'):
    """Calculate topic metrics with improved handling of small numbers"""
    target_date = pd.Timestamp(target_date)
    previous_date = target_date - pd.DateOffset(months=1)
    
    print(f"\nCalculating metrics for {target_date.strftime('%B %Y')} vs {previous_date.strftime('%B %Y')}")
    
    topic_metrics = []
    for idx, row in topics_df.iterrows():
        toxicity_dict = ast.literal_eval(row['toxicity_evolution']) if isinstance(row['toxicity_evolution'], str) else row['toxicity_evolution']
        temporal_dict = ast.literal_eval(row['temporal_evolution']) if isinstance(row['temporal_evolution'], str) else row['temporal_evolution']
        
        # Get yearly totals for context
        current_year_total = float(temporal_dict.get(str(target_date.year), 0))
        prev_year_total = float(temporal_dict.get(str(previous_date.year), 0))
        
        # Get monthly metrics
        current_month = target_date.strftime('%Y-%m')
        current_year = str(target_date.year)
        current_metrics = toxicity_dict.get(current_year, {}).get(current_month, {})
        
        prev_month = previous_date.strftime('%Y-%m')
        prev_year = str(previous_date.year)
        prev_metrics = toxicity_dict.get(prev_year, {}).get(prev_month, {})
        
        # Use yearly average when monthly data is too small
        current_posts = max(float(current_metrics.get('post_count', 0)), current_year_total/12)
        prev_posts = max(float(prev_metrics.get('post_count', 0)), prev_year_total/12)
        
        current_toxicity = float(current_metrics.get('avg_toxicity', row['avg_toxicity']))
        prev_toxicity = float(prev_metrics.get('avg_toxicity', row['avg_toxicity']))
        
        # Calculate changes with minimum threshold
        if prev_posts >= 1:  # Only calculate change if there were at least some posts
            post_change = ((current_posts - prev_posts) / prev_posts * 100)
        else:
            post_change = 0
            
        if prev_toxicity > 0:
            toxicity_change = ((current_toxicity - prev_toxicity) / prev_toxicity * 100)
        else:
            toxicity_change = 0
        
        # Calculate engagement using overall metrics
        total_posts = float(row['total_posts'])
        size = float(row['size'])
        topic_diversity = float(row['topic_diversity'])
        engagement_score = (size * topic_diversity * current_posts) if current_posts > 0 else 0
        
        keywords = ast.literal_eval(row['unique_keywords']) if isinstance(row['unique_keywords'], str) else row['unique_keywords']
        
        topic_metrics.append({
            'cluster_id': row['cluster_id'],
            'keywords': keywords,
            'current_posts': current_posts,
            'previous_posts': prev_posts,
            'post_change': post_change,
            'current_toxicity': current_toxicity,
            'previous_toxicity': prev_toxicity,
            'toxicity_change': toxicity_change,
            'engagement_score': engagement_score,
            'total_posts': total_posts,
            'yearly_posts': current_year_total
        })
        
    metrics_df = pd.DataFrame(topic_metrics)
    
    dashboard_metrics = {
        'most_active': {
            'topic': metrics_df[metrics_df['current_posts'] >= 1].nlargest(1, 'current_posts').iloc[0]['keywords'][:3],
            'posts': float(metrics_df[metrics_df['current_posts'] >= 1].nlargest(1, 'current_posts').iloc[0]['current_posts']),
            'previous_posts': float(metrics_df[metrics_df['current_posts'] >= 1].nlargest(1, 'current_posts').iloc[0]['previous_posts']),
            'change': float(metrics_df[metrics_df['current_posts'] >= 1].nlargest(1, 'current_posts').iloc[0]['post_change'])
        },
        'highest_toxicity': {
            'topic': metrics_df[metrics_df['current_toxicity'] > 0].nlargest(1, 'current_toxicity').iloc[0]['keywords'][:3],
            'score': float(metrics_df[metrics_df['current_toxicity'] > 0].nlargest(1, 'current_toxicity').iloc[0]['current_toxicity']),
            'previous_score': float(metrics_df[metrics_df['current_toxicity'] > 0].nlargest(1, 'current_toxicity').iloc[0]['previous_toxicity']),
            'change': float(metrics_df[metrics_df['current_toxicity'] > 0].nlargest(1, 'current_toxicity').iloc[0]['toxicity_change'])
        },
        'trending': {
            'topic': metrics_df[
                (metrics_df['previous_posts'] >= 1) & 
                (metrics_df['current_posts'] >= 1)
            ].nlargest(1, 'post_change').iloc[0]['keywords'][:3],
            'posts': float(metrics_df[metrics_df['previous_posts'] >= 1].nlargest(1, 'post_change').iloc[0]['current_posts']),
            'previous_posts': float(metrics_df[metrics_df['previous_posts'] >= 1].nlargest(1, 'post_change').iloc[0]['previous_posts']),
            'change': float(metrics_df[metrics_df['previous_posts'] >= 1].nlargest(1, 'post_change').iloc[0]['post_change'])
        },
        'most_engaged': {
            'topic': metrics_df[metrics_df['engagement_score'] > 0].nlargest(1, 'yearly_posts').iloc[0]['keywords'][:3],
            'posts': float(metrics_df[metrics_df['engagement_score'] > 0].nlargest(1, 'yearly_posts').iloc[0]['current_posts']),
            'previous_posts': float(metrics_df[metrics_df['engagement_score'] > 0].nlargest(1, 'yearly_posts').iloc[0]['previous_posts']),
            'change': float(metrics_df[metrics_df['engagement_score'] > 0].nlargest(1, 'yearly_posts').iloc[0]['post_change'])
        }
    }

    # Add high risk topics
    high_risk = metrics_df[metrics_df['current_toxicity'] > 0].nlargest(3, 'current_toxicity')
    dashboard_metrics['high_risk_topics'] = [
        {
            'keywords': row['keywords'][:3],
            'current_toxicity': float(row['current_toxicity']),
            'previous_toxicity': float(row['previous_toxicity']),
            'current_posts': float(row['current_posts']),
            'toxicity_change': float(row['toxicity_change'])
        }
        for _, row in high_risk.iterrows()
    ]

    # Add active discussions
    active_discussions = metrics_df[metrics_df['current_posts'] >= 1].nlargest(3, 'current_posts')
    dashboard_metrics['active_discussions'] = [
        {
            'keywords': row['keywords'][:3],
            'current_posts': float(row['current_posts']),
            'previous_posts': float(row['previous_posts']),
            'post_change': float(row['post_change']),
            'current_toxicity': float(row['current_toxicity'])
        }
        for _, row in active_discussions.iterrows()
    ]

    # Print debug information
    print("\nFinal Metrics:")
    for category in ['MOST_ACTIVE', 'HIGHEST_TOXICITY', 'TRENDING', 'MOST_ENGAGED']:
        print(f"\n{category}:")
        data = dashboard_metrics[category.lower()]
        print(f"Topic: {', '.join(data['topic'][:2])}")
        if 'score' in data:
            print(f"Current Score: {data['score']:.3f}")
            print(f"Previous Score: {data['previous_score']:.3f}")
        else:
            print(f"Current Posts: {data['posts']:.1f}")
            print(f"Previous Posts: {data['previous_posts']:.1f}")
        print(f"Change: {data['change']:+.1f}%")

    print("\nHIGH RISK TOPICS:")
    for topic in dashboard_metrics['high_risk_topics']:
        print(f"Topic: {', '.join(topic['keywords'][:2])}")
        print(f"Current Toxicity: {topic['current_toxicity']:.3f}")
        print(f"Previous Toxicity: {topic['previous_toxicity']:.3f}")
        print(f"Change: {topic['toxicity_change']:+.1f}%")
        print("---")

    print("\nACTIVE DISCUSSIONS:")
    for topic in dashboard_metrics['active_discussions']:
        print(f"Topic: {', '.join(topic['keywords'][:2])}")
        print(f"Current Posts: {topic['current_posts']:.1f}")
        print(f"Previous Posts: {topic['previous_posts']:.1f}")
        print(f"Change: {topic['post_change']:+.1f}%")
        print("---")
    
    # Save processed metrics
    with open('data/dashboard_topic_metrics.json', 'w') as f:
        json.dump(dashboard_metrics, f)


if __name__ == "__main__":
    # Read your topic modeling results
    topics_df = pd.read_csv('data/topic_clusters.csv')
    
    # Process and save metrics for January 2023
    calculate_topic_metrics(topics_df, target_date='2023-01-01')
    print("Preprocessing completed successfully!")