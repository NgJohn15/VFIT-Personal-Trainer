# VFIT-Personal-Trainer

## Description

VFIT Personal Trainer aims to use computer vision and voice recognition to promote health & fitness by assiting users in performing safe and fun exercises.


User's can select exercises using the interactive UI or by navigating with their voice. After selecting an exercise, VFIT PT will demonstrate the proper form of the exercise and will monitor the user's own form. VFIT PT has the added benefit of gamifiying popular exercises, making each repitation and set a fun miny game. Users can compete for the best score and compete on the leaderboards.

## Table of Contents (Optional)

- [Installation](#installation)
- [Usage](#usage)
- [Tools](#tools)
- [Credits](#credits)

## Installation

To get started, you'll need Python 3.9+

Download Python from the offical page [here](https://www.python.org/downloads/)

### Dependencies
Download the dependencies using 'requirements.txt'
```
python -m pip install -r requirements.txt
```

## Usage

Start the program by running the main.py file
```
python main.py
```

## Tools
### User Interface
The GUI was built using Python Tkinter. [Tkinter](https://docs.python.org/3/library/tkinter.html)
### Speech Recognition
Speech recognition was designed around Speech Recognition library [Speech Recognition](https://pypi.org/project/SpeechRecognition/)
### Pose Estimation
Pose estimation was generated through [OpenCV](https://opencv.org/) and classified through MediaPipe's [Pose](https://developers.google.com/mediapipe/solutions/vision/pose_landmarker/) model. 
### Speech to Text
Speech to text was handled using [pyttsx3](https://pypi.org/project/pyttsx3/) library

## Credits

 [John Ng](https://github.com/NgJohn15)
 
 
 [Danish Tamboli](https://github.com/danishtamboli123)
 
 
 [Ayush Shrivastava](https://github.com/Ayush2305)
