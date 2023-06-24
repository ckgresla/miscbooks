# Select a Torch Compute device for the platforms typically cared about

import torch

device = ("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")
print(device)

