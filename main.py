import cv2
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from voice import runLoop
import speech_recognition as sr
from threading import Thread
   

colors = {
    "Teal": {
        "200": "#212121",
        "500": "#212121",
        "700": "#212121",
    },
    "Red": {
        "200": "#C25554",
        "500": "#C25554",
        "700": "#C25554",
    },
    "Blue": {
        "200": "#0021A5",
        "500": "#0021A5",
        "700": "#0021A5"
    },
    "Orange": {
        "200": "#FA4616",
        "500": "#FA4616",
        "700": "#FA4616"
    },
    "Light": {
        "StatusBar": "E0E0E0",
        "AppBar": "#202020",
        "Background": "#2E3032",
        "CardsDialogs": "#FFFFFF",
        "FlatButtonDown": "#CCCCCC",
    },
}

class WelcomePage(Screen):
    pass
                
# Display list of exercises
class MenuPage(Screen):
    def change_exercise_name(self, exercise_name):
        print("Changing to", exercise_name)
        vfit_app.selected_exercise_name = exercise_name
        vfit_app.root.current = 'Exercise'

class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        print("updating")
        ret, frame = self.capture.read()
        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture



# Display list of exercises
class ExercisePage(Screen):
    name = 'Exercise'
    print("EXERCISE")

    def build(self):
        layout = MDGridLayout()
        layout.rows = 2
        print("building camera")
        layout.add_widget(MDLabel(text=vfit_app.selected_exercise_name), halign='center')
        self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.my_camera = KivyCamera(capture=self.capture, fps=60)
        layout.add_widget(self.my_camera)
        return layout

    def on_stop(self):
        #without this, app will not exit even if the window is closed
        self.capture.release()
        
class ComponentSetupPage(Screen):
    pass
    settings_text = StringProperty("INFO GOES HERE")

    def test_voice_button(self):
        # runLoop()
        print("TEST VOICE")

    def voice_button_event(self):
        print("voice button clicked")
        self.settings_text = "VOICE CHANGED"

    def test_video_button(self):
        print("test video")
        
class WindowManager(ScreenManager):
    pass

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    print("Listening...")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }


    print("Transcribing Audio...")

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response 

def listener(app):

   r = sr.Recognizer()
   print(sr.Microphone.list_microphone_names())
   mic = sr.Microphone(device_index=3)

   while True:

       response = recognize_speech_from_mic(r, mic)
       print(response["transcription"])

       if response["success"] and response["transcription"]!=None:

           transcription = response["transcription"].lower()

           if "quit" in transcription or "exit" in transcription or "close" in transcription:
               # Something to exit the app or go back to WelcomePage
               pass

           elif "start" in transcription:
               app.root.current = 'Welcome'

               exercise_button = app.root.current("Setup").ids.exercise_button
               Clock.schedule_once(lambda dt: exercise_button.trigger_action(0), 0)
               
           elif "ready" in transcription:
               app.root.current = "Menu"

               # Simulate button click
               exercise_button = app.root.current("Menu").ids.exercise_button
               Clock.schedule_once(lambda dt: exercise_button.trigger_action(0), 0)

           elif "excercise 1" in transcription:
               app.root.current = "Exercise"

               # Simulate button click
               start_button = app.root.get_screen("Exercise").ids.start_button
               Clock.schedule_once(lambda dt: start_button.trigger_action(0), 0)

           elif "stop" in transcription:
               app.root.current = "Menu"

               # Simulate button click
               stop_button = app.root.get_screen("Menu").ids.stop_button
               Clock.schedule_once(lambda dt: stop_button.trigger_action(0), 0)

       else:
           print("Unable to transcribe audio")
           
# Here, we pass the app object as a parameter to the listener function, so that we can access the Kivy UI elements from 
# within the function. We also added app as a parameter to the runLoop function and modified it to start the listener 
# thread with app as an argument:

def runLoop(app):
   listener_thread = Thread(target=listener, args=(app,))
   listener_thread.setDaemon(True)
   listener_thread.start()
   
class VFITApp(MDApp):
   def build(self):
       Builder.load_file("VFITApp.ky")
       runLoop(self)
       return WelcomePage() #to start from the welcome page, modifying this will take us to the different page (as modified) when the app runs


if __name__ == "__main__":

    # vid = cv2.VideoCapture(0)
    #
    # while (True):
    #
    #     # Capture the video frame
    #     # by frame
    #     ret, frame = vid.read()
    #
    #     # Display the resulting frame
    #     cv2.imshow('frame', frame)
    #
    #     # the 'q' button is set as the
    #     # quitting button you may use any
    #     # desired button of your choice
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
    #
    # # After the loop release the cap object
    # vid.release()
    # # Destroy all the windows
    # cv2.destroyAllWindows()
    # TODO: FIGRURE OUT CV
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
    
    vfit_app = VFITApp()
    vfit_app.run()
    