import numpy as np
np.random.seed(0)

# dataset
# Copyright (c) 2015 Andrej Karpathy
# License: https://github.com/cs231n/cs231n.github.io/blob/master/LICENSE
# Source: https://cs231n.github.io/neural-networks-case-study/

def spiral_data(samples, classes):
    X = np.zeros((samples*classes, 2))
    y = np.zeros(samples*classes, dtype='uint8')
    for class_number in range(classes):
        ix = range(samples*class_number, samples*(class_number+1))
        r = np.linspace(0.0, 1, samples)
        t = np.linspace(class_number*4, (class_number+1)*4, samples) + np.random.randn(samples)*0.2
        X[ix] = np.c_[r*np.sin(t*2.5), r*np.cos(t*2.5)]
        y[ix] = class_number
    return X, y 

# layer
class layer_dense:
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.10 * np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))
    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases

# ReLU 
class activation_relu:
    def forward(self, inputs):
        self.outputs = np.maximum(0, inputs)
# Softmax
class activation_solftmax:
    def forward(self, inputs):
        exp_value = np.exp(inputs - np.max(inputs, axis=1, keepdims=True)) # input - max(input) -> for avoiding overflow
        norm_value = np.sum(exp_value, axis=1, keepdims=True)
        self.outuput = exp_value / norm_value

class loss:
    def calculate(self, output, y):
        sample_losses = self.forward(output, y)
        data_losses = np.mean(sample_losses)
        return data_losses
    
class loss_CategoricalCrossEntropy(loss):
    def forward(self, y_pred, y_true):
        samples = len(y_pred)
        y_pred_clipped = np.clip(y_pred, 1e-7, 1-1e-7) # clippping value near to infinity avoid log(0) for y->prediction

        if len(y_true.shape) == 1:
            correct_confidences = y_pred_clipped[range(samples), y_true]
        elif len(y_true.shape()) == 2:
            correct_confidences = np.sum(y_pred_clipped*y_true, axis = 1)
        
        negative_log_likelihood = -np.log(correct_confidences)
        return negative_log_likelihood


X, y = spiral_data(samples=100, classes=3)

dense1 =layer_dense(2,3)
activation1 = activation_relu()

dense2 = layer_dense(3, 3)
activation2 = activation_solftmax()

dense1.forward(X)
activation1.forward(dense1.output)

dense2.forward(activation1.outputs)
activation2.forward(dense2.output)

print(activation2.outuput[:5])

loss_function = loss_CategoricalCrossEntropy()
loss = loss_function.calculate(activation2.outuput, y)

print(loss)