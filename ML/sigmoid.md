[[binary classification]] [[multiclass classification]] [[Model/Linear regression]] [[ANN]] [[Perceptron]]

# Sigmoid

> Sigmoid — the sigmoid is a smooth S-curve saturating at 0 and 1. In logistic regression:

```txt
        Sigmoid ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Interviewers ask about Sigmoid to check whether you can choose models/metrics…

## Sources
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html) — deep-dive
- [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course) — overview
- [sigmoid — Wikipedia](https://en.wikipedia.org/wiki/Sigmoid_function) — overview

## Key Concepts
- **Note:** The sigmoid is a smooth **S-curve** saturating at 0 and 1

```txt
z = w·x + b
p = σ(z) = P(y=1 | x)
```

- **Note:** Large positive **z** → p ≈ 1

| Role | Where |
|------|-------|
| **Output activation** | Final layer of binary classifier |
| **Gate (LSTM/GRU)** | Controls information flow (historical) |
| **Attention (legacy)** | Softmax replaced in many transformers |

- **Note:** **Multiclass** uses **softmax** (vector sigmoid generalization), not scalar s…

- **Note:** Derivatives: σ'(z) = σ(z)(1 − σ(z))

## Technical Details
```python
import numpy as np
from sklearn.linear_model import LogisticRegression

def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -500, 500)))  # clip avoids overflow

# Prefer library implementation
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)
proba = clf.predict_proba(X_test)[:, 1]  # already sigmoid of margin in binary case
```

### PyTorch

```python
import torch
p = torch.sigmoid(logits)           # binary
p = torch.softmax(logits, dim=-1)   # multiclass
```

### Plot calibration check

```python
from sklearn.calibration import calibration_curve
prob_true, prob_pred = calibration_curve(y_test, proba, n_bins=10)
# plot prob_pred vs prob_true — diagonal = well calibrated
```

## Mistakes to Avoid
> [!WARNING]
> **Sigmoid ≠ guaranteed calibrated probability** — especially on shifted data or after heavy oversampling.

> [!WARNING]
> **Class imbalance + sigmoid loss** — model may under-predict minority; tune threshold and use `class_weight`.

| Symptom | Check | Fix |
|---------|-------|-----|
| `overflow` in exp | Raw logits magnitude | Clip z; normalize features |
| Probabilities all ~0 or ~1 | Separable data, no regularization | Increase C⁻¹ in LogisticRegression; L2 |
| Sigmoid in hidden layers, dead grads | Saturation | Switch hidden activations to ReLU/GELU |
| miscalibrated probs | Reliability diagram | Platt scaling / isotonic |
| Multiclass with sigmoid per class | Wrong head | Softmax + cross-entropy |

## Pros/Cons or Trade-offs
- **Hidden layers in deep CNNs/Transformers** — ReLU, GELU, SiLU dominate.
- **Multiclass mutually exclusive labels** — softmax + cross-entropy.
- **Regression on continuous y** — linear head, no sigmoid.
