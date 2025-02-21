import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

image = np.asarray(Image.open("drache.png").convert("L")) / 255.0

print(image)
plt.imshow(image)
plt.show()