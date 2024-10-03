- compares the predicated ranks / scores against actual values to assess model performance visually.

```python
import matplotlib.pyplot as plt
plt.scatter(y_test, predictions, alpha=0.5)
plt.title('Actual vs Predicated')
plt.xlabel('Actual Ranks/Scores')
plt.ylabel('Predicated Ranks/Scores')
plt.show()
```
