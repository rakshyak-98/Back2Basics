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