#!/usr/bin/env python
# Repurposed for PyTorch from- https://www.geeksforgeeks.org/introduction-convolution-neural-network/

# import the necessary libraries
import numpy as np
import torch
import torchvision.transforms as transforms
import matplotlib.pyplot as plt

# set the param
plt.rc('figure', autolayout=True)
plt.rc('image', cmap='magma')

# define the kernel
kernel = torch.tensor([[-1, -1, -1],
                       [-1,  8, -1],
                       [-1, -1, -1]])

# load the image
image = plt.imread('Ganesh.jpg')
image = plt.imread('/Users/ckg/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Ikigai Quadrants.png')
image = transforms.ToTensor()(image)
image = image[0:3] 
image = transforms.Resize((300, 300))(image)

# plot the image
image, _, b = image.unbind(0)
# r, image, b = image.unbind(0)
# img = image.permute(1, 2, 0).squeeze().numpy() #1st method to convert the odd shaped img to plt-able version 
img = image.squeeze().numpy()

plt.figure(figsize=(5, 5))
# print(img[0])
plt.imshow(img, cmap='gray', vmin=0, vmax=255)
plt.gray()
plt.axis('off')
plt.title('Original Gray Scale image')
plt.show()

# Reformat
image = image.float().unsqueeze(0)
kernel = kernel.unsqueeze(0).unsqueeze(0).float()

# convolution layer
conv_fn = torch.nn.functional.conv2d

image_filter = conv_fn(
    input=image,
    weight=kernel,
    stride=1,
    padding=1,
)

plt.figure(figsize=(15, 5))

# Plot the convolved image
plt.subplot(1, 3, 1)
plt.imshow(
    image_filter.squeeze().detach().numpy()
)
plt.axis('off')
plt.title('Convolution')

# activation layer
relu_fn = torch.nn.functional.relu
# relu_fn = torch.nn.functional.gelu

# Image detection
image_detect = relu_fn(image_filter)

plt.subplot(1, 3, 2)
plt.imshow(
    image_detect.squeeze().detach().numpy()
)
plt.axis('off')
plt.title('Activation')

# Pooling layer
pool = torch.nn.functional.max_pool2d
image_condense = pool(input=image_detect,
                      kernel_size=(2, 2),
                      stride=(2, 2),
                      padding=0,
                      ceil_mode=False,
                    )

plt.subplot(1, 3, 3)
plt.imshow(image_condense.squeeze().detach().numpy())
plt.axis('off')
plt.title('Pooling')
plt.show()

