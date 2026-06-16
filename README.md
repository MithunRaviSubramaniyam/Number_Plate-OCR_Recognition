# Number Plate Recognition System

This project is a Python-based number plate recognition system that detects vehicle number plates from images and extracts the plate text using OpenCV and EasyOCR. It is useful for automatically reading vehicle registration numbers from image files.

The system processes vehicle images, detects the number plate area, improves the image when needed, and uses OCR to read the text from the plate. The detected number plate details are saved into a text file for later use.

The project uses Python as the main programming language. OpenCV is used for image processing and number plate detection, while EasyOCR is used to extract text from the detected plate. It also uses PyTorch, NumPy, and Pillow for supporting image and OCR operations.

The main features of this project include number plate detection, OCR-based text extraction, support for JPG, JPEG, and PNG image formats, automatic folder monitoring, saving detected results into a text file, and moving processed images into a separate folder.

To run this project, first clone the repository and install the required dependencies using `pip install -r requirements.txt`. If any package is missing, install `opencv-python`, `easyocr`, `torch`, `numpy`, and `pillow` manually.

After installing the dependencies, run the project using `python number_plate.py`. Before running the file, update the folder paths in `number_plate.py` according to your system. Once the script is running, add vehicle images to the input folder, and the system will automatically detect and extract the number plate text.

The project also includes sample images and an OCR demo notebook, which can be used to understand how EasyOCR reads number plate text from images.

This project can be improved further by adding a web interface, improving detection accuracy using deep learning models, adding a configuration file for paths, and updating the requirements file with all required dependencies.

Developed by Mithun Ravi.
