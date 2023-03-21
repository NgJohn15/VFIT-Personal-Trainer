# VFIT-Personal-Trainer

The code is written in Python 3 and Kivy, and is used to create a voice-controlled fitness application. This application includes a welcome page, a component setup page, a menu page, an exercise page, and a workout page.

The welcome page is used to greet the user and allow them to begin the process of setting up their components. The component setup page allows the user to test their microphone and camera, and change their voice settings if they wish. The menu page allows the user to select an exercise they wish to do.

The exercise page displays a camera feed and instructions for the exercise, as well as a start button for beginning the workout. The workout page displays instructions for the exercise and a stop button for ending the workout.

The code makes use of several libraries, including cv2 for accessing the camera, speech_recognition for recognizing speech from the microphone, and kivymd for creating the user interface. It also creates a global variable for storing the selected exercise name and a KivyCamera class for displaying the camera feed.

The main.py file contains the code for the application, including functions for recognizing speech from the microphone, changing the global variable for the exercise name, and loading the video frame from the camera. It also contains the classes for each page of the application, including the WelcomePage, MenuPage, ExercisePage, and WorkoutPage.

The code also contains a runLoop function for starting a listener thread and a listener function for recognizing speech and performing the associated action. The runLoop function is called from the VFITApp class and the listener function is called from the listener thread.

The VFITApp class is used to build the application and load the .ky file, which contains the Kivy code for the application. This includes the code for the layout of each page and the code for the components on each page.