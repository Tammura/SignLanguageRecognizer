# Sign Language Recognizer (SLR)

![SLR](https://res.cloudinary.com/dh79wyca2/image/upload/v1670700496/SLR_cqegm0.png "Sign Language Recongnizer")

This is an open-source Python script that uses computer vision to recognize Sign Language letters through a camera. Currently, the script can recognize only the letters in the word "HELLO". The script uses the Google MediaPipe library to detect hand movements and gestures.

### Getting Started

To run this script, you will need to have Python 3.10 or higher installed on your system. You will also need to install Poetry, a dependency manager for Python. Once you have Poetry installed, you can use it to install the required dependencies:

- `poetry install`

After installing the dependencies, you can run the script:

- `poetry run python SignLanguage.py`

### How it Works

The script uses the camera on your device to capture video frames, which are then analyzed to detect hand movements and gestures. The Google MediaPipe library provides pre-trained machine learning models that can detect landmarks on the hand, which are then used to recognize letter signs.

### Future Goals

We plan to expand the capabilities of this script to recognize additional signs beyond the letters in the word "HELLO". We also plan to add support for multiple languages beyond English.

### Contributing

We welcome contributions to this project! If you would like to contribute, please fork this repository and submit a pull request with your changes. Before submitting a pull request, please make sure that your changes are fully tested and that they adhere to our code standards.

### License

This project is licensed under the MIT License - see the LICENSE file for details.
