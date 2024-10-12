- rank prediction involves predicting a continuous output or an ordinal label
- To handle this, you would typically use a **neural network with multiple layers**
- predicting ranks is harder as the score distribution may be dense at certain ranges, leading to prediction uncertainties
- often, non-linear relationships where small score improvements at the top can lead to significant rank jumps
- In some cases, ranks might be divided into categories (e.g., top 1%, top 5%, etc.), making it a classification problem
- rank prediction is a classification problem
- for rank prediction the **Predicted vs Actual** plot will show how close the predicted ranks are to the actual ranks, giving a visual check of accuracy.
- combining multiple exam scores into a single composite score
When we aim to **predict the rank of a student based on their NEET marks** we are essentially dealing with **regression problem** in the realm.

> [!NOTE] since we are predicting a continuous numerical value (this rank), this aligns with a regression framework. The model will learn to map NEET marks (and possibly other features) to a specific rank value.

[[Linear regression]] and [[ordinal regression]]
- Linear regression: A basic approach where you assume a linear relationship between NEET marks and rank.
- Ordinal regression: Given that ranks are ordered, ordinal regression techniques can be particularly effective. They account for the inherent order in the target variable without assuming equal intervals between ranks.
### Alternative approaches
- Classification: Although ranks are numerical, treating them as categories for classification isn't ideal because it ignores the ordinal nature of ranks. However, if the rank range is limited and you treat each rank as separate class, classification methods could be applied, but this is generally less effective for this scenario.
- Learning to Rank: this is more applicable in information retrieval systems where the goal is to order a set of items relative to each other based on some criteria. In your case, since you're predicting a single rank value for each student, traditional regression methods are more suitable.
### Ideal matrix 
- Mean Absolute Error (MAE): 250
- Root Mean Squared Error (RMSE): 300
- R-squared (R²): 0.85
### Visualization
- a histogram would show how scores are distributed across bins, while a box plot could highlight outliers or the spread between high and low scores. (bin size selection can distort the visualization).
- a Density plot is smoother then histogram, shows continuous distribution (may be harder to interpret for larger datasets).
- a box plot highlights outliers and data spread, easy to compare multiple distributions (doesn't show the exact distribution of data points within quadrilles).

> [!INFO] use histogram or density plot for initial distribution checks. And opt for box plots when dealing with multiple categories or to identify outliers.
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
- how to fine tune the data?
- These algorithms consider various factors such as **past academic records, extracurricular activities, and even personal statements to create a holistic view of each applicant**
# Questions (issues)
## How does a student score relates to score?
## How to know does distribution of marks happens?
## What are the factors contributing to rank?
## Can I use RAG in rank prediction?
## How to visualize relationships in the data?
## Why does the rank prediction will not supported with unsupervised learning?
- Rank prediction requires specific output labels (ranks), so it doesn't fit the unsupervised learning category where labels aren’t provided.
- Unsupervised learning is more suited for tasks like clustering or anomaly detection, where the goal is to identify patterns without predefined outcomes.
## Bench mark for the model
1. mean absolute error (MAE)
	1. R-squared
	2. Rank correlation coefficient
2. Random model
	1. linear regression
	2. xgboost

## Linear model rank prediction calculation
- the output might typically not a direct rank but rather a
#### Reference
[error in rank predictor model](https://www.youtube.com/watch?v=5ZtCh0k9jd0)
[document to understand information retrievalz](https://web.stanford.edu/class/cs276/handouts/lecture14-learning-ranking.pdf)
[research paper](https://www.ijraset.com/best-journal/student-performace-pediction-using-ml-and-ai)
[research paper](https://link.springer.com/article/10.1007/s10462-022-10155-y)
[article](https://www.ai.codersarts.com/post/predicting-entrance-exam-ranks-and-college-admissions-with-machine-learning)
[article](https://indiaai.gov.in/article/ai-can-now-predict-a-student-s-grade-without-an-exam)
[article](https://towardsdatascience.com/learning-to-rank-a-complete-guide-to-ranking-using-machine-learning-4c9688d370d4)
[article](https://www.nowpublishers.com/article/DownloadSummary/INR-016)
[paper](http://arxiv.org/pdf/1811.12808)