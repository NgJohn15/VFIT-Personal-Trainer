import pyttsx3
import speech_recognition as sr
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import pygame
from ttkthemes import ThemedTk
from tkCamera import tkCamera
from PIL import Image, ImageTk

DEBUG = True


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
    if DEBUG:
        print("TTS:", text)
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        pass


def get_command():
    # it takes mic input from the user and return string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        if DEBUG:
            print("Listening...")
        r.pause_threshold = 0.6
        audio = r.listen(source)

    try:
        if DEBUG:
            print("Recognizing..")
        query = r.recognize_google(audio, language='en-in')
        if DEBUG:
            print(f"user Said :{query}\n")

    except Exception as e:
        if DEBUG:
            print(e)
        return "None"

    return query


def my_loop():
    while True:
        query = get_command().lower()

        # GO TO --> PAGE
        if 'go to' in query:
            if 'welcome page' in query:
                app.change_page_to_n(WelcomePage, "Changing to Welcome Page")
            elif 'set up page' in query or 'setup page' in query:
                app.change_page_to_n(SetupPage, "Changing to Setup Page")
            elif 'exercise selection' in query:
                app.change_page_to_n(
                    ExercisePage, "Changing to Exercise Selection")
            else:
                speak("I didn't understand that GO TO command")
        elif 'go back' in query:
            app.change_to_previous()

        # exit
        elif 'kill the program' in query:
            speak("exiting V-FIT PT")
            engine.stop()
            clean_video()
            app.destroy()
            break  # exit loop and thread will end

        # CLICK ON --> BTN
        elif 'click on' in query:
            if 'welcome button' in query and app.current_page == "Welcome":
                app.change_page_to_n(SetupPage, "Setup")
            elif 'ready button' in query and app.current_page == "Setup":
                app.change_page_to_n(ExercisePage, "Exercise selection")
            else:
                speak("I'm not sure what you want to click on")

        elif app.current_page == "Setup" and "ready" in query:
            app.change_page_to_n(ExercisePage, "Pick an exercise to begin!")

        elif app.current_page == "Welcome" and "let's begin" in query:
            app.change_page_to_n(SetupPage, "Starting with setup")

        elif app.current_page == "Exercise":
            # exercise selection
            if 'bicep curls' in query:
                speak("Let's do some curls!")
                app.frames[ExercisePage].select_exercise('bicep_curls')
            elif 'lunges' in query:
                speak("Here we go!")
                app.frames[ExercisePage].select_exercise('lunges')
            elif 'squats' in query:
                speak("Let's go!")
                app.frames[ExercisePage].select_exercise('squats')
            elif 'jumping jacks' in query:
                speak("Let's get to it!")
                app.frames[ExercisePage].select_exercise('jumping_jacks')
        elif app.current_page == "Video":
            if 'exit' in query or "another exercise" in query:
                app.change_page_to_n(
                    ExercisePage, 'Pick or say an exercise to begin!')
    exit(0)


def clean_video():
    # garbage collection
    for widget in app.frames[VideoPage].stream_widgets:
        widget.vid.running = False
        widget.vid.__del__()
        widget.destroy()

    app.frames[VideoPage].stream_widgets.clear()


class VFITApp(ThemedTk):
    current_page = ""
    previous_page = ""
    selected_exercise = "bicep_curls"
    volume = 50
    voice_thread = None

    prev_state = "None"
    prev_counter = 0
    prev_feedback = "None"
    dummy_var = [None, 0, None, 1]

    def gamification_data(dump, data):
        if data != app.dummy_var:
            if data[1] != app.prev_counter:
                if data[1] == 0:
                    app.prev_counter = data[1]
                elif data[1] % 15 == 0:
                    text = (
                        "Nice job. You're all done with set {}! You may now return to the exercise menu, or do another set.").format(
                        data[3])
                    threading.Thread(target=speak, args=(text,)).start()
                elif data[1] % 10 == 0:
                    threading.Thread(target=speak, args=("Ten done, Only Five more to go!",)).start()
                elif data[1] % 5 == 0:
                    threading.Thread(target=speak, args=("Five done, Ten to go!",)).start()
                app.prev_counter = data[1]

            elif str(data[2]) != app.prev_feedback:
                if str(data[2]) != "None":
                    threading.Thread(target=speak, args=(data[2],)).start()
                    app.prev_feedback = data[2]
                else:
                    app.prev_feedback = "None"

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        ThemedTk.__init__(self, *args, **kwargs, theme='radiance')
        # Escape fullscreen
        self.bind("<Escape>", lambda event: self.attributes(
            "-fullscreen", False))
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

        # perform garbage collection
        if app.previous_page == 'Video':
            clean_video()

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


class WelcomePage(tk.Frame):
    name = "Welcome"

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        image = Image.open("exercises/welcome_page.png")
        temp_image = image.resize(
            (self.winfo_screenwidth(), self.winfo_screenheight()))
        welcome_image = ImageTk.PhotoImage(temp_image)
        # WelcomeButton
        welcome_btn = tk.Button(self, image=welcome_image, compound="top", text="Welcome",
                                command=lambda: app.change_page_to_n(SetupPage, ""))
        # welcome_btn = ttk.Button(self, text="Welcome", command=lambda: self.welcome_button_pressed("arg"))
        welcome_btn.image = welcome_image
        welcome_btn.place(relx=.5, rely=.5, anchor='center',
                          relheight=1, relwidth=1)


class SetupPage(tk.Frame):
    name = "Setup"

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='white')
        # WelcomeButton
        backbtn = tk.Button(self, text="Go Back", command=lambda: app.change_page_to_n(WelcomePage, ""),
                            font=("Arial", 10), padx=30)
        backbtn.place(relx=0.016, rely=0.01, anchor='center',
                      relheight=0.02, relwidth=0.03)
        pygame.mixer.init()  # todo no volume
        sound = pygame.mixer.Sound("sounds/ding.wav")

        def play_sound(self):
            # Get the volume value from the slider
            new_volume = volume_slider.get() / 250
            snapped_value = int(round(float(new_volume) / 10)) * 10

            # print(snapped_value)
            # print(new_volume)
            # Set the volume of the sound
            sound.set_volume(new_volume)
            # Play the sound
            sound.play()

        volume_slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient='horizontal',
            command=play_sound)

        volume_slider.set(0)
        volume_slider.get()
        volume_slider.place(relx=.6, rely=.5, anchor='center',
                            relheight=0.05, relwidth=0.5)

        image = Image.open("exercises/volume_zero.png")
        temp_image = image.resize(
            (self.winfo_screenwidth() // 20, self.winfo_screenheight() // 17))
        volume_down_image = ImageTk.PhotoImage(temp_image)
        volume_zero_btn = tk.Button(self, image=volume_down_image, compound="top",
                                    command=lambda: volume_slider.set(0))
        volume_zero_btn.image = volume_down_image
        volume_zero_btn.place(relx=0.3, rely=0.5,
                              anchor='center', relheight=0.06, relwidth=0.05)
        volume_zero_btn.configure(bg='white', fg='black')

        image = Image.open("exercises/volume_full.png")
        temp_image = image.resize(
            (self.winfo_screenwidth() // 23, self.winfo_screenheight() // 18))
        volume_up_image = ImageTk.PhotoImage(temp_image)
        volume_full_btn = tk.Button(self, image=volume_up_image, compound="top",
                                    command=lambda: volume_slider.set(100))
        volume_full_btn.image = volume_up_image
        volume_full_btn.place(relx=0.9, rely=0.5,
                              anchor='center', relheight=0.06, relwidth=0.05)
        volume_full_btn.configure(bg='white', fg='black')

        text = Label(self, text="System Volume")
        text.config(font=("Courier", 14))
        text.place(relx=.15, rely=.5, anchor='center',
                   relheight=0.045, relwidth=0.0775)

        mic_rec_btn = tk.Button(self, text="Mic Recognition",
                                command=lambda: self.mic_test(), font=("Arial", 40))
        mic_rec_btn.place(relx=.3, rely=.75, anchor='center',
                          relheight=0.2, relwidth=0.3)
        ready_btn = tk.Button(self, text="Ready !", command=lambda: app.change_page_to_n(ExercisePage, ""),
                              font=("Arial", 40))
        ready_btn.place(relx=.7, rely=.75, anchor='center',
                        relheight=0.2, relwidth=0.3)

    def mic_test(self):
        speak("Listening")
        speak("You said " + get_command())


class ExercisePage(tk.Frame):
    name = "Exercise"

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='white')
        backbtn = tk.Button(self, text="Go Back", command=lambda: app.change_page_to_n(SetupPage, ""),
                            font=("Arial", 10), padx=30)
        backbtn.place(relx=0.016, rely=0.01, anchor='center',
                      relheight=0.02, relwidth=0.03)

        image = Image.open("exercises/curls.png")
        temp_image = image.resize(
            (self.winfo_screenwidth() // 5, self.winfo_screenheight() // 3))
        bicep_image = ImageTk.PhotoImage(temp_image)
        bicep_btn = tk.Button(self, text="Bicep Curls", image=bicep_image, compound="top",
                              command=lambda: self.select_exercise("bicep_curls"), font=("Arial", 40), pady=100)
        bicep_btn.image = bicep_image
        bicep_btn.place(relx=0.2, rely=0.5, anchor='center',
                        relheight=0.62, relwidth=0.15)
        bicep_btn.configure(bg='white', fg='black')

        image = Image.open("exercises/lunges.png")
        temp_image = image.resize(
            (self.winfo_screenwidth() // 5, self.winfo_screenheight() // 3))
        lunges_image = ImageTk.PhotoImage(temp_image)
        lunge_btn = tk.Button(self, text="Lunges", image=lunges_image, compound="top",
                              command=lambda: self.select_exercise("lunges"), font=("Arial", 40), pady=100)
        lunge_btn.image = lunges_image
        lunge_btn.place(relx=0.4, rely=0.5, anchor='center',
                        relheight=0.62, relwidth=0.15)
        lunge_btn.configure(bg='white', fg='black')

        image = Image.open("exercises/squat.png")
        temp_image = image.resize(
            (self.winfo_screenwidth() // 7, self.winfo_screenheight() // 3))
        squats_image = ImageTk.PhotoImage(temp_image)
        squat_btn = tk.Button(self, text="Squats", image=squats_image, compound="top",
                              command=lambda: self.select_exercise("squats"), font=("Arial", 40), pady=100)
        squat_btn.image = squats_image
        squat_btn.place(relx=0.6, rely=0.5, anchor='center',
                        relheight=0.62, relwidth=0.15)
        squat_btn.configure(bg='white', fg='black')

        image = Image.open("exercises/jumping-jacks.png")
        temp_image = image.resize(
            (self.winfo_screenwidth() // 5, self.winfo_screenheight() // 3))
        jumping_image = ImageTk.PhotoImage(temp_image)
        jumping_btn = tk.Button(self, text="Jumping\nJacks", image=jumping_image, compound="top",
                                command=lambda: self.select_exercise("jumping_jacks"), font=("Arial", 40), pady=100)
        jumping_btn.image = jumping_image
        jumping_btn.place(relx=0.8, rely=0.5, anchor='center',
                          relheight=0.62, relwidth=0.15)
        jumping_btn.configure(bg='white', fg='black')

    def select_exercise(self, exercise_name):
        app.change_page_to_n(VideoPage, "")
        app.selected_exercise = exercise_name
        app.frames[VideoPage].update_sources()
        speak("Try to follow the reference video on the right")


class VideoPage(tk.Frame):
    name = "Video"

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.stream_widgets = []
        self.width = self.winfo_screenwidth() // 2
        self.height = self.winfo_screenheight()

    def update_sources(self):
        # garbage collection

        clean_video()
        # for widget in self.stream_widgets:
        #     widget.vid.running = False
        #     widget.vid.__del__()
        #     widget.destroy()

        self.stream_widgets.clear()
        if DEBUG:
            print("updating to", app.selected_exercise)
        for number, (text, source, exercise_type) in enumerate(self.get_sources(app.selected_exercise)):
            widget = tkCamera(self, text, source, self.width,
                              self.height, exercise_type=exercise_type)
            widget.set_app(app)
            widget.grid(row=0, column=number)
            self.stream_widgets.append(widget)

    def get_sources(self, exercise):
        sources = [  # (text, source)
            # local webcams
            ("me", 0, str(exercise)),  # ~~~~
            # remote videos (or streams)
            (
                "Zakopane, Poland",
                "./exercises/" + str(exercise) + ".mp4", "None"  # ~~~~
            ),
        ]
        return sources


if __name__ == "__main__":
    engine = pyttsx3.init('sapi5')  # Windows
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    # run voice recognition thread
    # it has to be `,` in `(queue,)` to create tuple with one value
    task = threading.Thread(target=my_loop, args=())
    app = VFITApp()
    task.start()  # start thread
    app.mainloop()
    task.join()  # wait for end of thread

    engine.stop()
