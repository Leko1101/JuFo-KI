#import os
#from shutil import copyfile

#SRC_IMAGES_PATH = "./data"
#TARGET_PATH = "./dataset"

#image_dir = os.fsencode(SRC_IMAGES_PATH)
#index = 0
#for image in os.listdir(image_dir):
#    os.rename(image, ("ave-"+ str(index) + ".jpg"))
 #   index += 1
    
import os

SRC_IMAGES_PATH = "./data"
TARGET_PATH = "./dataset"

#create path
if not os.path.exists(TARGET_PATH):
    os.makedirs(TARGET_PATH)


#
for index, image in enumerate(os.listdir(SRC_IMAGES_PATH)):
    src = os.path.join(SRC_IMAGES_PATH, image)
    ext = os.path.splitext(image)[1]
    dst = os.path.join(TARGET_PATH, f"ave-{str(index).zfill(8)}{ext}")
    os.rename(src, dst)