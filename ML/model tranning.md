## Evaluation
- accuracy, precision, recall, F1 score, mean squared error.
### F1 score
- is a metric used to evaluate the performance of a classification model.
- useful in situation where you need to find a balance between precision and recall, especially in case with imbalanced datsets.
## Test size
- `test_size` parameter determines the proportion of the dataset to include in the test split 
- common values `0.2`, `0.25`, `0.1`
- `0.2`: common choice, good balance between training and testing data
- `0.25`: if a large dataset, allowing more data from testing
- `0.1`: very large datasets, where even a small percentage can provide a significant number of samples for testing.
> [!NOTE] for a smaller datasets, a large test size (like 30%) might be necessary to ensure you have enough samples for evaluation.

> [!NOTE] more complex models may require more data to train effectively, suggesting a smaller test size
## Random state
- `random_state` parameter controls the shuffling applied to the data before splitting it into
### Data features and labels
- a data set lacking the variation (features or labels being too similar) can lead to poor model learning.

> [!NOTE] having the same number of features and labels is normal, but the key is whether there is enough variation within the data.

- event with the same feature count, if features are highly correlated or irrelevant, the model may under perform due to poor predictive power.
- feature engineering: Same number of features is fine, but relevant, informative features are necessary for good model performance. You might need feature transformations to make the dataset more meaningful.