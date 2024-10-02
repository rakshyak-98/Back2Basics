- simplest type of neural network
- used for binary classification
- finding an appropriate learning rate requires some experimentation. 
	- If the learning rate is too large, the algorithm will overshoot the global loss minimum.
	- If the learning rate is too small, the algorithm will require more epochs until convergence, which can make the learning slow—especially for large datasets.

> [!INFO] perceptron algorithm never converges on datasets that aren’t perfectly linearly separable

A **perceptron** is the simplest type of artificial neural network used for binary classification tasks. It is the fundamental building block for more complex neural networks and operates similarly to a neuron in the brain. Here's a brief overview:
### Key Points:
1. **Structure**:
   - **Input Layer**: The perceptron takes multiple input values (features) as input.
   - **Weights**: Each input is assigned a weight that determines its importance.
   - **Summation and Activation**: The weighted inputs are summed up, and this sum is passed through an activation function (typically a step function or a sigmoid).
   - **Output**: The activation function produces the output, which is typically binary (0 or 1), representing one of two classes.

2. **Mathematical Representation**:
   - The perceptron can be described as:
     \[
     \text{Output} = \text{Activation} \left( \sum_{i=1}^{n} w_i x_i + b \right)
     \]
     - \(x_i\): Input features.
     - \(w_i\): Weights for the inputs.
     - \(b\): Bias term.
     - **Activation function**: Usually a step function that returns 1 if the weighted sum is above a threshold, and 0 otherwise.

3. **Learning Algorithm**:
   - The perceptron uses a learning algorithm to adjust weights based on errors in prediction (using gradient descent).
   - If the perceptron misclassifies an input, it updates the weights to reduce the error.

### Example:
Consider a simple perceptron for binary classification:
- Inputs: `x1 = 0.5`, `x2 = 1.0`
- Weights: `w1 = 0.7`, `w2 = 0.3`
- Bias: `b = -0.2`
- Summation: `(0.7 * 0.5) + (0.3 * 1.0) + (-0.2) = 0.35 + 0.3 - 0.2 = 0.45`
- If the threshold is 0, the output would be 1 (class 1) since 0.45 > 0.

### Advantages:
- **Simple**: Easy to understand and implement.
- **Binary Classification**: Effective for linearly separable data (can separate two classes with a straight line).

### Disadvantages:
- **Linear Limitation**: Can only classify linearly separable data. It struggles with complex data that can't be separated by a straight line (e.g., XOR problem).
- **Single Layer**: The basic perceptron is limited to binary classification and can't handle multi-class problems or complex patterns. This is why multilayer perceptrons (MLPs) and more complex neural networks are often used.

