import streamlit as st
import json
from streamlit.components.v1 import html
import pandas as pd

# Define custom CSS for the recommendation container
st.markdown("""
    <style>
    .recommendation-container {
        background-color: #f0f0f0; /* light grey */
        padding: 15px;
        border-radius: 8px;
        margin-top: 15px;
        font-size: 1.1em;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("Reddit Content Analysis: Topic Deep Dive")

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
        
        **Correlation Score**: The correlation score represents the strength of the relationship between topics.
        Higher scores indicate a stronger association between topics, suggesting that discussions in one topic
        may influence or correlate with discussions in another.
        """)

    # Create two main columns: one for stacked graphs and one for recommendations
    left_col, right_col = st.columns([3, 1])  # Left column wider than right column

    with left_col:
        tab1, tab2 = st.tabs(["Topic Relationship Tree", "Topic Relationship Trends Over Time"])

        with tab1:
            st.image('dashboard/graphs/police_tree.png', use_column_width=True)  # Fallback to static image

        with tab2:
            st.image('dashboard/graphs/police_temporal.png', use_column_width=True)

    with right_col:
    # Create tabs for insights and recommendations
        tab1, tab2 = st.tabs(["Insights", "Recommendations"])

        with tab1:
            st.markdown("""
            **Insights:**
            - High toxicity peaks are observed around **"Cops, Policeman, Arrest"**, especially between 2020-2021, with moderate correlation to topics like **"Accusations"** and **"Drugs"**.
            - Other sensitive topics like **"Burns"** and **"Filming, CCTV"** are also highly connected to police discussions.
            """)

        with tab2:
            # Container for recommendations with grey background
            st.markdown("""
            **Recommendations for Police-related Discussions:**
            1. <strong>Monitor keywords</strong> related to arrests and police actions (e.g., "arrest," "use of force," "riot") during sensitive periods to flag inflammatory content.
            2. <strong>Address sensitive topics</strong> like police accountability with fact-checking initiatives and encourage constructive, respectful discussions on legal rights and policing.
            """, unsafe_allow_html=True)



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
        # Create Tabs for the left column (graphs)
        tab1, tab2 = st.tabs(["Topic Relationship Tree", "Topic Relationship Trends Over Time"])

        with tab1:
            st.image('dashboard/graphs/lgbtq_tree.png', use_column_width=True)

        with tab2:
            st.image('dashboard/graphs/lgbtq_temporal.png', use_column_width=True)

    with right_col:
    # Create tabs for insights and recommendations
        tab1, tab2 = st.tabs(["Insights", "Recommendations"])

        with tab1:
            st.markdown("""
            **Insights:**
            - High toxicity peaks are observed around **"Homosexual, Repeal, Homosexuality, Transgender"**, especially between 2020-2023, indicating heightened toxicity during sensitive events like legal debates on LGBTQ rights.
            - Topics such as **"Patriarchy, Masculinity, Feminists"**, **"Diversity, Racists, Ethnic"**, and **"Ballot, Voting, Voted"** show moderate correlation with LGBTQ discussions, suggesting connections to broader societal issues like gender equality and voting rights.
            """)

        with tab2:
            # Container for recommendations with grey background
            st.markdown("""
            **Recommendations for LGBTQ-related Discussions:**
            1. <strong>Monitor and moderate sensitive keywords</strong> related to LGBTQ topics (e.g., "homosexuality," "transgender," "gender rights") during high-intensity periods such as debates on LGBTQ rights.
            2. <strong>Promote respectful dialogue</strong> by providing factual information on LGBTQ issues like gender equality and transgender rights, and encourage community leaders to reduce harmful rhetoric.
            """, unsafe_allow_html=True)