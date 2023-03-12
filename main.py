import kivy
from kivy.app import App
from kivy.uix.widget import Widget
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
        welcome_button.bind(on_press=self.welcome_button_event)
        self.add_widget(welcome_button)

    def welcome_button_event(self, instance):
        vfit_app.screen_manager.current = 'Menu'


# Display list of exericses
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
            temp = Button(text="Exercise " + str(i+1))

            # bind button to event
            temp.bind(on_press=self.exercise_button_event)

            exercise_layout.add_widget(temp)



        # Add Exercise Menu
        self.add_widget(exercise_layout)

    def exercise_button_event(self, instance):
        vfit_app.screen_manager.current = 'Exercise'

# Display list of exericses
class ExercisePage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 2

        self.add_widget(Label(text='VIDEO FEED'))

        self.add_widget(Label(text='REFERENCE'))

class VFITApp(App):
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

        return self.screen_manager


if __name__ == "__main__":
    vfit_app = VFITApp()
    vfit_app.run()
