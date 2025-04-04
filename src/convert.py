import os
from shutil import copyfile
import csv
import random

SRC_IMAGES_PATH = "./data/images/"
SRC_LABELS_PATH = "./data/bboxes/CropAndWeed/"

TARGET_PATH = "./dataset"

image_dir = os.fsencode(SRC_IMAGES_PATH)
for image in os.listdir(image_dir):

    is_val = random.random() > 0.8

    filename = os.fsdecode(image).replace(".jpg", "")
    with open (os.path.join(SRC_LABELS_PATH, filename + ".csv"), newline = "") as f:
        reader = csv.reader(f)
        data = list(reader)
    
    label_content = ""
    for box in data:
        left = float(box[0])
        top = float(box[1])
        right = float(box[2])
        bottom = float(box[3])
        label_id = int(float(box[4]))
        if label_id == 255:
            label_id = 100

        width = (right - left) / 1920
        height = (bottom - top) / 1088
        center_x = width + left / 1920
        center_y = height + top / 1088

        label_content += f"{label_id} {center_x} {center_y} {width} {height}\n"

    copyfile(os.path.join(SRC_IMAGES_PATH, filename + ".jpg"), os.path.join(TARGET_PATH + "/images/" + ("val" if is_val else "train"), filename + ".jpg"))
    
    f = open(os.path.join(TARGET_PATH + "/labels/" + ("val" if is_val else "train"), filename + ".txt"), "x")
    f.write(label_content)
    f.close()