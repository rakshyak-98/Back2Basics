- shows how the predicated ranks are distributed across the data.

```python
import seaborn as sns
sns.histplot(predictions, kde=True)
plt.title('Predicted Rank Distribution')
plt.xlabel('Predicted Rank')
plt.ylabel('Frequency')
plt.show()
```