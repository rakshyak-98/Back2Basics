- visualizes the difference between predicated and actual values, helping to assess model accuracy.

```python
residuals = y_test - predictions
plt.scatter(predictions, residuals, alpha=0.5)
plt.title('Residual Plot')
plt.xlabel('Predicted values')
plt.ylabel('Residuals')
plt.axhline(y=0, color='r', linestyle='--')
plt.show()
```