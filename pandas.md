```python
# Convert all numeric columns to integers
df = df.apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)
```
