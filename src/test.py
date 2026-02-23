from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import torch
import os
import yaml

def load_ground_truth(image_path, img_w, img_h, names):
    """Load ground truth labels for the given image (YOLO format)."""
    # Derive label path from image path: images/ -> labels/, .png/.jpg -> .txt
    label_path = image_path.replace("/images/", "/labels/")
    label_path = os.path.splitext(label_path)[0] + ".txt"

    boxes = []
    if not os.path.exists(label_path):
        print(f"No ground truth label file found: {label_path}")
        return boxes

    with open(label_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 5:
                continue
            cls = int(parts[0])
            cx, cy, w, h = float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])
            # Convert from normalized center format to pixel corner format
            x1 = int((cx - w / 2) * img_w)
            y1 = int((cy - h / 2) * img_h)
            x2 = int((cx + w / 2) * img_w)
            y2 = int((cy + h / 2) * img_h)
            boxes.append((x1, y1, x2, y2, cls, names.get(cls, str(cls))))
    return boxes

def run(param_image_path, includeGroundTruth=False):
    # Load the model
    model = YOLO("runs/detect/train12/weights/best.pt")

    # Load the image (keep BGR for YOLO — it handles BGR→RGB internally)
    image_path = param_image_path
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found or unreadable: {image_path}")
    img_h, img_w = image.shape[:2]

    # Run inference on BGR image (YOLO expects BGR input)
    results = model(image, device="cpu")

    # Draw ground truth bounding boxes (green)
    if includeGroundTruth:
        gt_boxes = load_ground_truth(image_path, img_w, img_h, model.names)
        for (x1, y1, x2, y2, cls, name) in gt_boxes:
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, f"GT: {name}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Draw predicted bounding boxes (red)
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get box coordinates
            conf = box.conf[0].item()  # Confidence score
            cls = int(box.cls[0].item())  # Class ID

            # Draw rectangle and label
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(image, f"{model.names[cls]} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Convert BGR→RGB for matplotlib display
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Show image with legend
    plt.imshow(image)
    plt.axis("off")
    handles = [mpatches.Patch(color="red", label="Prediction")]
    if includeGroundTruth:
        handles.insert(0, mpatches.Patch(color="green", label="Ground Truth"))
    plt.legend(handles=handles, loc="upper right")
    plt.show()

if __name__ == "__main__":
    run("../augmented_agricultural_plant_dataset/dataset/images/train/7.png")