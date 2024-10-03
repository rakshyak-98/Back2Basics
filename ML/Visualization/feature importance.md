- visualize the contribution of each feature to the model
- [[xg boost]] provides build in function to generate this plot
```python
import xgboost as xbg
import matplotlib.pyplot as plt

xgb.plot_importance(model) # xgboost provide built-in functions to generate this plot
plt.show()
```