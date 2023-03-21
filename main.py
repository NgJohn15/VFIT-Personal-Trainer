import cv2
from kivy.core.audio import SoundLoader
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
        print("updateing")
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

    def play_sound(self, value):
        sound = SoundLoader.load('ding.wav')
        vfit_app.volume = value/100.0
        sound.volume = vfit_app.volume
        if sound:
            sound.play()
    def my_value(self, value):
        print(value)

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


class VFITApp(MDApp):
    selected_exercise_name = StringProperty("")
    volume = 0.5  # default voluime

    def build(self):
        kv = Builder.load_file("VFITApp.ky")
        return kv


if __name__ == "__main__":
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
    vfit_app = VFITApp()
    vfit_app.run()
