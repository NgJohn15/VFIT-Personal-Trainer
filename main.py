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

    def build(self):
        layout = MDBoxLayout(orientation='vertical')
        self.image = Image()
        layout.add_widget(self.image)

        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.load_video, 1.0/60.0)
        return layout

    def load_video(self, *args):
        ret, frame = self.capture.read()
        buffer = cv2.flip(frame, 0).toString()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmg='ubyte')
        self.image.texture = texture
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


class VFITApp(MDApp):
    selected_exercise_name = StringProperty("")
    # capture = cv2.VideoCapture(0)
    # cam = Camera(play=True)
    def build(self):
        kv = Builder.load_file("VFITApp.ky")
        return kv


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
