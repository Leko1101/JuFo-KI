from PIL import Image
import random
from plant_species import plant_species_map
#import matplotlib.pyplot as plt
#import matplotlib.image as mpimg

random.seed(10)

number_plant_species = 23
number_augmented_imgs = 100
DESTINATION_PATH = "./dest_imgs"

def create_augmented_img():
    ext = ".png"
    ground_img = random.randint(0,9)
    number_plants_in_img = random.randint(1,25)
    
    for i in range(number_plants_in_img):

        plant_species = random.randint(1,23)
        species_name = plant_species_map[plant_species]
        plant_specimen = random.randint(0,9)
        
        background = Image.open(f"./src_imgs/ground/{ground_img}{ext}").convert("RGBA")
        foreground = Image.open(f"./src_imgs/{species_name}/{plant_specimen}{ext}").convert("RGBA")

    

        background.paste(foreground, (0,0), foreground)
        background.save("test.png")
        
        


if __name__ == "__main__":
    for i in range(number_augmented_imgs):
        create_augmented_img()


