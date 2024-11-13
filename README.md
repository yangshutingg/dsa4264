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

## Running the Interactive Streamlit Dashboard

To view the analysis results interactively, launch the Streamlit dashboard from the project’s root directory:

```bash
cd dashboard
streamlit run Home.py
```
