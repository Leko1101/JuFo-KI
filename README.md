Proof-of-Concept Model for Plant Detection and Labeling especially for differentiating between crops, definded interseeds and weeds.
for local training clone https://github.com/cropandweed/cropandweed-dataset, download the data to data and use convert.py to clone data to dataset folder.
Requriments: dataset folder with images folder with train folder
                                               with val folder
                            with labels folder with train folder
                                               with val folder
                                               with train.cache file
                                               with val.cache

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