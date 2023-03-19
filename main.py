from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

class WelcomePage(Screen):
    pass


# Display list of exercises
class MenuPage(Screen):
    def change_exercise_name(self, exercise_name):
        print("Changing to", exercise_name)
        vfit_app.selected_exercise_name = exercise_name
        vfit_app.root.current = 'Exercise'


# Display list of exercises
class ExercisePage(Screen):
    pass


class ComponentSetupPage(Screen):
    pass
    settings_text = StringProperty("INFO GOES HERE")

    def test_voice_button(self):
        # runLoop()
        print("TEST VOICE")

    def voice_button_event(self):
        print("voice button clicked")
        self.settings_text = "VOICE CHANGED"


class WindowManager(ScreenManager):
    pass


class VFITApp(App):
    selected_exercise_name = StringProperty("")

    def build(self):
        kv = Builder.load_file("VFITApp.ky")
        return kv


if __name__ == "__main__":
    vfit_app = VFITApp()
    vfit_app.run()
