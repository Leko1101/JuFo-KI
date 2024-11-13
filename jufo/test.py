import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

image = Image.open("drache.png")
image = image[::7.5, ::7.5]
image = np.asarray(image).convert("L") /255

image.show
print(image)
plt.imshow(image)
plt.show()