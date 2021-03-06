# Data Science & Analytics Project

## Movie Genre Prediction From Trailer Videos 

Main Focus:
* Predict testing data genre based on the training data. 

More detailed information can be found on the program source code or by clicking [here](https://docs.google.com/presentation/d/1QQ8NGCxgldaiX_JHSs7e5jC3SQUjoP4kknG1FAFB_Qo/edit?usp=sharing).

## Getting Started (How to Run the Program)

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites (How to set up your machine)

1. Navigate to the directory where is the root of this project folder.
2. Still in the directory where is the root of this project, install all its dependencies.

    ```bash
    pip3 install -r requirements.txt
    ```

    Dependencies are all listed in `requirements.txt`. To re-generate
    this file (after you've installed new packages), simply you can
    it directly on the file. If you have a problem installing the dependencies, 
    please install python system package first.

3. All the trailer videos is in MovieScope_DataSet directory. 
4. Unspecific videos genre can be cleaned with clean.py
5. Limit to 1 film per trailer can be cleaned using extra_clean.py

## How the Applications Work

The application is console-based which can be executed from the terminal. The general steps are as follows:

1. Execute create_data.py using genre e.g create_data.py [extractor] 

   **vgg16 or resnet

2. create_model.py [model_name_train]

   **mlp, spatial, or lstm

3. test_model.py [video/test] [....] [....]

   **If video then [video_Path] [model_filename]

   **If test then [model_name] [extractor_name]

4. The extracted feature & model will be saved on data directory

## Built With

* [OpenCV](https://pypi.org/project/opencv-python/) - 3.4.0.12
* [Keras](https://pypi.org/project/Keras/) - 2.1.6
* [Tensorflow](https://www.tensorflow.org/api_docs/python/) - 1.8.0

## Authors

* **Adityo Anggraito** - *Computer Science Student University of Indonesia* - [GitHub](https://github.com/primetime49)
* **Bryanza Novirahman** - *Computer Science Student University of Indonesia* - [GitHub](https://github.com/bryanzanr)
* **Muhammad Faiz** - *Computer Science Student University of Indonesia* - [GitHub](https://github.com/muhammadfaiz12)
* **Muhammad Izzudin Syamil** - *Computer Science Student University of Indonesia* - [GitHub](https://github.com/izzuddinsyamil)
* **Muhammad Ramadhan** - *Computer Science Student University of Indonesia* - [GitHub](https://github.com/muhramadhan)

## Source Code Reference
* [Github](https://github.com/maximus009/MovieScope)
Language Used : Python 3.5.2 (https://www.python.org/)