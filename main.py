from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button


class WelcomePage(GridLayout):
    # runs on initialization
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # initialize grid size
        self.cols = 1

        welcome_button = Button(
            text='Welcome',
            font_size='32'  # todo: change to dynamically change based on window size
            # size_hint=(1, 1),
            # pos_hint={'x': .2, 'y': .2},
        )
        welcome_button.bind(on_press=welcome_button_event)
        self.add_widget(welcome_button)


def welcome_button_event(self):
    vfit_app.screen_manager.current = 'Setup'


# Display list of exercises
class MenuPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.rows = 2

        self.add_widget(Label(text="Select an exercise to be begin"))

        # generate Exercise menu
        exercise_layout = GridLayout()
        exercise_num = 4
        exercise_layout.cols = exercise_num
        for i in range(exercise_num):
            exercise_name = "Exercise " + str(i+1)
            temp = Button(
                text=exercise_name,
                on_press=lambda *args: exercise_button_event(exercise_name, *args))

            # bind button to event
            # temp.bind(on_press=exercise_button_event(exercise_name))
            # temp.bind(on_press=lambda *args: self.exercise_button_event(exercise_name, *args))

            # Button(on_press=lambda *args: self.my_function('btn1', *args))

            exercise_layout.add_widget(temp)

        # Add Exercise Menu
        self.add_widget(exercise_layout)


def exercise_button_event(self, exercise_name):
    vfit_app.screen_manager.current = 'Exercise'
    vfit_app.selected_exercise = exercise_name


# Display list of exercises
class ExercisePage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.rows = 2
        self.exercise_label = Label(text="selected exercise: " + vfit_app.selected_exercise)  # todo: dynamically update text to selected exercise
        self.add_widget(self.exercise_label)

        feed_layout = GridLayout()
        feed_layout.cols = 2
        feed_layout.add_widget(Label(text='VIDEO FEED'))
        feed_layout.add_widget(Label(text='REFERENCE'))

        self.add_widget(feed_layout)


class ComponentSetupPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 3

        content = GridLayout()
        content.cols = 2

        # Buttons
        menu_layout = GridLayout()
        menu_layout.rows = 3

        # Video
        video_button = Button(
            text="VIDEO"
        )
        menu_layout.add_widget(video_button)
        # Voice
        voice_button = Button(
            text="VOICE",
            on_press=voice_button_event
        )
        # voice_button.bind(on_press=voice_button_event)
        menu_layout.add_widget(voice_button)
        # Audio
        audio_button = Button(
            text="AUDIO"
        )
        menu_layout.add_widget(audio_button)

        content.add_widget(menu_layout)
        content.add_widget(Label(text="INFO GOES HERE"))

        self.add_widget(Label(text="SETTINGS"))
        self.add_widget(content)
        self.add_widget(Button(text="READY?", on_press=ready_button_event))


def voice_button_event(self):
    print("voice button clicked")


def ready_button_event(self):
    vfit_app.screen_manager.current = "Menu"


class VFITApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_page = None
        self.exercise_page = None
        self.menu_page = None
        self.welcome_page = None
        self.screen_manager = None
        self.selected_exercise = ""

    def build(self):
        # We are going to use screen manager, so we can add multiple screens
        # and switch between them
        self.screen_manager = ScreenManager()

        # Initial, connection screen (we use passed in name to activate screen)
        # First create a page, then a new screen, add page to screen and screen to screen manager
        self.welcome_page = WelcomePage()
        screen = Screen(name='Welcome')
        screen.add_widget(self.welcome_page)
        self.screen_manager.add_widget(screen)

        # Menu Page
        self.menu_page = MenuPage()
        screen = Screen(name='Menu')
        screen.add_widget(self.menu_page)
        self.screen_manager.add_widget(screen)

        # Exercise Page
        self.exercise_page = ExercisePage()
        screen = Screen(name='Exercise')
        screen.add_widget(self.exercise_page)
        self.screen_manager.add_widget(screen)

        # Setup Page
        self.setup_page = ComponentSetupPage()
        screen = Screen(name='Setup')
        screen.add_widget(self.setup_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


if __name__ == "__main__":
    vfit_app = VFITApp()
    vfit_app.run()
