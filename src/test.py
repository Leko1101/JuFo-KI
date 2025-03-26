from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

# Load the model
model = YOLO("yolov11n.pt")  # Using a pre-trained YOLOv8 nano model

# Load the image
image_path = "./datasets/images/val/ave-0053-0019.jpg"  # Replace with your image path
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Run inference
results = model(image)

# Draw bounding boxes
for r in results:
    for box in r.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get box coordinates
        conf = box.conf[0].item()  # Confidence score
        cls = int(box.cls[0].item())  # Class ID

        # Draw rectangle and label
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(image, f"{model.names[cls]} {conf:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

# Show image
plt.imshow(image)
plt.axis("off")
plt.show()
