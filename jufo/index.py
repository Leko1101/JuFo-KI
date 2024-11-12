import torch 
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout(0.25)
        self.linear1 = nn.Linear(9216, 128)
        self.dropout2 = nn.Dropout(0.5)
        self.linear2 = nn.Linear(128, 10)
    
    def forward(self, x):
        y = self.conv1(x)
        y = F.relu(y)
        y = self.conv2(y)
        y = F.relu(y)
        y = F.max_pool2d(y, 2)
        y = self.dropout1(y)
        y = torch.flatten(y, 1)
        y = self.linear1(y)
        y = F.relu(y)
        y = self.dropout2(y)
        y = self.linear2(y)
        y = F.log_softmax(y, dim = 1)
        return y