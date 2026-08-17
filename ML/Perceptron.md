[[ML]] [[ANN]] [[sigmoid]] [[supervised learning]]

# Perceptron

> A perceptron is a tiny linear classifier — weighted sum + threshold; the building block of neural nets.





## Interview Relevance
Interviewers ask about Perceptron to check whether you can choose models/metrics for the problem, explain bias-variance trade-offs, and avoid evaluation mistakes.

## Sources
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html) — deep-dive
- [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course) — overview
- [Perceptron — Wikipedia](https://en.wikipedia.org/wiki/Perceptron) — overview

## Key Concepts
```txt
x · w + b  →  activation  →  ŷ
     ↑ update w when wrong (perceptron rule / gradient)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Weights / bias** | Learnable params | “Draw the decision boundary.” |
| **Linearly separable** | Line/plane splits classes | “XOR needs more layers.” |
| **Activation** | Step / sigmoid / ReLU | “Non-linearity enables depth.” |
| **Epoch** | One pass over data | “Shuffle each epoch.” |

## Technical Details
```python
import numpy as np
def predict(x, w, b):
    return 1 if np.dot(x, w) + b > 0 else 0

# perceptron update
w += lr * (y - ŷ) * x
b += lr * (y - ŷ)
```

| Knob | Why it matters |
|------|----------------|
| Learning rate | Too high oscillates |
| Feature scale | Dominating dimensions |
| Bias | Boundary not forced through origin |

## Pros/Cons or Trade-offs
- **XOR-like problems** — need MLP.
- **Raw images/text** — use modern architectures.

## Mistakes to Avoid
> [!WARNING]
> **Single perceptron ≠ deep learning** — no hidden layer → only linear boundaries.

> [!WARNING]
> **Unscaled inputs** — large features steal the decision.

| Symptom | Check | Fix |
|---------|-------|-----|
| Never converges | Not linearly separable | Add features / hidden layer |
| Oscillates | lr too high | Lower lr; normalize X |
| Always one class | class imbalance / bad init | Check labels; class weights |
| Good train, bad test | tiny data | More data / simpler model |
