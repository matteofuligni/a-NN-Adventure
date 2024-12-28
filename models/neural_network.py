 
import numpy as np

class NeuralNetwork:
    def __init__(self, input_size, hidden_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = 3
        
        self.weights = [
            np.random.randn(self.input_size, self.hidden_size),
            np.random.randn(self.hidden_size, self.output_size)
        ]
        self.biases = [
            np.random.randn(self.hidden_size),
            np.random.randn(self.output_size)
        ]
        self.learning_rate = 0.1
        self.momentum = 0.9
        self.loss = 0.0
        self.accuracy = 0.0
        self.error = 0.0
        self.epoch = 0
        self.batch_size = 0
        self.optimizer = None
        self.loss_function = None
        self.activation_function = self.sigmoid

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def make_decision(self, vision):
        self.vision = vision
        input_to_hidden = self.activation_function(
            np.dot(self.vision, self.weights[0]) + self.biases[0]
        )
        hidden_to_output = self.activation_function(
            np.dot(input_to_hidden, self.weights[1]) + self.biases[1]
        )
        return np.argmax(hidden_to_output)
    
    def train(self, X, y, epochs):
        for epoch in range(epochs):
            for i in range(len(X)):
                # Forward pass
                input_to_hidden = self.activation_function(
                    np.dot(X[i], self.weights[0]) + self.biases[0]
                )
                hidden_to_output = self.activation_function(
                    np.dot(input_to_hidden, self.weights[1]) + self.biases[1]
                )

                # Calculate loss (Mean Squared Error)
                loss = y[i] - hidden_to_output

                # Backward pass
                d_hidden_to_output = loss * self.sigmoid_derivative(hidden_to_output)
                d_input_to_hidden = np.dot(d_hidden_to_output, self.weights[1].T) * self.sigmoid_derivative(input_to_hidden)

                # Update weights and biases
                self.weights[1] += self.learning_rate * np.dot(input_to_hidden.reshape(-1, 1), d_hidden_to_output.reshape(1, -1))
                self.biases[1] += self.learning_rate * d_hidden_to_output
                self.weights[0] += self.learning_rate * np.dot(X[i].reshape(-1, 1), d_input_to_hidden.reshape(1, -1))
                self.biases[0] += self.learning_rate * d_input_to_hidden

            # Print loss every 100 epochs
            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Loss: {np.mean(np.square(loss))}")
        
        


#vision = np.random.randn(input_size)  # Simulazione di un input di visione
#decision = nn.make_decision(vision)
#print(f"Decision: {decision}")
        