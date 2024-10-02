- rank prediction involves predicting a continuous output or an ordinal label
- To handle this, you would typically use a **neural network with multiple layers**
- predicting ranks is harder as the score distribution may be dense at certain ranges, leading to prediction un-certainities
- often, non-linear relationships where small score improvements at the top can lead to significant rank jumps
- In some cases, ranks might be divided into categories (e.g., top 1%, top 5%, etc.), making it a classification problem
- rank prediction is a classification problem
### Advantages of Using Neural Networks for Rank Prediction:
- Non-linear Relationships: Neural networks can capture complex, non-linear relationships between features and ranks.
- Scalability: MLPs can be scaled with more layers to handle more sophisticated rank prediction problems.
- Flexibility: Neural networks can be trained for both continuous rank prediction (regression) and ordinal rank prediction (classification).
## Modal tanning
- ordinal labels
- data cleaning
- data normalize or scale features
- linear regression (Ordinal regression) or Gradient boosting algorithms (XGBoost, LightGBM)
- how to find the ranking loss?
# Questions
## How does a student score relates to score?
## How to know does distribution of marks happens?
## What are the factors contributing to rank?
## Why does the rank prediction will not supported with unsupervised learning?
- Rank prediction requires specific output labels (ranks), so it doesn't fit the unsupervised learning category where labels aren’t provided.
- Unsupervised learning is more suited for tasks like clustering or anomaly detection, where the goal is to identify patterns without predefined outcomes.

#### Reference
[error in rank predictor model](https://www.youtube.com/watch?v=5ZtCh0k9jd0)
[document to understand information retrievalz](https://web.stanford.edu/class/cs276/handouts/lecture14-learning-ranking.pdf)
[research paper](https://www.ijraset.com/best-journal/student-performace-pediction-using-ml-and-ai)
[research paper](https://link.springer.com/article/10.1007/s10462-022-10155-y)
[article](https://www.ai.codersarts.com/post/predicting-entrance-exam-ranks-and-college-admissions-with-machine-learning)
[article](https://indiaai.gov.in/article/ai-can-now-predict-a-student-s-grade-without-an-exam)
[article](https://towardsdatascience.com/learning-to-rank-a-complete-guide-to-ranking-using-machine-learning-4c9688d370d4)