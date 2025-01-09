 
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

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
        
        

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size): #building the input, hidden and output layer
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x): #this is a feed-forward neural net
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, file_name='model.pth'): #saving the model
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)

        
class QTrainer:
    def __init__(self, model, lr, gamma): #initializing 
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr) #optimizer
        self.criterion = nn.MSELoss() #loss function

    def train_step(self, state, action, reward, next_state, done): #trainer
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        if len(state.shape) == 1: #if there 1 dimension
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done,)
        pred = self.model(state) #using the Q=model predict equation above

        target = pred.clone() #using Qnew = r+y(next predicted Q) as mentionned above
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))
            target[idx][torch.argmax(action[idx]).item()] = Q_new

        self.optimizer.zero_grad() #calculating loss function
        loss = self.criterion(target, pred)
        loss.backward()
        self.optimizer.step()