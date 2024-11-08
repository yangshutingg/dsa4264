# Technical Report

**Project: {insert project name}**  
**Members: Bernice Ong Hwee Yee, Cao Han, Luo Xinming, Su Xuanxuan, Yang Shu Ting**  
Last updated on 28/10/2024

## Section 1: Context

*In this section, you should explain how this project came about. Retain all relevant details about the project’s history and context, especially if this is a continuation of a previous project.*

*If there are any slide decks or email threads that started before this project, you should include them as well.*

The Ministry of Digital Development and Innovation's (MDDI) Online Trust and Safety Department initiated this project to address the growing concern over increasing toxicity and hate speech on social media. Recent data from MDDI’s Online Safety Poll showed a rise in harmful content exposure, with 66% of respondents encountering such content, up from 57% the previous year. This is particularly concerning for a diverse society like Singapore, where children are especially vulnerable to online toxicity.

MDDI has been working with social media platforms like Meta, Google, and TikTok to combat this issue, but a more comprehensive data-driven study was needed to assess the extent of the problem. This project focuses on analysing Singapore-specific subreddits (r/Singapore, r/SingaporeRaw, r/SingaporeHappenings) to understand the rise in toxic content over the past few years. The goal is to identify patterns and drivers of hatefulness and toxicity, providing actionable insights for future policy decisions. Armed with these insights, MDDI aims to collaborate more effectively with social media platforms to develop interventions that can mitigate the spread of harmful content.

## Section 2: Scope

### 2.1 Problem

*In this subsection, you should explain what is the key business problem that you are trying to solve through your data science project. You should aim to answer the following questions:*

* *What is the problem that the business unit faces? Be specific about who faces the problem, how frequently it occurs, and how it affects their ability to meet their desired goals.*
* *What is the significance or impact of this problem? Provide tangible metrics that demonstrate the cost of not addressing this problem.*
* *Why is data science / machine learning the appropriate solution to the problem?*

The key business problem faced by the Online Trust and Safety Department at MDDI is the increasing volume of toxic and hateful content on social media platforms, specifically on Singapore-related subreddits. This issue is particularly urgent due to the 66% increase in reports of harmful content from users, up from 57% in the previous year. This growing trend hampers the department’s ability to ensure online safety, especially for vulnerable populations like children. The increase in such content poses a social risk by encouraging divisiveness in a multi-ethnic, multi-religious society, potentially escalating societal tensions.

If not addressed, this problem can lead to further polarisation of public opinion, diminish trust in social platforms, and create an unsafe online environment. The long-term consequence could be widespread societal harm, especially for young people who are frequently exposed to this content. Furthermore, MDDI faces challenges in manually monitoring the sheer volume of posts and discussions across platforms, which makes automation critical.

Thus, data science and machine learning will be appropriate solutions because they can automate the analysis of large-scale social media data, providing insights that can help identify trends, flag harmful content, and determine the key drivers behind the rise in toxicity. Natural Language Processing (NLP) models can help classify and quantify toxic content, offering an accurate, scalable, and objective method to tackle this problem.

### 2.2 Success Criteria

*In this subsection, you should explain how you will measure or assess success for your data science project. You need to specify at least 2 business and/or operational goals that will be met if this project is successful. Business goals directly relate to the business’s objectives, such as reduced fraud rates or improved customer satisfaction. Operational goals relate to the system’s needs, such as better reliability, faster operations, etc.*

Success for this project will be measured using two key performance indicators (KPIs):

1. Actionable Insights and Policy Recommendations: The project aims to identify at least two critical drivers or topics contributing to the rise in toxicity within Singapore-related subreddits. Insights derived will inform specific recommendations for MDDI, enabling them to implement targeted interventions to reduce harmful content exposure, especially for vulnerable groups. This KPI will demonstrate the project’s effectiveness in generating insights that directly support MDDI’s policy-making efforts.

2. Reduction in Toxic Discourse: Achieving a 20% decrease in toxic discourse within Singapore-related subreddits over the next year will indicate success in mitigating harmful content. This metric will be assessed through a year-over-year comparison of average toxicity scores across all relevant comments, highlighting the impact of MDDI’s interventions informed by the project’s findings.

Regular monitoring in collaboration with MDDI will validate these KPIs, showcasing the project’s role in enhancing online safety and reducing exposure to harmful content.

### 2.3 Assumptions

*In this subsection, you should set out the key assumptions for this data science project that, if changed, will affect the problem statement, success criteria, or feasibility. You do not need to detail out every single assumption if the expected impact is not significant.*

*For example, if we are building an automated fraud detection model, one important assumption may be whether there is enough manpower to review each individual decision before proceeding with it.*

One important assumption is that social media platforms, particularly Reddit, will collaborate with MDDI in applying the findings of this analysis to enforce policies and reduce toxic content. Without platform cooperation, the impact of the project’s recommendations could be limited.

Another assumption is that MDDI will have adequate resources to train and support personnel tasked with implementing the recommendations. Without this, there could be delays or gaps in effectiveness, affecting the timeliness and impact of the project.

## Section 3: Methodology

### 3.1 Technical Assumptions

*In this subsection, you should set out the assumptions that are directly related to your model development process. Some general categories include:*
* *How to define certain terms as variables*
* *What features are available / not available*
* *What kind of computational resources are available to you (ie on-premise vs cloud, GPU vs CPU, RAM availability)*
* *What the key hypotheses of interest are*
* *What the data quality is like (especially if incomplete / unreliable)*

For this project, several technical assumptions guide the methodology:

Toxicity and hate speech are defined based on the context of the project. Toxicity refers to content that is rude, disrespectful, or otherwise likely to make someone leave a discussion, while hate speech refers to content that promotes violence or prejudice against individuals or groups based on race, ethnicity, religion, gender, sexual orientation, or other protected characteristics. Hate speech is considered a subset of toxicity, meaning that while all hate speech is toxic, not all toxic content qualifies as hate speech. Therefore, we will primarily model toxicity scores, while acknowledging that hate detection may require additional analysis. These scores range from 0 to 1, where a higher score indicates more harmful or disrespectful language. Toxicity scores quantify the level of toxic discourse in the text and will be used to measure and track toxicity trends in Singapore-specific subreddits.

The dataset includes text (Reddit comments), timestamps, usernames and metadata (links, subreddit IDs, moderation). Only the text field is used for toxicity detection and topic modelling, as it contains the linguistic content of interest. Moreover, we assume that the absence of the original thread text will not significantly hinder the investigation.

The analysis relies on cloud-based and on-premise computational resources, with the assumption of access to free online GPUs to handle large-scale data processing using transformer-based models like HateBERT and HateXplain. We also assume that the available RAM is sufficient for batch processing up to 5 million rows, allowing the use of efficient data-handling techniques.

Due to resource constraints, we are limited to using free models available on platforms like HuggingFace, ruling out paid services such as the Perspective API or OpenAI API. This affects our model selection, as only free models are considered for toxicity and hate speech detection.

**(to add on more focused questions for hypothesis)**
We hypothesise that hate speech and toxicity have increased in Singapore-specific subreddits over the years and that specific topics (e.g. political, racial or religious content) may exacerbate such behaviors. 

The dataset, although complete for comment texts, contains linguistic variations (e.g. mixed languages, slang, spelling errors), but these are manageable using pre-trained NLP models. Additionally, we will account for comments that are removed or deleted during the preprocessing stage.

### 3.2 Data

*In this subsection, you should provide a clear and detailed explanation of how your data is collected, processed, and used. Some specific parts you should explain are:*
* *Collection: What datasets did you use and how are they collected?*
* *Cleaning: How did you clean the data? How did you treat outliers or missing values?*
* *Features: What feature engineering did you do? Was anything dropped?*
* *Splitting: How did you split the data between training and test sets?*

The data for this project comprises Reddit comments from Singapore-specific subreddits such as r/Singapore, r/SingaporeRaw, and r/SingaporeHappenings. Data was provided by MDDI, focusing on posts and comments from 2020 to 2023 to track toxicity trends over recent years. For each comment, metadata such as the timestamp, username, subreddit ID, and moderation status were given, although the actual analysis will focus primarily on the `text` content.

To ensure a high-quality dataset, we performed several cleaning steps. We dropped rows with missing values and removed entries with deleted or removed comments, ensuring only usable data remained for analysis. In this project, we did not perform tokenisation as a separate step since we relied on pre-trained transformer models that automatically handle tokenisation as part of their processing. This allowed us to streamline the data processing pipeline and leverage the sophisticated tokenisation built into these models, ensuring that the text inputs were prepared in a way that optimises model performance and coherence analysis without requiring additional pre-processing. Several features were also engineered to enhance the data’s analytical value. Specifically, we extracted a `yearmonth` field from `timestamp` to analyse toxicity trends over time, isolated post titles from the link field for potential topic alignment, and added an `index` field as a unique identifier, simplifying the processing of data through our NLP models. The relevant code can be found in `src/data_processing.ipynb`.

Rather than splitting the data, we applied pre-trained NLP models directly to the entire cleaned dataset to gain insights. To evaluate the topic modeling results, we used a sample of one month’s data (`2023-10`) to calculate the coherence score, ensuring our topic modeling maintained interpretability and consistency across topics. 

### 3.3 Experimental Design

*In this subsection, you should clearly explain the key steps of your model development process, such as:*
* *Algorithms: Which ML algorithms did you choose to experiment with, and why?*
* *Evaluation: Which evaluation metric did you optimise and assess the model on? Why is this the most appropriate?*
* *Training: How did you arrive at the final set of hyperparameters? How did you manage imbalanced data or regularisation?*

- Why we chose HateBERT, HateXplain, ToxicBert -> why average the score
- Why we chose BERTopic instead of LDA -> why we choose certain parameters in BERTopic
    - evaluate by coherence score, quality of topics

Our model development process involved experimenting with various NLP algorithms to detect toxicity levels and uncover topic trends across Reddit comments. Given our focus on detecting nuanced language patterns and toxic behaviour, we chose transformer-based models such as HateBERT, HateXplain, and ToxicBERT, which are specifically fine-tuned for handling toxic language on social media and online forums, which closely aligns with the characteristics of our dataset. Reddit is known for its conversational, often informal, and sometimes contentious style of discussion, which these models are well-equipped to handle due to their training on similar datasets. These models were also selected based on their ability to handle the complexities of such online discourse, including slang, sarcasm, and mixed languages. The relevant codes can be found under `src/toxicity models`. In addition, averaging the toxicity scores across these three models provides a more reliable estimate, reducing biases associated with any one model’s classification tendencies. The implementation of the averaging can be found in `src/data_processing.ipynb`.


For topic modelling, we opted for BERTopic instead of more traditional algorithms like Latent Dirichlet Allocation (LDA) to identify and analyse discussion topics within Reddit comments for each `yearmonth` across our dataset. By examining each `yearmonth` separately, we could observe how certain topics and themes evolved over time, enabling us to pinpoint when and where toxicity levels might have surged and uncover any patterns in discourse contributing to this increase. BERTopic was chosen because it leverages transformer-based embeddings, allowing it to capture contextual nuances and generate coherent topics from unstructured text. This approach was particularly valuable for identifying the thematic trends that contribute to online toxicity in Singapore-specific subreddits. 

More specifically, we chose the `KeyBERTInspired` representation model because it focuses on extracting key phrases from each topic in a way that emphasises contextual relevance. This model allowed us to generate coherent and meaningful phrases representative of user discussions, aligning well with the informal and conversational style of Reddit comments. We also set `nr_topics` to `auto` to dynamically reduce the number of topics and improve interpretability. This setting automatically merges similar topics, allowing us to avoid manually tuning the topic count and instead focusing on distinct, meaningful themes. The implementation can be found in `src/topic models/topic_modelling.ipynb`.

To ensure the quality and relevance of the extracted topics, we used a coherence score as our evaluation metric. Coherence scores indicate the degree to which the words within each topic are semantically related, providing a measure of the interpretability and meaningfulness of the topics.
For this, we used a sample month’s data (`2023-10`) to evaluate the coherence of the topic model, as calculating coherence for every month would be computationally intensive. This sample provided a benchmark for assessing how well the topic model captured meaningful patterns in Reddit discussions. The evaluation can also be found in `src/topic models/topic_modelling.ipynb`.

## Section 4: Findings

### 4.1 Results

*In this subsection, you should report the results from your experiments in a summary table, keeping only the most relevant results for your experiment (ie your best model, and two or three other options which you explored). You should also briefly explain the summary table and highlight key results.*

*Interpretability methods like LIME or SHAP should also be reported here, using the appropriate tables or charts.*

In our chosen configuration, the coherence score for October 2023 was 0.33, reflecting moderate alignment between extracted topics and actual themes. This indicates that while the model successfully identified meaningful, though somewhat broad, relationships among topic words, there remains room for further tuning. Nonetheless, this score offers a reasonable baseline for our initial analysis.

| Model               | Representation Model | Number of Topics | Coherence Score |
| :---                | :----:               | :----:           | :----:          |
| BERTopic            | KeyBERTInspired      | auto             | 0.33            |

From our results, common themes like “crime”, “LGBTQ”, “politics”, “immigration” and “race” is frequently associated with high toxicity scores. Surprisingly, seemingly benign words related to families such as “marriage”, “parenthood” and “pregnancy”. Overall, the 3 Subreddits have seen an increase in toxicity from 2020 to 2023, with a large spike in toxicity score in October 2023. 


### 4.2 Discussion

*In this subsection, you should discuss what the results mean for the business user – specifically how the technical metrics translate into business value and costs, and whether this has sufficiently addressed the business problem.*

*You should also discuss or highlight other important issues like interpretability, fairness, and deployability.*

### 4.3 Recommendations

*In this subsection, you should highlight your recommendations for what to do next. For most projects, what to do next is either to deploy the model into production or to close off this project and move on to something else. Reasoning about this involves understanding the business value, and the potential IT costs of deploying and integrating the model.*

*Other things you can recommend would typically relate to data quality and availability, or other areas of experimentation that you did not have time or resources to do this time round.*

Given our findings, we recommend several next steps to further MDDI’s objective of creating a safer online space, particularly on Reddit. These recommendations are focused on deploying the model, enhancing data quality, and improving support for affected communities.
1. Deploy the Model to Flag Toxic Comments Exceeding a Threshold
Firstly, we would recommend implementing this model in a production environment to automatically flag comments exceeding a toxicity threshold. This would allow real-time monitoring of harmful content. The flagged comments could be reviewed by moderators or automatically sent to platform administrators for additional scrutiny. This process can also inform further discussions with Reddit about monitoring toxic content and refining their moderation practices.
2. Implement Age Limit Verification
Given the prevalence of toxic content and the particular risk it poses to younger audiences, implementing an age limit verification feature on these subreddits or urging Reddit to do so would help shield minors from harmful content. This feature could prompt users to confirm their age before accessing certain threads with higher probability of high toxicity score, thereby potentially reducing exposure among younger demographics.
3. Establish a Support Hotline for Minority Groups
Our analysis shows that certain groups may be disproportionately affected by toxic content. Setting up an integrated platform where minority group members can provide feedback, report content, or seek support would create a channel for direct communication and assistance. This platform could offer psychological support and practical resources for anyone affected by hate speech or needs someone to talk to about their experiences on Reddit.
4. Public Service Announcement (PSA) for Elevated Toxicity Levels
If the model detects a sustained increase in toxicity over time, a parliamentary address could be made to raise awareness about the issue and encourage respectful discourse. Such a discourse could emphasize the importance of digital responsibility, especially in sensitive discussions affecting public morale. This approach helps manage public perception and actively reminds users of the importance of positive online behaviour.
5. Integrate Real-Time Monitoring with Reddit via API
Making API calls to Reddit to obtain real-time data on toxicity would allow for a continuous, updated analysis of trends and behaviours on Singapore subreddits. This integration would provide MDDI with a real time update of relevant data and enable more timely interventions.
6. Acknowledge Model Limitations, Especially Lack of Singapore-Specific Context
- One important limitation of the current model is that it may not be fully tailored to Singapore’s linguistic and cultural context. For instance, language nuances, slang, or dialectal expressions unique to Singapore may be misclassified as toxic or go unrecognized. Future work could involve training the model with more Singapore-specific data to enhance its accuracy and ensure fairer, more culturally appropriate results.
- give specific egs: low coherence score in topics, 

Possible Future Enhancements

1.	Improving Data Quality and Availability: Access to original Reddit thread content (currently unavailable) would allow the model to better understand the context of toxic comments. Future partnerships with Reddit could focus on enabling this level of access.
2.	Experiment with Different Models or Thresholds: Further testing with alternative models and adjusting thresholds for toxicity may yield even more accurate results. Additionally, experimenting with models specifically trained on multilingual data may help mitigate bias and improve fairness.
By following these recommendations, MDDI can maximize the business value of this project and continue to make strides toward a safer online environment for Singapore’s Reddit users.
