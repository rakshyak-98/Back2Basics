# Histogram
- displays the frequency distribution of a dataset
- best for showing how data is spread across intervals (bins)
```python
import matplotlib.pyplot as plt
plt.hist(data, bins=20, alpha=0.7)
plt.title('Data distribution (Histogram)')
plt.xlabel('Data values')
plt.ylabel('Frequency')
plt.show()
```

## Density Plot (KDE- Kernel Density Estimate)
- A smoothed curve representing the distribution of data, which is similar to a smoothed histogram.
- better for showing data distribution in a more continuous and smooth way, ideal for visualizing probability distributions.

```python
import seaborn as sns
sns.kdeplot(data)
plt.title('Data distribution (Density Plot)')
plt.xlabel('Data values')
plt.show()
```

## Box plot
- summarizes data distribution with minimum, first quartile, median, third quartile, and maximum.
- useful for identifying outliers and comparing distributions across categories.

```python
import seaborn as sns
sns.boxplot(data=data)
plt.title('Data distribution (box plot)')
plt.show()
```

## Violin plot
- combines a box plot with a KDE plot, showing shape and data summary.
- offers a deeper understanding of the distribution, combining box plot features with KDE.

```python
import seaborn as sns
sns.violinplot(data=data)
plt.show();
```
