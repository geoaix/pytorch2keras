import numpy as np
import torch
import torch.nn as nn
from torch.autograd import Variable
from pytorch2keras.converter import pytorch_to_keras


class LayerTest(nn.Module):
    def __init__(self):
        super(LayerTest, self).__init__()
        self.selu = nn.SELU()

    def forward(self, x):
        x = self.selu(x)
        return x


class FTest(nn.Module):
    def __init__(self):
        super(FTest, self).__init__()

    def forward(self, x):
        from torch.nn import functional as F
        return F.selu(x)


def check_error(output, k_model, input_np, epsilon=1e-5):
    pytorch_output = output.data.numpy()
    keras_output = k_model.predict(input_np)

    error = np.max(pytorch_output - keras_output)
    print('Error:', error)

    assert error < epsilon
    return error


if __name__ == '__main__':
    max_error = 0
    for i in range(10):
        model = LayerTest()
        model.eval()

        input_np = np.random.uniform(0, 1, (1, 3, 224, 224))
        input_var = Variable(torch.FloatTensor(input_np))
        output = model(input_var)

        k_model = pytorch_to_keras(model, input_var, (3, 224, 224,), verbose=True)

        error = check_error(output, k_model, input_np)
        if max_error < error:
            max_error = error

    for i in range(10):
        model = FTest()
        model.eval()

        input_np = np.random.uniform(0, 1, (1, 3, 224, 224))
        input_var = Variable(torch.FloatTensor(input_np))
        output = model(input_var)

        k_model = pytorch_to_keras(model, input_var, (3, 224, 224,), verbose=True)

        error = check_error(output, k_model, input_np)
        if max_error < error:
            max_error = error

    print('Max error: {0}'.format(max_error))
