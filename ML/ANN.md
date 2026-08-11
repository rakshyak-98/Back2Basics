[[Perceptron]] [[sigmoid]] [[scikitlearn]] [[binary classification]] [[regression]]

# ANN (Artificial Neural Network)

> Stacked layers of weighted sums + nonlinear activations — universal function approximator trained by gradient descent — **Goodfellow et al. (Deep Learning)**.

---

## Mental model

A feedforward ANN maps input **x** through layers:

```txt
h₁ = σ(W₁x + b₁)
h₂ = σ(W₂h₁ + b₂)
ŷ  = W₃h₂ + b₃        # regression head, or softmax for classes
```

Each **neuron** = affine transform + activation (**ReLU**, **sigmoid**, **softmax**). Training minimizes loss (MSE, cross-entropy) via **backpropagation** — chain rule through the graph.

| Concept | Meaning |
|---------|---------|
| **Width / depth** | Capacity; deeper ≠ always better on tabular data |
| **Activation** | Nonlinearity enables curved boundaries |
| **Regularization** | Dropout, L2, early stopping fight overfit |
| **Batch norm** | Stabilizes deep training; watch train/eval mode |

For **retrieval at scale** (recommendation, search), ANN also means **Approximate Nearest Neighbor** index (FAISS, HNSW) — different topic; see embedding + vector DB patterns below.

---

## Standard config / commands

### scikit-learn MLP (tabular baseline)

```python
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

clf = Pipeline([
    ("scale", StandardScaler()),  # ANNs need scaled features
    ("mlp", MLPClassifier(
        hidden_layer_sizes=(128, 64),
        activation="relu",
        alpha=1e-4,              # L2
        early_stopping=True,
        validation_fraction=0.1,
        max_iter=500,
        random_state=42,
    )),
])
clf.fit(X_train, y_train)
```

### PyTorch sketch (custom architecture)

```python
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(in_features, 256), nn.ReLU(), nn.Dropout(0.2),
    nn.Linear(256, 128), nn.ReLU(),
    nn.Linear(128, n_classes),
)
# loss = nn.CrossEntropyLoss(); optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
```

**Why StandardScaler:** unscaled features dominate gradients; tree models don't need this — see [[Decision tree]].

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Loss flat / NaN | Learning rate, input scale | Lower LR; StandardScaler; gradient clipping |
| Train acc high, val low | Capacity, no regularization | Dropout, weight decay, early stopping, more data |
| Slow convergence | LR schedule, batch size | AdamW + warmup; tune batch size to GPU |
| Random results | Seeds, data shuffle | Fix `random_state`; set torch/cuda seeds |
| "ANN" search returns garbage | Embedding quality, index params | Retrain embeddings; tune HNSW `ef`, recall@k |

---

## Gotchas

> [!WARNING]
> **Tabular Kaggle data:** [[Gradient boosting]] / [[Random forest]] often beat shallow MLPs with less tuning. Reach for ANNs when you have images, text, sequences, or massive unstructured data.

> [!WARNING]
> **Leakage via normalization:** fit scaler on **train only** inside a Pipeline or CV fold.

---

## When NOT to use

- **Small tabular datasets (<10k rows)** — [[Decision tree]], [[Model/support vector machines (SVM)]], or linear models first.
- **Need exact interpretable coefficients** — use [[Model/Linear regression]] or GAM.
- **Hard latency SLA on CPU** — deep nets vs single [[Decision tree]] inference cost.

---

## Related

[[Perceptron]] · [[sigmoid]] · [[supervised learning]] · [[binary classification]] · [[Gradient boosting]] · [[scikitlearn]]
