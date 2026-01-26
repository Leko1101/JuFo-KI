import os

BASE_PATH = "./src_imgs"

for root, dirs, files in os.walk(BASE_PATH):
    files = sorted([f for f in files if not f.startswith('.')])  # Skip hidden files
    for idx, filename in enumerate(files):
        ext = ".jpg"
        new_name = f"{idx}{ext}"
        old_path = os.path.join(root, filename)
        new_path = os.path.join(root, new_name)
        if old_path != new_path:
            os.rename(old_path, new_path)