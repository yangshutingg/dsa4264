import pandas as pd
import numpy as np
from datetime import datetime
import os

def preprocess_time_metrics(input_file, output_dir='data'):

    print("Loading raw data...")
    df = pd.read_csv(input_file)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Hourly Summary
    print("Processing hourly metrics...")
    hourly_metrics = df.groupby(df['timestamp'].dt.hour).agg({
        'text': 'count',  # post count
        'average_toxicity_score': 'mean',
        'hatebert_toxicity_score': 'mean',
        'hateXplain_toxicity_score': 'mean',
        'toxicbert_toxicity_score': 'mean'
    }).reset_index()
    hourly_metrics.columns = ['hour', 'post_count', 'avg_toxicity', 
                            'hatebert_score', 'hatexplain_score', 'toxicbert_score']
    
    # Add relative metrics
    hourly_metrics['post_percent'] = (hourly_metrics['post_count'] / 
                                    hourly_metrics['post_count'].sum() * 100)
    hourly_metrics['toxicity_vs_mean'] = ((hourly_metrics['avg_toxicity'] - 
                                         hourly_metrics['avg_toxicity'].mean()) / 
                                         hourly_metrics['avg_toxicity'].mean() * 100)
    
    # 2. Daily Summary
    print("Processing daily metrics...")
    daily_metrics = df.groupby(df['timestamp'].dt.day_name()).agg({
        'text': 'count',
        'average_toxicity_score': 'mean',
        'hatebert_toxicity_score': 'mean',
        'hateXplain_toxicity_score': 'mean',
        'toxicbert_toxicity_score': 'mean'
    }).reset_index()
    daily_metrics.columns = ['day', 'post_count', 'avg_toxicity',
                           'hatebert_score', 'hatexplain_score', 'toxicbert_score']
    
    # Add relative metrics
    daily_metrics['post_percent'] = (daily_metrics['post_count'] / 
                                   daily_metrics['post_count'].sum() * 100)
    daily_metrics['toxicity_vs_mean'] = ((daily_metrics['avg_toxicity'] - 
                                        daily_metrics['avg_toxicity'].mean()) / 
                                        daily_metrics['avg_toxicity'].mean() * 100)
    
    # 3. Monthly Summary
    print("Processing monthly metrics...")
    # First create a year-month column for proper grouping
    df['year_month'] = df['timestamp'].dt.to_period('M')
    monthly_agg = df.groupby('year_month').agg({
        'text': 'count',
        'average_toxicity_score': ['mean', 'std'],
        'hatebert_toxicity_score': ['mean', 'std'],
        'hateXplain_toxicity_score': ['mean', 'std'],
        'toxicbert_toxicity_score': ['mean', 'std']
    })
    
    # Flatten the multi-level columns
    monthly_agg.columns = ['_'.join(col).strip() for col in monthly_agg.columns.values]
    monthly_metrics = monthly_agg.reset_index()
    # Extract year and month from period index
    monthly_metrics['year'] = monthly_metrics['year_month'].dt.year
    monthly_metrics['month'] = monthly_metrics['year_month'].dt.month
    # Drop the period column and reorder
    monthly_metrics = monthly_metrics.drop('year_month', axis=1)
    
    # Rename columns to be more intuitive
    monthly_metrics = monthly_metrics.rename(columns={
        'text_count': 'post_count',
        'average_toxicity_score_mean': 'avg_toxicity_mean',
        'average_toxicity_score_std': 'avg_toxicity_std',
        'hatebert_toxicity_score_mean': 'hatebert_mean',
        'hatebert_toxicity_score_std': 'hatebert_std',
        'hateXplain_toxicity_score_mean': 'hatexplain_mean',
        'hateXplain_toxicity_score_std': 'hatexplain_std',
        'toxicbert_toxicity_score_mean': 'toxicbert_mean',
        'toxicbert_toxicity_score_std': 'toxicbert_std'
    })
    
    # 4. Peak Hours Analysis
    print("Processing peak hours analysis...")
    peak_hours = pd.DataFrame({
        'metric': ['posts', 'toxicity'],
        'peak_hour': [
            hourly_metrics.loc[hourly_metrics['post_count'].idxmax(), 'hour'],
            hourly_metrics.loc[hourly_metrics['avg_toxicity'].idxmax(), 'hour']
        ],
        'peak_value': [
            hourly_metrics['post_count'].max(),
            hourly_metrics['avg_toxicity'].max()
        ],
        'lowest_hour': [
            hourly_metrics.loc[hourly_metrics['post_count'].idxmin(), 'hour'],
            hourly_metrics.loc[hourly_metrics['avg_toxicity'].idxmin(), 'hour']
        ],
        'lowest_value': [
            hourly_metrics['post_count'].min(),
            hourly_metrics['avg_toxicity'].min()
        ]
    })
    
    # Save processed data
    print("Saving processed data...")
    hourly_metrics.to_csv(f"{output_dir}/hourly_metrics.csv", index=False)
    daily_metrics.to_csv(f"{output_dir}/daily_metrics.csv", index=False)
    monthly_metrics.to_csv(f"{output_dir}/monthly_metrics.csv", index=False)
    peak_hours.to_csv(f"{output_dir}/peak_hours.csv", index=False)
    
    # Generate metadata
    metadata = {
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_posts': len(df),
        'date_range': f"{df['timestamp'].min()} to {df['timestamp'].max()}",
        'file_paths': {
            'hourly_metrics': 'hourly_metrics.csv',
            'daily_metrics': 'daily_metrics.csv',
            'monthly_metrics': 'monthly_metrics.csv',
            'peak_hours': 'peak_hours.csv'
        }
    }
    
    # Save metadata
    pd.DataFrame([metadata]).to_json(f"{output_dir}/metadata.json", orient='records')
    
    print("Processing complete! Files saved in:", output_dir)
    return metadata


if __name__ == "__main__":
    input_file = "data/combined_data_scores.csv"
    metadata = preprocess_time_metrics(input_file)
    print("\nProcessing Summary:")
    for key, value in metadata.items():
        print(f"{key}: {value}")