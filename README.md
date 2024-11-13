# Singapore Subreddits Toxicity Analysis  
Members: Bernice Ong Hwee Yee, Cao Han, Luo Xinming, Su Xuanxuan, Yang Shu Ting

## Project Overview
This project focuses on analysing toxicity (content that is rude, disrespectful, or otherwise likely to make someone leave a discussion) in Singapore Subreddits text data to uncover insights and patterns. Using natural language processing (NLP) techniques, we process, analyse, and visualise text data to identify sentiment trends and key topic clusters.

## Data Access
To run the entire project, you’ll need, at a minimum, a raw data file with the columns: `timestamp`, `link`, and `text`, saved within your project’s `data` subfolder. For running individual scripts, ensure you have access to any necessary intermediate data files.

Please note that the raw data used in this project is restricted and not publicly accessible due to ownership limitations. For data access requests, contact the respective data owner or organisation. If you have questions or need processed sample data for testing, feel free to open an issue in this repository. We’ll assist within the allowed guidelines.

Thank you for your cooperation!

## Results
Upon completing the analysis, the key findings and visualisations are accessible in the dashboard folder, including:

- Topic Clusters and Keywords: Identified thematic clusters and representative keywords.
- Sentiment Trends Over Time: Patterns of toxicity and sentiment changes across the analysed period.
- Topic Network Clouds: Visualisations of topic relationships and high-similarity themes.

## Installation
To get started, clone this repository and install the required packages:

```bash
git clone https://github.com/yangshutingg/dsa4264.git
cd dsa4264
pip install -r dashboard/requirements.txt
```
Create a `data` folder in the root directory, verify the directory organisation:

```plaintext
DSA4264/
├── dashboard/               # Dashboard codes, to be further illustrated in later section
├── data/                    # Data folder to place your downloaded data here
├── report/                  # Final reports and documentation
├── src/                     # Source code 
│   ├── topic models/
│   │   ├── parameter_tuning.ipynb # Requires combined_data_scores.csv
│   │   ├── topic_clustering.ipynb # Requires topic_2020.csv, topic_2021.csv, topic_2022.csv, topic_2023.csv, generates topic_clusters.csv
│   │   ├── topic_modelling.ipynb  # Requires combined_data_scores.csv
│   │   ├── topic_network.ipynb    # Requires topic_clusters.csv
│   ├── toxicity models/
│   │   ├── hatebert_model.ipynb   # Requires combined_data.csv, generates hatebert_scores.csv
│   │   ├── hateXplain_model.ipynb # Requires combined_data.csv, generates hateXplain_scores.csv
│   │   ├── toxicbert_model.ipynb  # Requires combined_data.csv, generates toxicbert_scores.csv
│   ├── data_processing.ipynb      # Requires original datasets, combined_data.csv, hatebert_scores.csv, hateXplain_scores.csv, toxicbert_scores.csv,
                                   # generates combined_data_scores.csv
│   ├── trend_analysis.ipynb       # Requires topic_2020.csv, topic_2021.csv, topic_2022.csv, topic_2023.csv, combined_data_scores.csv, generate monthly_scores_summary.csv
├── .gitignore              
├── README.md                
```
Before running individual scripts, ensure the respective required data files are available in the `data/` directory.

```plaintext
data/
├── combined_data.csv
├── combined_data_scores.csv
├── daily_metrics.csv
├── dashboard_topic_metrics.json
├── hourly_metrics.csv
├── monthly_metrics.csv
├── monthly_scores_summary.csv
├── monthly_summary.csv
├── peak_hours.csv
├── top10_topics.csv
├── topic_clusters.csv
├── topics_2020.csv
├── topics_2021.csv
├── topics_2022.csv
├── topics_2023.csv
├── hatebert_scores.csv
├── hateXplain_scores.csv
├── toxicbert_scores.csv
```
## Running the Interactive Streamlit Dashboard

To view the analysis results interactively, please verify the data structure of the `dashboard` folder:

```plaintext
dashboard/
├── graphs/               # Download graphs from drive and place them here
├── pages/                
│   ├── 1_Overview.py     # Requires monthly_scores_summary.csv, topic_clusters.csv, top10_topics.csv
│   ├── 2_Detailed_Analysis.py  # Requires graphs in graphs directory
├── scripts/              # Intermediate preprocessing scripts, run in root directory
│   ├── home_topic.py     # Requires topic_clusters.csv, generate dashboard_topic_metrics.json
│   ├── time_metrics.py   # Requires combined_data_scores.csv, generate hourly_metrics.csv, daily_metrics.csv, peak_hours.csv
├── Home.py               # Requires monthly_summary.csv, hourly_metrics.csv, daily_metrics.csv, peak_hours.csv, dashboard_topic_metrics.json
├── requirements.txt      # Ensure packages are installed
```

And launch the Streamlit dashboard from the project’s root directory:

```bash
streamlit run dashboard/Home.py
```
