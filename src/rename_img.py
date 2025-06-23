import os

SRC_IMAGES_PATH = "./data"
TARGET_PATH = "./dataset"

#create path
if not os.path.exists(TARGET_PATH):
    os.makedirs(TARGET_PATH)

for index, image in enumerate(os.listdir(SRC_IMAGES_PATH)):
    index = str(index).zfill(8)
    index_first_slice = index[:4]
    index_second_slice = index[4:]
    index = index_first_slice + "-" + index_second_slice
    new_img_name =" jfk-" + index + ".jpg"
    source_image = os.path.join(SRC_IMAGES_PATH, image)
    destination_image = os.path.join(TARGET_PATH, new_img_name)
    os.rename(source_image, destination_image)