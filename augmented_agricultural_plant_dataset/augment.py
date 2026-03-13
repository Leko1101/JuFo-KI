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

        # Split into RGB and alpha channels
        rgb = foreground.convert("RGB")
        alpha = foreground.getchannel("A")

        # Resize RGB and alpha only
        ratio = rgb.height / rgb.width
        resizing_factor = random.random() * 0.2 + 0.1
        if ratio > 1:
            r = rgb.width / rgb.height
            new_w = max(1, int(600 * r * resizing_factor))
            new_h = max(1, int(600 * resizing_factor))
        else:
            new_w = max(1, int(600 * resizing_factor))
            new_h = max(1, int(600 * ratio * resizing_factor))
        rgb = rgb.resize((new_w, new_h), Image.LANCZOS)
        alpha = alpha.resize((new_w, new_h), Image.LANCZOS)

        # Rotate both channels
        angle = random.random() * 360
        rgb = rgb.rotate(angle, expand=True)
        alpha = alpha.rotate(angle, expand=True)

        # After rotation, resize both to the same size (use rgb as reference)
        final_size = rgb.size
        rgb = rgb.resize(final_size, Image.LANCZOS)
        alpha = alpha.resize(final_size, Image.LANCZOS)

        # Apply only one enhancement randomly instead of all four to RGB
        aug_choice = random.randint(0, 3)
        if aug_choice == 0:
            rgb = ImageEnhance.Brightness(rgb).enhance(random.random() + 0.5)
        elif aug_choice == 1:
            rgb = ImageEnhance.Contrast(rgb).enhance(random.random() + 0.5)
        elif aug_choice == 2:
            rgb = ImageEnhance.Color(rgb).enhance(random.random() * 0.2 + 0.9)
        else:
            rgb = ImageEnhance.Sharpness(rgb).enhance(random.random() * 0.6 + 0.7)

        # Apply filter (one or none) to RGB
        filter_choice = random.randint(0, 2)
        if filter_choice == 0:
            rgb = rgb.filter(ImageFilter.SHARPEN)
        elif filter_choice == 1:
            rgb = rgb.filter(ImageFilter.SMOOTH)

        #smooth alpha
        #alpha = alpha.filter(ImageFilter.GaussianBlur(radius=1.5))


        # Merge RGB and alpha back
        foreground = rgb.convert("RGBA")
        foreground.putalpha(alpha)

        foreground = foreground.filter(ImageFilter.GaussianBlur(radius=foreground.width/300))

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


