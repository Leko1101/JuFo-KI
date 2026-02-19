import os
from PIL import Image
from plant_species import plant_species_map

BASE_PATH = "./src_imgs"

for root, dirs, files in os.walk(BASE_PATH):
    files = sorted([f for f in files if not f.startswith('.')])  # Skip hidden files
    for idx, filename in enumerate(files):
        ext = ".png"
        new_name = f"{idx}{ext}"
        old_path = os.path.join(root, filename)
        new_path = os.path.join(root, new_name)
        if old_path != new_path:
            os.rename(old_path, new_path)

number_plant_species = 23
ext = ".png"

for i in range(number_plant_species+1):
    species_name = plant_species_map[i]
    for i in range(10):
        img_path = f"./src_imgs/{species_name}/{i}{ext}"
        img = Image.open(img_path)
        if species_name == "ground":
            img = img.resize([600,600]) 
        else:
            img = img.resize([100,100])
        img.save(img_path)
        




