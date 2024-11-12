# Technical Report

**Project: Singapore Subreddits Toxicity Analysis**  
**Members: Bernice Ong Hwee Yee, Cao Han, Luo Xinming, Su Xuanxuan, Yang Shu Ting**  
Last updated on 13/11/2024

## Section 1: Context

The Ministry of Digital Development and Innovation's (MDDI) Online Trust and Safety Department initiated this project to address the growing concern over increasing toxicity and hate speech on social media. Recent data from MDDI’s Online Safety Poll showed a rise in harmful content exposure, with 66% of respondents encountering such content, up from 57% the previous year. This is particularly concerning for a diverse society like Singapore, where children are especially vulnerable to online toxicity.

MDDI has been working with social media platforms like Meta, Google, and TikTok to combat this issue, but a more comprehensive data-driven study was needed to assess the extent of the problem. This project focuses on analysing Singapore-specific subreddits (r/Singapore, r/SingaporeRaw, r/SingaporeHappenings) to understand the rise in toxic content over the past few years. The goal is to identify patterns and drivers of hatefulness and toxicity, providing actionable insights for future policy decisions. Armed with these insights, MDDI aims to collaborate more effectively with social media platforms to develop interventions that can mitigate the spread of harmful content.

## Section 2: Scope

### 2.1 Problem

The key business problem faced by the Online Trust and Safety Department at MDDI is the increasing volume of toxic and hateful content on social media platforms, specifically on Singapore-related subreddits. This issue is particularly urgent due to the 66% increase in reports of harmful content from users, up from 57% in the previous year. This growing trend hampers the department’s ability to ensure online safety, especially for vulnerable populations like children. The increase in such content poses a social risk by encouraging divisiveness in a multi-ethnic, multi-religious society, potentially escalating societal tensions.

If not addressed, this problem can lead to further polarisation of public opinion, diminish trust in social platforms, and create an unsafe online environment. The long-term consequence could be widespread societal harm, especially for young people who are frequently exposed to this content. Furthermore, MDDI faces challenges in manually monitoring the sheer volume of posts and discussions across platforms, which makes automation critical.

Thus, data science and machine learning will be appropriate solutions because they can automate the analysis of large-scale social media data, providing insights that can help identify trends, flag harmful content, and determine the key drivers behind the rise in toxicity. Natural Language Processing (NLP) models can help classify and quantify toxic content, offering an accurate, scalable, and objective method to tackle this problem.

### 2.2 Success Criteria

Success for this project will be measured using two key performance indicators (KPIs):

1. Actionable Insights and Policy Recommendations: The project aims to identify at least two critical drivers or topics contributing to the rise in toxicity within Singapore-related subreddits. Insights derived will inform specific recommendations for MDDI, enabling them to implement targeted interventions to reduce harmful content exposure, especially for vulnerable groups. This KPI will demonstrate the project’s effectiveness in generating insights that directly support MDDI’s policy-making efforts.

2. Reduction in Toxic Discourse: Achieving a 20% decrease in toxic discourse within Singapore-related subreddits over the next year will indicate success in mitigating harmful content. This metric will be assessed through a year-over-year comparison of average toxicity scores across all relevant comments, highlighting the impact of MDDI’s interventions informed by the project’s findings.

Regular monitoring in collaboration with MDDI will validate these KPIs, showcasing the project’s role in enhancing online safety and reducing exposure to harmful content.

### 2.3 Assumptions

One important assumption is that social media platforms, particularly Reddit, will collaborate with MDDI in applying the findings of this analysis to enforce policies and reduce toxic content. Without platform cooperation, the impact of the project’s recommendations could be limited.

Another assumption is that MDDI will have adequate resources to train and support personnel tasked with implementing the recommendations. Without this, there could be delays or gaps in effectiveness, affecting the timeliness and impact of the project.

## Section 3: Methodology

### 3.1 Technical Assumptions

For this project, several technical assumptions guide the methodology:

Toxicity and hate speech are defined based on the context of the project. Toxicity refers to content that is rude, disrespectful, or otherwise likely to make someone leave a discussion, while hate speech refers to content that promotes violence or prejudice against individuals or groups based on race, ethnicity, religion, gender, sexual orientation, or other protected characteristics. Hate speech is considered a subset of toxicity, meaning that while all hate speech is toxic, not all toxic content qualifies as hate speech. Therefore, we will primarily model toxicity scores, while acknowledging that hate detection may require additional analysis. These scores range from 0 to 1, where a higher score indicates more harmful or disrespectful language. Toxicity scores quantify the level of toxic discourse in the text and will be used to measure and track toxicity trends in Singapore-specific subreddits.

The dataset includes text (Reddit comments), timestamps, usernames and metadata (links, subreddit IDs, moderation). Only the text field is used for toxicity detection and topic modelling, as it contains the linguistic content of interest. Moreover, we assume that the absence of the original thread text will not significantly hinder the investigation.

The analysis relies on cloud-based and on-premise computational resources, with the assumption of access to free online GPUs to handle large-scale data processing using transformer-based models like HateBERT and HateXplain. We also assume that the available RAM is sufficient for batch processing up to 5 million rows, allowing the use of efficient data-handling techniques.

Due to resource constraints, we are limited to using free models available on platforms like HuggingFace, ruling out paid services such as the Perspective API or OpenAI API. This affects our model selection, as only free models are considered for toxicity and hate speech detection.

Our key hypotheses propose that toxicity levels have risen over the past four years in Singapore-specific subreddits, particularly around certain topics like politics, race, and religion. We aim to examine if this increase in toxicity aligns with a higher volume of news reports involving crimes committed by foreigners, potentially fueling public dissatisfaction and hostility toward foreign nationals. Additionally, we hypothesise that growing toxicity could be linked to increasingly polarised views on LGBTQ+ issues, potentially influenced by religious beliefs and a rise in outspoken opposition toward the LGBTQ+ community.

The dataset, although complete for comment texts, contains linguistic variations (e.g. mixed languages, slang, spelling errors), but these are manageable using pre-trained NLP models. Additionally, we will account for comments that are removed or deleted during the preprocessing stage.

### 3.2 Data

The data for this project comprises Reddit comments from Singapore-specific subreddits such as r/Singapore, r/SingaporeRaw, and r/SingaporeHappenings. Data was provided by MDDI, focusing on posts and comments from 2020 to 2023 to track toxicity trends over recent years. For each comment, metadata such as the timestamp, username, subreddit ID, and moderation status were given, although the actual analysis will focus primarily on the `text` content.

To ensure a high-quality dataset, we performed several cleaning steps. We dropped rows with missing values and removed entries with deleted or removed comments, ensuring only usable data remained for analysis. In this project, we did not perform tokenisation as a separate step since we relied on pre-trained transformer models that automatically handle tokenisation as part of their processing. This allowed us to streamline the data processing pipeline and leverage the sophisticated tokenisation built into these models, ensuring that the text inputs were prepared in a way that optimises model performance and coherence analysis without requiring additional pre-processing. Several features were also engineered to enhance the data’s analytical value. Specifically, we extracted a `yearmonth` field from `timestamp` to analyse toxicity trends over time, isolated post titles from the link field for potential topic alignment, and added an `index` field as a unique identifier, simplifying the processing of data through our NLP models. The relevant code can be found in `src/data_processing.ipynb`.

Rather than splitting the data, we applied pre-trained NLP models directly to the entire cleaned dataset to gain insights. To evaluate the topic modeling results, we used a sample of one month’s data (`2023-10`) to calculate the coherence score, ensuring our topic modeling maintained interpretability and consistency across topics. 

### 3.3 Experimental Design

#### Toxicity Scores
Our model development process involved experimenting with various NLP algorithms to detect toxicity levels and uncover topic trends across Reddit comments. Given our focus on detecting nuanced language patterns and toxic behaviour, we chose transformer-based models such as HateBERT, HateXplain, and ToxicBERT, which are specifically fine-tuned for handling toxic language on social media and online forums and hence closely aligns with the characteristics of our dataset. Reddit is known for its conversational, often informal, and sometimes contentious style of discussion, which these models are well-equipped to handle due to their training on similar datasets. These models were also selected based on their ability to handle the complexities of such online discourse, including slang, sarcasm, and mixed languages. The relevant codes can be found under `src/toxicity models`. In addition, averaging the toxicity scores across these three models provides a more reliable estimate, reducing biases associated with any one model’s classification tendencies. The implementation of the averaging can be found in `src/data_processing.ipynb`.

#### Topic Modelling
For topic modelling, we opted for BERTopic instead of more traditional algorithms like Latent Dirichlet Allocation (LDA) to identify and analyse discussion topics within Reddit comments for each `yearmonth` across our dataset. By examining each `yearmonth` separately, we could observe how certain topics and themes evolved over time, enabling us to pinpoint when and where toxicity levels might have surged and uncover any patterns in discourse contributing to this increase. BERTopic was chosen because it leverages transformer-based embeddings, allowing it to capture contextual nuances and generate coherent topics from unstructured text. This approach was particularly valuable for identifying the thematic trends that contribute to online toxicity in Singapore-specific subreddits. 

More specifically, we chose the `KeyBERTInspired` representation model because it focuses on extracting key phrases from each topic in a way that emphasises contextual relevance. This model allowed us to generate coherent and meaningful phrases representative of user discussions, aligning well with the informal and conversational style of Reddit comments. We also set `nr_topics` to `auto` to dynamically reduce the number of topics and improve interpretability. This setting automatically merges similar topics, allowing us to avoid manually tuning the topic count and instead focusing on distinct, meaningful themes. The implementation can be found in `src/topic models/topic_modelling.ipynb`.

To ensure the quality and relevance of the extracted topics, we used a coherence score as our evaluation metric. Coherence scores indicate the degree to which the words within each topic are semantically related, providing a measure of the interpretability and meaningfulness of the topics.
For this, we used a sample month’s data (`2023-10`) to evaluate the coherence of the topic model, as calculating coherence for every month would be computationally intensive. This sample provided a benchmark for assessing how well the topic model captured meaningful patterns in Reddit discussions. The evaluation can also be found in `src/topic models/topic_modelling.ipynb`.

#### Topic Clustering
To analyse toxicity across different themes within Reddit posts, related topics are grouped into clusters with the in-cluster toxicity level over time examined. This process consists of four main steps. First, textual topic data are converted into TF-IDF vectors to capture the importance of terms while considering both individual words and bigrams. Then, nearest neighbor analysis with cosine similarity is used to identify similar topics based on vectorized keywords. The next step is building a graph where nodes represent topics and edges represent high-similarity relationships, following which community detection algorithms are applied to this network to reveal clusters of related topics, i.e. the semantic clusters. The implementation can be found in `src/topic models/topic_clustering.ipynb`.

To ensure the quality and relevance of the clusters, we used **topic diversity** as an additional evaluation metric. Topic diversity measures the range of unique keywords within each cluster, giving us a sense of how broad or specific each cluster is. Our analysis showed a mean topic diversity score of 2.31, which suggests that clusters contain a fairly diverse set of terms. This diversity allows each cluster to capture a broad range of ideas while still being coherent, as reflected by the coherence scores. By including topic diversity, we can better understand if our clusters are well-balanced in representing both focused and broader themes. This evaluation can also be found in `src/topic models/topic_clustering.ipynb`.

## Section 4: Findings

### 4.1 Results

While the overall toxicity scores across the three subreddits remain relatively low at around 0.06, there is a gradual increase from 2020 to 2023, with a significant spike in October 2023. 

![Figure 1. Overall Toxicity Trend](<images/Overall Toxicity Trend.png>)

After the topic clustering step, we calculate the average toxicity scores for posts within each cluster. Certain themes, such as "police" and "drugs," are notably associated with higher toxicity. Interestingly, seemingly neutral themes like "football" and "jokes" also appear among the top 10 clusters with elevated toxicity levels.

![Table 1. Top 10 Toxic Topic Clusters](<images/top10 table.png>)

Examining the toxicity trends across different clusters, we find that topics related to **wages (Cluster 28)** and **LGBTQ+ issues (Cluster 31)** consistently show elevated toxicity scores. Notably, LGBTQ+-related topics display a rising trend in toxicity over time, as seen in the increasing peaks of the light-blue line. 

![Figure 2. Toxicity Evolution of Top 10 Toxic Topics](<images/top10 time graph.png>)

In our chosen configuration, the coherence score for October 2023 was 0.33, reflecting moderate alignment between extracted topics and actual themes. This indicates that while the model successfully identified meaningful, though somewhat broad, relationships among topic words, there remains room for further tuning. Nonetheless, this score offers a reasonable baseline for our initial analysis.

| Model   | Representation Model | Total Number of Topics | Total Number of Useful Topics | Coherence Score |
| :---:   | :----:               | :----:                 | :----:                        | :----:          |
| BERTopic| KeyBERTInspired      | 800                    | 56                            | 0.33            |

### 4.2 Discussion

In this section, we will interpret the results in terms of business value, addressing how the toxicity scoring impacts MDDI’s Online Trust and Safety department and other stakeholders. Additionally, we will examine aspects like interpretability, fairness, and deployability, providing a well-rounded view of the implications of the findings to policy-making.
#### Translating Technical Metrics to Business Value
Our findings show a gradual increase in toxicity across subreddits, with specific themes like "crime," "LGBTQ," "politics," and "race" frequently associated with higher toxicity scores, and a notable spike in October 2023. These scores provide a detailed understanding of toxic discourse, highlighting areas with the highest risk. This nuanced scoring allows MDDI to pinpoint content that could be more harmful, helping protect children and vulnerable groups on social media through targeted policy interventions.

Implementing Large Language Models (LLMs) has high computational costs, as it requires processing and scoring each comment rather than simply flagging content. However, this nuanced approach provides richer insights that justify the investment, as MDDI can focus resources on the most toxic areas, minimising social costs associated with unchecked online toxicity.
#### Interpretability
Understanding why certain topics, like "religion" and "employment," correlate with high toxicity scores is vital for actionable insights. Topic modelling helps identify specific words and phrases contributing to toxicity, which enables policymakers to understand not only if content is harmful but why it might be harmful. This interpretability is essential for creating well-informed, data-driven policies to keep online spaces safe.

Furthermore, the model’s ability to identify specific themes and language patterns driving toxicity allows MDDI to craft more focused interventions. For instance, policies may now address harmful discussions around sensitive societal themes identified in our findings.
#### Fairness
Fairness is critical in toxicity scoring, especially in a multicultural and multiracial context like Singapore.
The models could inadvertently assign higher toxicity scores to certain comments with specific words if they are not trained across diverse language styles and cultural expressions. This is particularly relevant in Singapore, where language can vary significantly across ethnic groups. For instance, the use of Singlish words in different contexts can have vastly different meaning.
#### Deployability
The model’s continuous scoring allows MDDI to monitor toxicity trends periodically, which proves to be a useful tool that scales to changing trends. This would be valuable for MDDI’s ongoing efforts, as the model could be integrated with other social media platforms for real-time analysis.

The model should also be retrained periodically to stay current with linguistic trends and shifts in online behaviour. Regular updates like this ensure the model remains relevant, capturing new forms of toxic language as they emerge and accurately assessing nuanced expressions unique to the local context.

By integrating this model alongside existing moderation policies on Reddit, MDDI could enhance overall safety with minimal operational overhead. Toxicity scores could inform moderators of the subreddit on varying levels of moderation, targeting the most harmful content while maintaining platform engagement.

With these results and considerations, our toxicity scoring and topic modelling methods effectively addresses the business problem by providing MDDI’s Online Trust and Safety department with actionable insights into the severity and drivers of toxic content over time. This allows the department to make data-informed policy recommendations and foster collaboration with Reddit and the general public to mitigate online harm at various toxicity levels.

### 4.3 Recommendations

Given our findings, we recommend several next steps to further MDDI’s objective of creating a safer online space, particularly on Reddit. These recommendations are focused on deploying the model, enhancing data quality, and improving support for affected communities.
#### 1. Deploy the Model to Flag Toxic Comments Exceeding a Threshold
Firstly, we would recommend implementing this model in a production environment to automatically flag comments exceeding a toxicity threshold. This would allow real-time monitoring of harmful content. The flagged comments could be reviewed by moderators or automatically sent to platform administrators for additional scrutiny. This process can also inform further discussions with Reddit about monitoring toxic content and refining their moderation practices. By identifying trends in toxicity scores over time and across different topics, MDDI can also make more informed decisions on which content types, user groups, or subreddits may have higher probability of having high toxicity score and thus need enhanced monitoring. The scores provide guidance for working with Reddit to develop tools that address different toxicity levels, enhancing online safety in Singapore.
#### 2. Implement Age Limit Verification
Given the prevalence of toxic content and the particular risk it poses to younger audiences, implementing an age limit verification feature on these subreddits or urging Reddit to do so would help shield minors from harmful content. This feature could prompt users to confirm their age before accessing certain threads with higher probability of high toxicity score, thereby potentially reducing exposure among younger demographics.
#### 3. Establish a Support Hotline for Minority Groups
Our analysis shows that the LGBTQ+ community as well as foreigners may be disproportionately affected by toxic content. Setting up an integrated platform where minority group members can provide feedback, report content, or seek support would create a channel for direct communication and assistance. This platform could offer psychological support and practical resources for anyone affected by hate speech or needs someone to talk to about their experiences on Reddit. 
#### 4. Integrate Real-Time Monitoring with Reddit via API
Making API calls to Reddit to obtain real-time data on toxicity would allow for a continuous, updated analysis of trends and behaviours on Singapore subreddits. This integration would provide MDDI with a real time update of relevant data and enable more timely interventions.
#### 5. Public Service Announcement (PSA) for Elevated Toxicity Levels
If the model detects a sustained increase in toxicity over time, a parliamentary address could be made to raise awareness about the issue and encourage respectful discourse. Such a discourse could emphasise the importance of digital responsibility, especially in sensitive discussions affecting public morale. This approach helps manage public perception and actively reminds users of the importance of positive online behaviour.

#### Possible Future Enhancements
##### 1. Parameter Tuning on BERTopic Model
As mentioned in Section 4.1, the initial coherence score of 0.33, though fair and sufficient for capturing key topic structures, left some room for improvement. To enhance topic coherence, we experimented with parameter tuning on the BERTopic Model again using data from (`2023-10`) as a sample. We adjusted key parameters within the vectorizer model, dimensionality reduction via UMAP, and clustering thresholds. By modifying `min_df`, `max_df`, and the `ngram_range` for the vectorizer, we targeted a balance between general and specific terms. Similarly, adjustments to `n_neighbors` and `min_dist` in UMAP helped create more distinct clusters, enhancing interpretability. This configuration has helped the coherence score increase to 0.42 and the implementation can be found in `src/topic models/parameter_tuning.ipynb`.

However, due to the large size of the dataset and time constraints, we chose not to apply the revised configuration across the entire dataset. Running the full tuning process for every subset would be computationally intensive, potentially requiring substantial processing time and resources beyond our current capacity. The current coherence score of 0.33 strikes a practical balance between specificity and efficiency for our initial analysis.
##### 2. Fine-tune Models to Singapore-Specific Context
One important limitation of the current model is that it may not be fully tailored to Singapore’s linguistic and cultural context. For instance, language nuances, slang, or dialectal expressions unique to Singapore may be misclassified as toxic or go unrecognised. Future work could involve fine-tuning the models for local language variants such as Singlish to better understand and appropriately score context-specific expressions that may carry different connotations in Singapore. To ensure that the toxicity scoring model is fair, we could periodically retrain the model with balanced, representative data. Using fairness metrics, we can help ensure that the model does not unfairly target specific comments. This approach minimises undue censorship and promotes equitable toxicity scoring across all comments. Additionally, experimenting with models specifically trained on multilingual data may help mitigate bias and improve fairness. To improve the coherence score of our topic models, we can preprocess text data more thoroughly, such as by removing irrelevant words, filtering out extreme frequencies, and using n-grams or phrases. Additionally, we can also tune the hyperparameters, such as alpha, beta, and eta, to control the prior distributions of the topics and words. 
##### 3. Improving Data Quality and Availability
Access to original Reddit thread content (currently unavailable) would allow the model to better understand the context of toxic comments. Future partnerships with Reddit could focus on enabling this level of access.

Even though the potential IT costs of deploying and integrating the model may be high, we believe that it is a worthwhile investment as it provides useful insights to analyse toxcity changes on these Singapore subreddits. By following these recommendations, MDDI can maximize the business value of this project and continue to make strides toward a safer online environment for Singapore’s Reddit users, especially the younger audience.
