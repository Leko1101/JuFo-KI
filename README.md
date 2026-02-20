Dokumentation

Plant Identification AI

The goal of this project is to develop an AI-supported solution for real-time detection of crops and weeds in an agricultural environment. For example, farmers could be enabled to selectively and species-specifically remove unwanted plants. This allows, among other things, the targeted preservation of cover or undersown crops, thus utilizing their agronomic benefits while simultaneously effectively eliminating harmful weeds.


Originally, the plan was to build the AI on a custom-developed Convolutional Neural Network (CNN). A corresponding basic structure was already designed for this purpose. However, during the process, we decided to use a YOLO model (You Only Look Once) based on a Transformer architecture instead, as it is better suited for the requirements of real-time object detection. Specifically, we use the Ultralytics YOLOv11 model, which combines high detection accuracy with fast inference time, making it ideal for application in the agricultural environment. The model marks objects with boxes called bounding boxes, or bboxes.

The next step was to find a suitable dataset to train the model. Since publicly available datasets for this specific application area are limited, the search proved challenging. Ultimately, we chose the “Crop and Weed Dataset” from the Austrian Institute of Technology.

After developing a program to format the data so that it matches the expected input format of the model, we agreed to scale all images to a resolution of 640×640 pixels. Additionally, smaller preprocessing functionalities were implemented.

We then began training the model. Due to limited computing resources, we were only able to use the smallest model variant, YOLOv11-M. The training ultimately resulted in a theoretically functioning AI model specialized for our application.
The evaluation of the above statistics as well as the example image shown reveal an uneven distribution of classes (plant species) in the Crop and Weed Dataset. This led to an unexpectedly erroneous classification in the example: the AI detects grass disproportionately often, even in cases where other plant species are depicted.
One possible reason for this is overfitting of the model to the training data, since grass is presumably overrepresented in the dataset, causing the model to develop a skewed understanding of the class distribution.


Due to the identified quality issues in the existing dataset, we decided to create our own dataset to specifically expand the training base. This dataset is intended to supplement the existing Crop and Weed Dataset and be optimized especially for our specific requirements.


To ensure the highest possible quality and diversity in the dataset, we decided to take the required images ourselves. The goal was to generate more variation regarding lighting conditions, perspectives, image sharpness, and plant types. For this, we arranged an appointment with an organic farmer from Steudach, on whose fields we were allowed to carry out the recordings. The variety of images was further increased by using different camera models, varying camera settings, and shooting positions, including blurry or empty images to simulate real conditions. We also documented several fields with different crops and weed species to further increase the range of the dataset.


In the end, we had more than 3,000 self-recorded images with a total size of about 16 GiB.

The next step was annotating the recorded images to create a usable dataset for training the AI. For this, we chose CVAT (Computer Vision Annotation Tool), an open-source tool developed by Intel that is particularly well suited for image annotation using bounding boxes (bboxes) for YOLO models.


Due to the large number of images as well as the high plant variety per image, the annotation was a very elaborate and time-consuming task.


Citing: 

    @InProceedings{Steininger_2023_WACV,
        author    = {Steininger, Daniel and Trondl, Andreas and Croonen, Gerardus and Simon, Julia and Widhalm, Verena},
        title     = {The CropAndWeed Dataset: A Multi-Modal Learning Approach for Efficient Crop and Weed Manipulation},
        booktitle = {Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)},
        month     = {January},
        year      = {2023},
        pages     = {3729-3738}
    }
    
    Ultralytics