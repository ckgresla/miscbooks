# Need a Torch install w CUDA
import torch


device = torch.cuda.is_available()
print(device)
print(torch.cuda.get_device_name())
print(torch.cuda.memory_reserved())

if device != False:
    print("Congratulations, you are not poor GPU Owner!")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


