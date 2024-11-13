# Singapore Subreddits Toxicity Analysis  
Members: Bernice Ong Hwee Yee, Cao Han, Luo Xinming, Su Xuanxuan, Yang Shu Ting

## Project Overview
This project focuses on analyzing toxicity (Content that is rude, disrespectful, or otherwise likely to make someone leave a discussion) in Singapore Subreddits text data to uncover insights and patterns. Using natural language processing (NLP) techniques, we process, analyze, and visualize text data to identify sentiment trends and key topic clusters.

## Data Access
To run the entire project, you should have minially a raw data file that contains three columns, `timestamp`, `link`, `text` and is saved in your own `data` subfolder. If you just want to run a specific script, ensure that you have access to the necessary (intermediate) data. 

The raw data used in this project is not publicly available due to ownership restrictions. If you would like access to the data, please reach out directly to the data owner or organization responsible. If you have specific questions about the data or need processed examples for testing, feel free to open an issue in this repository, and we will do my best to assist within the guidelines allowed.

Thank you for understanding!


## Results
After running the analysis, key findings and visualizations are available in the dashboard folder. These include:

- Topic clusters and keywords
- Sentiment trends over time
- Topic networks clouds

## Installation
To get started, clone this repository and install the required packages:

```bash
git clone https://github.com/yangshutingg/dsa4264.git
cd dsa4264
pip install -r dashboard/requirements.txt
```

## How to Run the Interactive Streamlit Dashboard

To visualize the analysis results, you can run the interactive Streamlit dashboard. If you are in the root directory of the project:

```bash
cd dashboard
streamlit run Home.py
```
