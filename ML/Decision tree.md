[[ML Classifiers]] [[Random forest]] [[Gradient boosting]] [[scikitlearn]] [[supervised learning]] [[xg boost]] [[binary classification]] [[multiclass classification]] [[data preprocessing]]

# Decision tree

> Decision tree — asks yes/no feature questions until a leaf assigns a class or average target value.

```txt
        Decision tree ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use decision trees to check impurity splits, overfit knobs (dept…

## Sources
- [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course) — overview
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html) — deep-dive
- [sklearn.tree.DecisionTreeClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html) — deep-dive

## Key Concepts
- **Note:** A decision tree asks a sequence of **yes/no questions** on one feature at a t…

```txt
                    [root: age <= 35?]
                   /                  \
              yes /                    \ no
        [income <= 50k?]          [leaf: high risk]
         /            \
   leaf: low      leaf: medium
```

- **Note:** **Training:** at each node, pick the split that maximizes **information gain*…

- **Note:** **Inference:** O(tree depth) comparisons

- **Note:** **Ensembles:** single trees overfit

## Technical Details
### scikit-learn (classification)

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score

clf = DecisionTreeClassifier(
    max_depth=6,              # cap depth — primary overfit knob
    min_samples_leaf=20,      # leaves need enough support
    min_samples_split=40,
    max_features="sqrt",      # random subspace at each split (RF-like)
    class_weight="balanced",  # skewed labels
    random_state=42,
)
clf.fit(X_train, y_train)
```

### Regression

```python
from sklearn.tree import DecisionTreeRegressor

reg = DecisionTreeRegressor(max_depth=8, min_samples_leaf=10)
```

### Interpretability

```python
from sklearn.tree import export_text, plot_tree

print(export_text(clf, feature_names=list(X.columns)))
# plot_tree(clf, feature_names=..., class_names=..., filled=True)
```

### Hyperparameter search (start here)

| Knob | Effect |
|------|--------|
| `max_depth` | ↑ capacity, ↑ overfit |
| `min_samples_leaf` | ↑ smoothing, ↓ variance |
| `ccp_alpha` | post-prune via cost-complexity |
| `max_leaf_nodes` | hard cap on complexity |

## Mistakes to Avoid
> [!WARNING]
> **Extrapolation:** trees cannot predict outside training range for regression — flat plateau at training min/max.

> [!WARNING]
> **Axis-aligned only:** diagonal boundaries need many splits; [[Model/support vector machines (SVM)]] or linear models may win on linear separable data with fewer params.

> [!WARNING]
> **Leakage via target encoding:** if you encode categoricals using global target stats **before** CV split, metrics lie. Encode inside CV folds.

> [!WARNING]
> **Monotonic constraints ignored** unless you use libraries that support them (XGBoost, LightGBM). Raw sklearn trees can violate business rules (e.g. "higher income → lower risk").

| Symptom | Check | Fix |
|---------|-------|-----|
| 100% train / 50% val | Depth too high, leaf min too low | Reduce `max_depth`; raise `min_samples_leaf`; try `ccp_alpha` |
| Model ignores a feature | High cardinality / sparse one-hot | Target encoding, binning, or tree ensemble |
| Unstable splits run-to-run | Small data + many ties | Set `random_state`; increase `min_samples_split` |
| Biased toward majority class | Check `class_weight`, metric | `class_weight="balanced"`; optimize PR-AUC not accuracy |
| Slow training on wide data | `max_features`, depth | Limit depth; use `max_features`; switch to [[Random forest]] / [[xg boost]] |

## Pros/Cons or Trade-offs
- **High-dimensional sparse text** without feature engineering
- **Need calibrated probabilities** from one tree
- **Strict monotonic or linear relationship**
- **Production latency at massive depth**

## Comparison
- We will … because …

- **Positive:** …

- **Negative / trade-offs:** …

| Alternative | Why rejected |
|-------------|--------------|
| … | … |
