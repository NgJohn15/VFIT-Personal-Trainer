import sys
import pyttsx3
import speech_recognition as sr
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import pygame


class VoiceThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(VoiceThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def start(self):
        my_loop()


def speak(text):
    print("TTS:", text)
    engine.say(text)
    engine.runAndWait()


def get_command():
    # it takes mic input from the user and return string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing..")
        query = r.recognize_google(audio, language='en-in')
        print(f"user Said :{query}\n")

    except Exception as e:
        print(e)

        print("Say that again please")
        return "None"

    return query


def my_loop():
    while True:
        query = get_command().lower()

        # Logic for executing task based query
        if 'go to' in query:
            if 'welcome page' in query:
                app.change_page_to_n(WelcomePage, "Changing to Welcome Page")
            elif 'set up page' in query or 'setup page' in query:
                app.change_page_to_n(SetupPage, "Changing to Setup Page")
            elif 'exercise selection' in query:
                app.change_page_to_n(ExercisePage, "Changing to Exercise Selection")
            else:
                speak("Try Go To Command again")
        elif 'go back' in query:
            app.change_to_previous()
        elif 'click on' in query:
            if 'welcome button' in query and app.current_page == "Welcome":
                app.change_page_to_n(SetupPage, "Setup")
            elif 'ready button' in query and app.current_page == "Setup":
                app.change_page_to_n(ExercisePage, "Exercise selection")
        elif 'exit program' in query:
            speak("exiting V-FIT PT")
            app.quit()
            break  # exit loop and thread will end


class VFITApp(tk.Tk):
    current_page = ""
    previous_page = ""

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Escape fullscreen
        self.bind("<Escape>", lambda event: self.attributes("-fullscreen", False))
        # Fullscreen
        self.attributes("-fullscreen", True)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        welcome_frame = WelcomePage(container, self)
        setup_frame = SetupPage(container, self)
        exercise_frame = ExercisePage(container, self)
        video_frame = VideoPage(container, self)

        self.frames[WelcomePage] = welcome_frame
        self.frames[SetupPage] = setup_frame
        self.frames[ExercisePage] = exercise_frame
        self.frames[VideoPage] = video_frame

        setup_frame.grid(row=0, column=0, sticky="nsew")
        welcome_frame.grid(row=0, column=0, sticky="nsew")
        exercise_frame.grid(row=0, column=0, sticky="nsew")
        video_frame.grid(row=0, column=0, sticky="nsew")

        self.current_page = WelcomePage.name
        self.show_frame(WelcomePage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def change_page_to_n(self, page, msg: str):
        """
        Changes current to provided page then TTS msg
        :param page: Destination page
        :param msg: Msg to spoken out loud
        :return: void
        """
        # Update App Data
        app.previous_page = app.current_page
        app.current_page = page.name

        self.show_frame(page)
        speak(msg)

    def change_to_previous(self):
        msg = "Going back"
        if app.previous_page == 'Welcome':
            self.change_page_to_n(WelcomePage, msg)
        elif app.previous_page == 'Setup':
            self.change_page_to_n(SetupPage, msg)
        elif app.previous_page == 'Exercise':
            self.change_page_to_n(ExercisePage, msg)
        elif app.previous_page == 'Video':
            self.change_page_to_n(VideoPage, msg)

    def end_fullscreen(self):
        self.attributes("-fullscreen", False)


class WelcomePage(tk.Frame):
    name = "Welcome"

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        # WelcomeButton
        welcome_btn = ttk.Button(self, text="Welcome", command=lambda: self.welcome_button_pressed())
        # welcome_btn = ttk.Button(self, text="Welcome", command=lambda: self.welcome_button_pressed("arg"))
        welcome_btn.place(relx=.5, rely=.5, anchor='center', relheight=0.5, relwidth=0.5)

    def welcome_button_pressed(self):
        app.change_page_to_n(SetupPage, "")

    # function with arguments
    # def welcome_button_pressed(self, arg):
    #     print(arg)


class SetupPage(tk.Frame):
    name = "Setup"

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # WelcomeButton
        mic_test_btn = ttk.Button(self, text="Mic Test", command=lambda: self.mic_test())
        mic_test_btn.place(relx=.3, rely=.15, anchor='center', relheight=0.2, relwidth=0.3)
        pygame.mixer.init()  # todo no volume
        sound = pygame.mixer.Sound("sounds/ding.wav")
        mic_rec_btn = ttk.Button(self, text="Mic Recognition", command=lambda: get_command())
        mic_rec_btn.place(relx=.7, rely=.15, anchor='center', relheight=0.2, relwidth=0.3)

        def play_sound(self):
            # Get the volume value from the slider
            new_volume = volume_slider.get()
            snapped_value = int(round(float(new_volume) / 10)) * 10

            # print(snapped_value)
            # print(new_volume)
            # Set the volume of the sound
            sound.set_volume(snapped_value)
            # Play the sound
            sound.play()

        volume_slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient='horizontal',
            command=play_sound)

        volume_slider.get()
        volume_slider.place(relx=.6, rely=.5, anchor='center', relheight=0.2, relwidth=0.5)

        text = Label(self, text="Audio")
        text.config(font=("Courier", 14))
        text.place(relx=.2, rely=.5, anchor='center', relheight=0.1, relwidth=0.1)
        ready_btn = ttk.Button(self, text="Ready !", command=lambda: app.change_page_to_n(ExercisePage, ""))
        ready_btn.place(relx=.5, rely=.75, anchor='center', relheight=0.2, relwidth=0.4)

    def mic_test(self):
        speak("Listening")
        speak("You said " + get_command())


class ExercisePage(tk.Frame):
    name = "Exercise"

    def __init__(self, parent, controller):
        bicep = tk.PhotoImage(file='exercises/bicep-clipart-11.png')
        tk.Frame.__init__(self, parent)
        bicep_btn = ttk.Button(self, text="Bicep", command=lambda: self.select_exercise(""))
        bicep_btn.place(relx=0.2, rely=0.5, anchor='center', relheight=0.75, relwidth=0.15)

        lunge_btn = ttk.Button(self, text="Lunge", command=lambda: self.select_exercise(""))
        lunge_btn.place(relx=0.4, rely=0.5, anchor='center', relheight=0.75, relwidth=0.15)

        squat_btn = ttk.Button(self, text="Squat", command=lambda: self.select_exercise(""))
        squat_btn.place(relx=0.6, rely=0.5, anchor='center', relheight=0.75, relwidth=0.15)

        jumping_btn = ttk.Button(self, text="Jumping", command=lambda: self.select_exercise(""))
        jumping_btn.place(relx=0.8, rely=0.5, anchor='center', relheight=0.75, relwidth=0.15)

    def select_exercise(self, *arg):
        app.change_page_to_n(VideoPage, "")


class VideoPage(tk.Frame):
    name = "Video"

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # insert video feed and ref video


if __name__ == "__main__":
    engine = pyttsx3.init('sapi5')  # Windows
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    app = VFITApp()
    # run voice recognition thread
    task = threading.Thread(target=my_loop, args=())  # it has to be `,` in `(queue,)` to create tuple with one value
    task.start()  # start thread
    app.mainloop()
    task.join()  # wait for end of thread
    app.bind("<Destroy>", sys.exit(0))  # TODO: if user closes app, close voice recognition