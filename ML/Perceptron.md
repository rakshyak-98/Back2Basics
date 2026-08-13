[[ML]] [[ANN]] [[sigmoid]]

# Perceptron

> A perceptron is a tiny linear classifier — weighted sum + threshold; the building block of neural nets.

---

## How it works

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

---


## Configuration and commands

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

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Never converges | Not linearly separable | Add features / hidden layer |
| Oscillates | lr too high | Lower lr; normalize X |
| Always one class | class imbalance / bad init | Check labels; class weights |
| Good train, bad test | tiny data | More data / simpler model |

---


## Gotchas

> [!WARNING]
> **Single perceptron ≠ deep learning** — no hidden layer → only linear boundaries.

> [!WARNING]
> **Unscaled inputs** — large features steal the decision.

---


## When not to use

- **XOR-like problems** — need MLP.
- **Raw images/text** — use modern architectures.


## Related

[[ANN]] [[sigmoid]] [[supervised learning]]

## Sources

- [Wikipedia — Perceptron](https://en.wikipedia.org/wiki/Perceptron)
