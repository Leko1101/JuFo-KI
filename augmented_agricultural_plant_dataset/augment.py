from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import random
import csv
import os
from multiprocessing import Pool, cpu_count
from plant_species import plant_species_map

number_plant_species = 23
number_augmented_imgs = 1
DESTINATION_PATH = "./dest_imgs"
ext = ".png"

# These will be loaded per-process
ground_images = None
plant_images = None

def load_images():
    """Load all source images into memory."""
    global ground_images, plant_images
    ground_images = []
    for g in range(10):
        ground_images.append(Image.open(f"./src_imgs/ground/{g}{ext}").convert("RGBA"))
    plant_images = {}
    for species_id in range(1, number_plant_species + 1):
        species_name = plant_species_map[species_id]
        plant_images[species_id] = []
        for specimen in range(10):
            plant_images[species_id].append(
                Image.open(f"./src_imgs/{species_name}/{specimen}{ext}").convert("RGBA")
            )

def init_worker(seed_base):
    """Initialize each worker process with images and unique seed."""
    load_images()
    random.seed(seed_base + os.getpid())

def create_augmented_img(number_img):
    ground_img = random.randint(0, 9)
    number_plants_in_img = random.randint(1, 25)

    plants_in_img = []
    plants_data = []

    background = ground_images[ground_img].copy()

    for _ in range(number_plants_in_img + 1):

        placement_failed = False
        plant_species = random.randint(1, 23)
        plant_specimen = random.randint(0, 9)

        foreground = plant_images[plant_species][plant_specimen]

        # Resize to final size in one step (NEAREST is fastest)
        ratio = foreground.height / foreground.width
        resizing_factor = random.random() * 0.2 + 0.1
        if ratio > 1:
            r = foreground.width / foreground.height
            new_w = max(1, int(600 * r * resizing_factor))
            new_h = max(1, int(600 * resizing_factor))
        else:
            new_w = max(1, int(600 * resizing_factor))
            new_h = max(1, int(600 * ratio * resizing_factor))
        foreground = foreground.resize((new_w, new_h), Image.NEAREST)

        # Rotate small image
        foreground = foreground.rotate(random.random() * 360, expand=True)

        # Apply only one enhancement randomly instead of all four
        aug_choice = random.randint(0, 3)
        if aug_choice == 0:
            foreground = ImageEnhance.Brightness(foreground).enhance(random.random() + 0.5)
        elif aug_choice == 1:
            foreground = ImageEnhance.Contrast(foreground).enhance(random.random() + 0.5)
        elif aug_choice == 2:
            foreground = ImageEnhance.Color(foreground).enhance(random.random() * 0.2 + 0.9)
        else:
            foreground = ImageEnhance.Sharpness(foreground).enhance(random.random() * 0.6 + 0.7)

        # Apply filter (one or none)
        filter_choice = random.randint(0, 2)
        if filter_choice == 0:
            foreground = foreground.filter(ImageFilter.SHARPEN)
        elif filter_choice == 1:
            foreground = foreground.filter(ImageFilter.SMOOTH)

        # Ensure foreground fits within 600x600
        if foreground.width >= 600 or foreground.height >= 600:
            continue

        fw = foreground.width
        fh = foreground.height
        max_x = 600 - fw
        max_y = 600 - fh

        foreground_x = random.randint(0, max_x)
        foreground_y = random.randint(0, max_y)
        foreground_x2 = foreground_x + fw
        foreground_y2 = foreground_y + fh

        # Collision detection
        for (prev_x, prev_y, prev_x2, prev_y2) in plants_in_img:
            attempts = 0
            while (foreground_x < prev_x2 and foreground_x2 > prev_x and
                   foreground_y < prev_y2 and foreground_y2 > prev_y):
                attempts += 1
                if attempts > 3:
                    placement_failed = True
                    break
                foreground_x = random.randint(0, max_x)
                foreground_y = random.randint(0, max_y)
                foreground_x2 = foreground_x + fw
                foreground_y2 = foreground_y + fh

            if placement_failed:
                break

        if placement_failed:
            break

        plants_in_img.append((foreground_x, foreground_y, foreground_x2, foreground_y2))
        plants_data.append((plant_species, foreground_x + fw / 2, foreground_y + fh / 2, fw, fh))

        background.paste(foreground, (foreground_x, foreground_y), foreground)

    background.save(f"./dest_imgs/{number_img}{ext}")
    return plants_data


if __name__ == "__main__":
    os.makedirs(DESTINATION_PATH, exist_ok=True)
    output_file = "plants_annotations.csv"

    num_workers = max(1, cpu_count() - 1)
    print(f"Using {num_workers} workers")

    with Pool(processes=num_workers, initializer=init_worker, initargs=(2,)) as pool:
        # todo images should have a unique id. ID must also be present in csv
        results = pool.map(create_augmented_img, range(number_augmented_imgs))

    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['species_id', 'center_x', 'center_y', 'width', 'height'])
        for plants_data in results:
            writer.writerows(plants_data)

    print(f"Generated {number_augmented_imgs} images")
    print(f"Data saved to: {output_file}")


