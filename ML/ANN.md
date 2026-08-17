[[Perceptron]] [[sigmoid]] [[scikitlearn]] [[binary classification]] [[regression]] [[supervised learning]] [[Gradient boosting]]

# ANN (Artificial Neural Network)

> Stacked layers of weighted sums + nonlinear activations — universal function approximator trained by gradient descent — **Goodfellow et al. (Deep Learning)**.

```txt
        ANN (Artificial Ne ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Interviewers ask about ANN (Artificial Neural Network) to check whether you c…

## Sources
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html) — deep-dive
- [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course) — overview

## Key Concepts
A feedforward ANN maps input **x** through layers:

```txt
h₁ = σ(W₁x + b₁)
h₂ = σ(W₂h₁ + b₂)
- **Note:** ŷ = W₃h₂ + b₃ # regression head, or softmax for classes
```

- **Note:** Each **neuron** = affine transform + activation (**ReLU**, **sigmoid**, **sof…

| Concept | Meaning |
|---------|---------|
| **Width / depth** | Capacity; deeper ≠ always better on tabular data |
| **Activation** | Nonlinearity enables curved boundaries |
| **Regularization** | Dropout, L2, early stopping fight overfit |
| **Batch norm** | Stabilizes deep training; watch train/eval mode |

- **Note:** For **retrieval at scale** (recommendation, search), ANN also means **Approxi…

## Technical Details
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

- **Why StandardScaler:** unscaled features dominate gradients; tree models don…

## Mistakes to Avoid
> [!WARNING]
> **Tabular Kaggle data:** [[Gradient boosting]] / [[Random forest]] often beat shallow MLPs with less tuning. Reach for ANNs when you have images, text, sequences, or massive unstructured data.

> [!WARNING]
> **Leakage via normalization:** fit scaler on **train only** inside a Pipeline or CV fold.

| Symptom | Check | Fix |
|---------|-------|-----|
| Loss flat / NaN | Learning rate, input scale | Lower LR; StandardScaler; gradient clipping |
| Train acc high, val low | Capacity, no regularization | Dropout, weight decay, early stopping, more data |
| Slow convergence | LR schedule, batch size | AdamW + warmup; tune batch size to GPU |
| Random results | Seeds, data shuffle | Fix `random_state`; set torch/cuda seeds |
| "ANN" search returns garbage | Embedding quality, index params | Retrain embeddings; tune HNSW `ef`, recall@k |

## Pros/Cons or Trade-offs
- **Small tabular datasets (<10k rows)**
- **Need exact interpretable coefficients**
- **Hard latency SLA on CPU**
