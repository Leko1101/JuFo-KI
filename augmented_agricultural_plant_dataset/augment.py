from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import random
import os
from multiprocessing import Pool, cpu_count
from plant_species import plant_species_map

IMG_SIZE = 600
number_plant_species = 30
number_augmented_imgs = 30
val_split = 0.2
DATASET_PATH = "./dataset"
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
        plant_species = random.randint(1, number_plant_species)
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
        foreground = foreground.resize((new_w, new_h), Image.LANCZOS)

        # Rotate small image

        foreground = foreground.rotate(random.random() * 360, expand=True, fillcolor=(0, 0, 0, 0))

        #Split RGBA and merge to RGB before enhancements
        r_img, g_img, b_img, a_img = foreground.split()
        rgb_img = Image.merge('RGB', (r_img, g_img, b_img))

        # Apply enhancements only to RGB
    
        foreground = ImageEnhance.Brightness(foreground).enhance(random.random() + 0.5)
        foreground = ImageEnhance.Contrast(foreground).enhance(random.random() + 0.5)
        foreground = ImageEnhance.Color(foreground).enhance(random.random() * 0.2 + 0.9)
        #foreground = ImageEnhance.Sharpness(foreground).enhance(random.random() * 0.2 + 0.9)

        # Apply filter
        #if filter_choice == 0:
        #   foreground = foreground.filter(ImageFilter.SHARPEN)
        #elif filter_choice == 1:
        #Check usefulness
        #if(random.random() > 0.8) {
        #    foreground = foreground.filter(ImageFilter.SMOOTH)
        #}

        #if(random.random() > 0.8) {
        #    foreground = foreground.filter(ImageFilter.CONTOUR)
        #}

        #if(random.random() > 0.8) {
        #    foreground = foreground.filter(ImageFilter.BLUR)
        #}

        #if(random.random() > 0.8) {
        #    foreground = foreground.filter(ImageFilter.DETAIL)
        #}

        #Blur Alpha Channel
        a_img = a_img.filter(ImageFilter.GaussianBlur(radius=1.5))
        #a_img = a_img.point(lambda x: 255 if x > 200 else 0)
        

        foreground = Image.merge('RGBA', (*rgb_img.split(), a_img))
        

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
            while (foreground_x < prev_x2 and foreground_x2 > prev_x and foreground_y < prev_y2 and foreground_y2 > prev_y):
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
        # Normalize to 0-1 for YOLO format
        plants_data.append((
            plant_species,
            (foreground_x + fw / 2) / IMG_SIZE,
            (foreground_y + fh / 2) / IMG_SIZE,
            fw / IMG_SIZE,
            fh / IMG_SIZE
        ))

        background.paste(foreground, (foreground_x, foreground_y), foreground)

    # Decide train or val
    split = "val" if random.random() < val_split else "train"

    background.save(os.path.join(DATASET_PATH, "images", split, f"{number_img}{ext}"))

    # Write YOLO .txt label (space-separated, no header)
    label_path = os.path.join(DATASET_PATH, "labels", split, f"{number_img}.txt")
    with open(label_path, 'w') as f:
        for species_id, cx, cy, w, h in plants_data:
            f.write(f"{species_id} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}\n")

    return plants_data


if __name__ == "__main__":
    for split in ["train", "val"]:
        os.makedirs(os.path.join(DATASET_PATH, "images", split), exist_ok=True)
        os.makedirs(os.path.join(DATASET_PATH, "labels", split), exist_ok=True)

    num_workers = max(1, cpu_count() - 1)
    print(f"Using {num_workers} workers")

    with Pool(processes=num_workers, initializer=init_worker, initargs=(2,)) as pool:
        pool.map(create_augmented_img, range(number_augmented_imgs))

    print(f"Generated {number_augmented_imgs} images")
    print(f"Dataset saved to: {DATASET_PATH}/")


