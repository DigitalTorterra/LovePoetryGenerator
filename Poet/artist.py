#A stripped down version that just generates poetry
#based on saved weights
# Importing libraries
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F

#custom modules
from helper_functions import *
from CharRNN import CharRNN
from training_function import train

#import text
with open('poetry.txt','r',encoding='cp1252')  as f:
    text = f.read()

# encoding the text and map each character to an integer and vice versa
# 1. int2char, which maps integers to characters
# 2. char2int, which maps characters to integers
chars = tuple(set(text))
int2char = dict(enumerate(chars))
char2int = {ch:ii for ii,ch in int2char.items()}
encoded = np.array([char2int[i] for i in text])

# Check if GPU is available
train_on_gpu = torch.cuda.is_available()


n_hidden=512
n_layers=2

net = CharRNN(chars, n_hidden, n_layers)
net.load_state_dict(torch.load('weights.ckpt'))
print(net)

# Declaring the hyperparameters
batch_size = 128
seq_length = 100

# Defining a method to generate the next character
def predict(net, char, h=None, top_k=None):
    ''' Given a character, predict the next character.
        Returns the predicted character and the hidden state.
    '''

    # tensor inputs
    x = np.array([[net.char2int[char]]])
    x = one_hot_encode(x, len(net.chars))
    inputs = torch.from_numpy(x)

    if(train_on_gpu):
        inputs = inputs.cuda()

    # detach hidden state from history
    h = tuple([each.data for each in h])
    # get the output of the model
    out, h = net(inputs, h)

    # get the character probabilities
    p = F.softmax(out, dim=1).data
    if(train_on_gpu):
        p = p.cpu() # move to cpu

    # get top characters
    if top_k is None:
        top_ch = np.arange(len(net.chars))
    else:
        p, top_ch = p.topk(top_k)
        top_ch = top_ch.numpy().squeeze()

    # select the likely next character with some element of randomness
    p = p.numpy().squeeze()
    char = np.random.choice(top_ch, p=p/p.sum())

    # return the encoded value of the predicted char and the hidden state
    return net.int2char[char], h

def sample(net, size, prime='The', top_k=None):

    if(train_on_gpu):
        net.cuda()
    else:
        net.cpu()

    net.eval() # eval mode

    # First off, run through the prime characters
    chars = [ch for ch in prime]
    h = net.init_hidden(1)
    for ch in prime:
        char, h = predict(net, ch, h, top_k=top_k)

    chars.append(char)

    # Now pass in the previous character and get a new one
    for ii in range(size):
        char, h = predict(net, chars[-1], h, top_k=top_k)
        chars.append(char)

    return ''.join(chars)

# Generating new text
print(sample(net, 1000, prime='The', top_k=5))

with open('New_Poetry.txt','w') as f:
    poetry = sample(net, 10000, prime='The', top_k=5)
