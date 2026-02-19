from PIL import Image, ImageEnhance, ImageFilter, ImageOps
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

    plants_in_img = []

    background = Image.open(f"./src_imgs/ground/{ground_img}{ext}").convert("RGBA")
    
    for i in range(number_plants_in_img+1):

        placement_failed = False
        plant_species = random.randint(1,23)
        species_name = plant_species_map[plant_species]
        plant_specimen = random.randint(0,9)
        
        foreground = Image.open(f"./src_imgs/{species_name}/{plant_specimen}{ext}").convert("RGBA")

        resizing_factor = random.random()* 0.2 + 0.1
        foreground = foreground.resize([int(foreground.width*resizing_factor), int(foreground.height*resizing_factor)])

        foreground_x = (random.randint(0, 600 - foreground.width)) 
        foreground_y = (random.randint(0, 600 - foreground.height)) 

        foreground_x2 = foreground_x + foreground.width
        foreground_y2 = foreground_y + foreground.height

        foreground.rotate(random.random() * 360, expand = True)

        ImageEnhance.Brightness(foreground).enhance(random.random()* 1 + 0.5)
        ImageEnhance.Contrast(foreground).enhance(random.random()* 1 + 0.5)
        ImageEnhance.Color(foreground).enhance(random.random()* 0.001 + 0.0095)
        ImageEnhance.Sharpness(foreground).enhance(random.random()* 0.6 + 0.7)

        sharpen_or_blur = random.randint(0,1)
        if sharpen_or_blur == 0:
            foreground = foreground.filter(ImageFilter.SHARPEN)
        #else:
        #    foreground = foreground.filter(ImageFilter.GaussianBlur(random.random() * 0.6 + 0.7))

        bool_smooth = random.randint(0,1)
        if bool_smooth == 1:
            foreground = foreground.filter(ImageFilter.SMOOTH)

        #if random.random() < 0.3:  # Apply to 30% of images
        #    width, height = foreground.size
        #    coeffs = [
        #        1 + random.uniform(-0.15, 0.15),  # x scale
        #        random.uniform(-0.08, 0.08),    # x shear
        #        random.uniform(-width*0.08, width*0.08),  # x translation
        #        random.uniform(-0.08, 0.08),    # y shear
        #        1 + random.uniform(-0.15, 0.15),  # y scale
        #        random.uniform(-height*0.08, height*0.08),  # y translation
        #        random.uniform(-0.0002, 0.0002),  # perspective x
        #        random.uniform(-0.0002, 0.0002)   # perspective y
        #    ]
        #    foreground = foreground.transform(foreground.size, Image.PERSPECTIVE, coeffs, Image.BICUBIC)
        #
        # Solarize - simulates overexposure from harsh sunlight (10% probability)
        #if random.random() < 0.1:
        #    # Convert to RGB for solarize, then back to RGBA
        #    alpha = foreground.split()[3]  # Save alpha channel
        #    foreground_rgb = foreground.convert('RGB')
        #    threshold = random.randint(100, 180)  # Partial solarization
        #    foreground_rgb = ImageOps.solarize(foreground_rgb, threshold)
        #    foreground = foreground_rgb.convert('RGBA')
        #    foreground.putalpha(alpha)  # Restore alpha
        
        # Posterize - reduces color depth, simulates low-quality cameras (5% probability)
        #if random.random() < 0.05:
        #    alpha = foreground.split()[3]  # Save alpha channel
        #    foreground_rgb = foreground.convert('RGB')
        #    bits = random.randint(3, 5)  # 3-5 bits per channel (subtle effect)
        #    foreground_rgb = ImageOps.posterize(foreground_rgb, bits)
        #    foreground = foreground_rgb.convert('RGBA')
        #    foreground.putalpha(alpha)  # Restore alpha

        for plant_in_img in plants_in_img:
            (previous_x, previous_y, previous_x2, previous_y2) = plant_in_img
            i = 0
            while foreground_x < previous_x2 and foreground_x > previous_x or foreground_x > previous_x and foreground_x < previous_x2 or foreground_y < previous_y2 and foreground_y > previous_y or foreground_y2 < previous_y2 and foreground_y2 > previous_y:
                i += 1
                if i > 3:
                    placement_failed = True
                    print("failed to place image")
                    plants_in_img.append((foreground_x, foreground_y, foreground_x2, foreground_y2))
                    break

                foreground_x = (random.randint(0, 600 - foreground.width)) 
                foreground_y = (random.randint(0, 600 - foreground.height)) 

                foreground_x2 = foreground_x + foreground.width
                foreground_y2 = foreground_y + foreground.height

            plants_in_img.append((foreground_x, foreground_y, foreground_x2, foreground_y2))

        if placement_failed == True:
            break 

        background.paste(foreground, (foreground_x,foreground_y), foreground)
        background.save("test.png")
        
        
if __name__ == "__main__":
    for i in range(number_augmented_imgs):
        create_augmented_img()


