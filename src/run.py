from test import run
import os
import time

def get_image_path():
   return os.path.join("./", "20250509_171308.jpg")

if __name__ == "__main__":
    interval = 0.1
    while True:
        run(get_image_path())
        time.sleep(interval)



