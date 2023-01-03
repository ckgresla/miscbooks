# Apply Convolutions to Images with Numpy -- would like to get this to create "gaussian blur" nicely (currently just creates kinda noise)
import numpy as np
from PIL import Image


# Apply a Basic Convolution
out = np.convolve([1, 2, 3], [4, 5, 6])
print(out)


# Read in Image From Disk + Print Info
img = Image.open('wiz.png')

print(img.format)
print(img.size)
print(img.mode)


# Convert PIL Image to ndarray
img = np.asarray(img)
print(f"image array shape: {img.shape}")

# Flatten Image Tensor to Vector
img = img.flatten() #as per- https://numpy.org/doc/stable/reference/generated/numpy.ndarray.flatten.html
print(f"flattened image vector: {img.shape}")


# Create Kernel for Convolution
kernel = np.random.normal(0, 1, 50) #values @ Mean zero w Unit Variance 
#kernel = np.full(shape=9, fill_value=1/9) #set kernel (like in the 3blue1brown video)


# Convolve Image's Vector w Kernel
out = np.convolve(img, kernel)
print(f"convolved image shape: {out.shape}")


# Write out Convolved Image 
out = out[25:-24] #chop off extra pixels (for normal distribution)
# out = out[1:-1] #chop off extra pixels (for full/constant kernel)
out = np.reshape(out, (512, 512, 4))
data = Image.fromarray(out, 'RGBA')
data.save("out.png")



