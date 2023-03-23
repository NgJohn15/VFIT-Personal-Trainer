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
        if 'welcome' in query:
            app.change_to_setup_page()

        elif 'exit program' in query:
            speak("V-FIT PT is now ending")
            app.quit()
            break  # exit loop and thread will end


class VFITApp(tk.Tk):
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

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

        self.show_frame(WelcomePage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def change_to_setup_page(self):
        self.show_frame(SetupPage)
        speak("Setup")


class WelcomePage(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        # WelcomeButton
        welcome_btn = ttk.Button(self, text="Welcome", command=lambda: self.welcome_button_pressed())
        # welcome_btn = ttk.Button(self, text="Welcome", command=lambda: self.welcome_button_pressed("arg"))
        welcome_btn.place(relx=.5, rely=.5, anchor='center', relheight=0.5, relwidth=0.5)

    def welcome_button_pressed(self):
        self.controller.show_frame(SetupPage)

    # function with arguments
    # def welcome_button_pressed(self, arg):
    #     print(arg)


class SetupPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # WelcomeButton
        setup_btn = ttk.Button(self, text="Mic Test")
        setup_btn.place(relx=.3, rely=.15, anchor='center', relheight=0.2, relwidth=0.3)
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
        ready_btn = ttk.Button(self, text="Ready !", command=lambda: controller.show_frame(ExercisePage))
        ready_btn.place(relx=.5, rely=.75, anchor='center', relheight=0.2, relwidth=0.4)


class ExercisePage(tk.Frame):

    def __init__(self, parent, controller):
        bicep = tk.PhotoImage(file='exercises/bicep-clipart-11.png')
        tk.Frame.__init__(self, parent)
        bicep_btn = ttk.Button(self, text="Bicep", command=lambda: controller.show_frame(VideoPage))
        bicep_btn.place(relx=0.2, rely=0.5, anchor='center', relheight=0.75, relwidth=0.15)

        lunge_btn = ttk.Button(self, text="Lunge", command=lambda: controller.show_frame(VideoPage))
        lunge_btn.place(relx=0.4, rely=0.5, anchor='center', relheight=0.75, relwidth=0.15)

        squat_btn = ttk.Button(self, text="Squat", command=lambda: controller.show_frame(VideoPage))
        squat_btn.place(relx=0.6, rely=0.5, anchor='center', relheight=0.75, relwidth=0.15)

        jumping_btn = ttk.Button(self, text="Jumping", command=lambda: controller.show_frame(VideoPage))
        jumping_btn.place(relx=0.8, rely=0.5, anchor='center', relheight=0.75, relwidth=0.15)


class VideoPage(tk.Frame):
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
