import datetime
import os
import pyttsx3
import speech_recognition as sr
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import *
import pygame
from ttkthemes import ThemedTk
from tkCamera import tkCamera
from PIL import Image, ImageTk
import pandas as pd
import textwrap3

DEBUG = True
TEST = True


def wrap(string, lenght=50):
    return '\n'.join(textwrap3.wrap(string, lenght))


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


def get_voice_command():
    while True:
        query = get_command().lower()

        # exit
        if 'kill the program' in query:
            speak("exiting V-FIT PT")
            clean_video()
            app.destroy()
            engine.stop()
            exit(0)

        # GO TO --> PAGE
        elif 'go to' in query:
            if 'welcome page' in query:
                app.change_page_to_n(WelcomePage, "Changing to Welcome Page")
            elif 'set up page' in query or 'setup page' in query:
                app.change_page_to_n(SetupPage, "Changing to Setup Page")
            elif 'exercise selection' in query:
                app.change_page_to_n(
                    ExercisePage, "Changing to Exercise Selection")
            elif 'scoreboard' in query:
                app.change_page_to_n(Scoreboard, "Changing to Scoreboard")
            else:
                speak("I didn't understand that GO TO command")
        elif 'go back' in query:
            app.change_to_previous()

        # CLICK ON --> BTN
        elif 'click on' in query:
            if 'welcome button' in query and app.current_page == "Welcome":
                app.change_page_to_n(SetupPage, "Setup")
            elif 'ready button' in query and app.current_page == "Setup":
                app.change_page_to_n(ExercisePage, "Exercise selection")
            else:
                speak("I'm not sure what you want to click on")

        # SETUP Page
        elif app.current_page == "Setup" and "ready" in query:
            app.change_page_to_n(ExercisePage, "Pick an exercise to begin!")

        # WELCOME Page
        elif app.current_page == "Welcome" and "let's begin" in query:
            app.change_page_to_n(SetupPage, "Starting with setup")

        # Exercise Page
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
        # Video Page
        elif app.current_page == "Video":
            if 'exit' in query or "another exercise" in query:
                app.change_page_to_n(
                    ExercisePage, 'Pick or say an exercise to begin!')
        # Ignore empty prompts
        elif "" == query:
            pass
        # Inform user
        else:
            speak("I didn't catch that. Please speak slowly and clearly.")


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

    exercise_start_time = None
    filepath = None

    # User Data
    total_voice_commands = 0
    total_click_commands = 0
    squat_completion_time = None
    bicep_curl_completion_time = None
    jumping_jack_completion_time = None
    lunge_completion_time = None

    def gamification_data(dump, data):
        if data != app.dummy_var:
            if data[1] != app.prev_counter:
                if data[1] == 0:
                    app.prev_counter = data[1]
                elif data[1] % 15 == 0:
                    if TEST:
                        if app.selected_exercise == 'bicep_curls':
                            app.bicep_curl_completion_time = datetime.datetime.now() - app.exercise_start_time
                            write_data(app.filepath, "BicepCurls_Completion_Time " + str(app.bicep_curl_completion_time))
                        elif app.selected_exercise == 'jumping_jacks':
                            app.jumping_jack_completion_time = datetime.datetime.now() - app.exercise_start_time
                            write_data(app.filepath, "JumpingJacks_Completion_time " + str(app.jumping_jack_completion_time))
                        elif app.selected_exercise == 'squats':
                            app.squat_completion_time = datetime.datetime.now() - app.exercise_start_time
                            write_data(app.filepath, "Squats_Completion_Time " + str(app.squat_completion_time))
                        elif app.selected_exercise == 'lunges':
                            app.lunge_completion_time = datetime.datetime.now() - app.exercise_start_time
                            write_data(app.filepath, "Lunges_Completion_Time " + str(app.lunge_completion_time))

                    text = (
                        "Nice job. You're all done with set {}! You may now return to the exercise menu, or do another set.").format(
                        data[3])
                    threading.Thread(target=speak, args=(text,)).start()
                elif data[1] % 10 == 0:
                    threading.Thread(target=speak, args=(
                        "Ten done, Only Five more to go!",)).start()
                elif data[1] % 5 == 0:
                    threading.Thread(target=speak, args=(
                        "Five done, Ten to go!",)).start()
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
        introduction_frame = IntroductionPage(container, self)
        setup_frame = SetupPage(container, self)
        exercise_frame = ExercisePage(container, self)
        video_frame = VideoPage(container, self)
        scoreboard_frame = Scoreboard(container, self)

        self.frames[WelcomePage] = welcome_frame
        self.frames[IntroductionPage] = introduction_frame
        self.frames[SetupPage] = setup_frame
        self.frames[ExercisePage] = exercise_frame
        self.frames[VideoPage] = video_frame
        self.frames[Scoreboard] = scoreboard_frame

        setup_frame.grid(row=0, column=0, sticky="nsew")
        welcome_frame.grid(row=0, column=0, sticky="nsew")
        introduction_frame.grid(row=0, column=0, sticky="nsew")
        exercise_frame.grid(row=0, column=0, sticky="nsew")
        video_frame.grid(row=0, column=0, sticky="nsew")
        scoreboard_frame.grid(row=0, column=0, sticky="nsew")

        self.current_page = WelcomePage.name
        self.show_frame(WelcomePage)

    def show_frame(self, cont):
        """
        Display frame on GUI
        :param cont: Frame Class
        :return: void
        """
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
        """
        Changes to previous frame if possible
        :return: void
        """
        msg = "Going back"
        if app.previous_page == 'Welcome':
            self.change_page_to_n(WelcomePage, msg)
        elif app.previous_page == 'Introduction':
            self.change_page_to_n(IntroductionPage, msg)
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
        self.configure(bg='white')

        image = Image.open("exercises/welcome_page.png")
        temp_image = image.resize(
            (self.winfo_screenwidth(), self.winfo_screenheight()))
        welcome_image = ImageTk.PhotoImage(temp_image)
        # WelcomeButton
        welcome_btn = tk.Button(self, image=welcome_image, compound="top",
                                command=lambda: app.change_page_to_n(IntroductionPage, ""), highlightthickness=0, bd=0,
                                bg="white", activebackground='white')
        # welcome_btn = ttk.Button(self, text="Welcome", command=lambda: self.welcome_button_pressed("arg"))
        welcome_btn.image = welcome_image
        welcome_btn.place(relx=.5, rely=.5, anchor='center',
                          relheight=1, relwidth=1)


class IntroductionPage(tk.Frame):
    name = "Introduction"

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg='white')

        backbtn_image = ImageTk.PhotoImage(Image.open("ui_elements/back_btn.png").convert(mode="RGBA").resize(
            (self.winfo_screenheight() // 15, self.winfo_screenheight() // 15)))
        backbtn = tk.Button(self, image=backbtn_image, command=lambda: app.change_page_to_n(
            WelcomePage, ""), highlightthickness=0, bd=0, bg="white", activebackground='white')
        backbtn.image = backbtn_image
        backbtn.place(relx=((self.winfo_screenwidth() // 20) / self.winfo_screenwidth() * 9 / 16),
                      rely=(1 - (self.winfo_screenheight() // 20) / self.winfo_screenheight()), anchor='center')

        voice_commands_list = tk.Label(self, text="VOICE COMMANDS")
        voice_commands_list.config(
            font=("Helvetica", 24), bd=0, bg="white", activebackground='white', foreground="#223063")
        voice_commands_list.place(relx=0.5, rely=0.05, anchor="center")

        df = pd.read_excel("excelfiles\commands.xlsx")

        tree = ttk.Treeview(self)
        tree['show'] = 'headings'
        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview",
                        font=("Helvetica", 16),
                        rowheight=64,
                        background="black",
                        foreground="white",
                        fieldbackground="black")

        style.map("Treeview", background=[('selected', 'grey')])
        tree["columns"] = list(df.columns)

        style.configure('Treeview.Heading',
                        background="white",
                        foreground="#223063",
                        font=("Helvetica", 16),
                        rowheight=64,
                        fieldbackground="white")
        # Add column headings
        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center')

        # Add rows to the table
        for i, row in df.iterrows():
            temp_arr = []
            for line in row:
                temp_arr.append(wrap(line, 32))
            tree.insert("", "end", values=temp_arr, tags=(
                'oddrow',) if i % 2 == 0 else ('evenrow',))

        tree_scroll = ttk.Scrollbar(
            tree, orient="vertical", command=tree.yview)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        style.configure("Vertical.TScrollbar",
                        background="#6279CA",
                        fieldbackground="#6279CA",
                        arrowcolor="white",
                        troughcolor="#223063",
                        )

        tree.configure(yscrollcommand=tree_scroll.set)
        tree.tag_configure('oddrow', background='#223063')
        tree.tag_configure('evenrow', background='#314792')
        tree.place(relx=0.5, rely=0.5,
                   relheight=(1 - (self.winfo_screenheight() // 5) / self.winfo_screenheight()),
                   relwidth=1 - ((self.winfo_screenwidth() // 5) / self.winfo_screenwidth() * 9 / 16), anchor="center")

        next_btn_image = ImageTk.PhotoImage(Image.open("ui_elements/next_btn.png").convert(mode="RGBA").resize(
            (self.winfo_screenheight() // 15, self.winfo_screenheight() // 15)))
        next_btn = tk.Button(self, image=next_btn_image, command=lambda: app.change_page_to_n(SetupPage, ""),
                             font=("Helvetica", 10), highlightthickness=0, bd=0, bg="white", activebackground='white')
        next_btn.image = next_btn_image
        next_btn.place(relx=(1 - (self.winfo_screenwidth() // 20) / self.winfo_screenwidth() * 9 / 16),
                       rely=(1 - (self.winfo_screenheight() // 20) / self.winfo_screenheight()), anchor='center')


class SetupPage(tk.Frame):
    name = "Setup"

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='white')

        # WelcomeButton
        backbtn_image = ImageTk.PhotoImage(Image.open("ui_elements/back_btn.png").convert(mode="RGBA").resize(
            (self.winfo_screenheight() // 15, self.winfo_screenheight() // 15)))
        backbtn = tk.Button(self, image=backbtn_image, command=lambda: app.change_page_to_n(IntroductionPage, ""),
                            font=("Helvetica", 10), highlightthickness=0, bd=0, bg="white", activebackground='white')
        backbtn.image = backbtn_image
        backbtn.place(relx=((self.winfo_screenwidth() // 20) / self.winfo_screenwidth() * 9 / 16),
                      rely=(1 - (self.winfo_screenheight() // 20) / self.winfo_screenheight()), anchor='center')

        pygame.mixer.init()  # todo no volume

        def play_sound(self):
            """
            Plays ding sound
            :param self: dummy self
            :return:
            """
            sound = pygame.mixer.Sound("sounds/ding.wav")
            # Get the volume value from the slider
            new_volume = volume_slider.get() / 250
            # Set the volume of the sound
            sound.set_volume(new_volume)
            # Play sound
            sound.play()

        volume_slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient='horizontal',
            command=play_sound)

        volume_slider.set(0)
        volume_slider.get()
        volume_slider.place(relx=.5, rely=.5, anchor='center',
                            relheight=(self.winfo_screenheight() // 30) / self.winfo_screenheight(), relwidth=0.4)
        style = ttk.Style()
        style.configure("TScale",
                        background="#6279CA",
                        fieldbackground="#6279CA",
                        arrowcolor="black",
                        troughcolor="#223063",
                        )

        vol_down_image = ImageTk.PhotoImage(Image.open("ui_elements/volume_zero.png").convert(mode="RGBA").resize(
            (self.winfo_screenheight() // 15, self.winfo_screenheight() // 15)))
        volume_zero_btn = tk.Button(self, image=vol_down_image,
                                    command=lambda: volume_slider.set(0), highlightthickness=0, bd=0, bg="white",
                                    activebackground='white')
        volume_zero_btn.image = vol_down_image
        volume_zero_btn.place(relx=0.25, rely=0.5,
                              anchor='center')
        volume_zero_btn.configure(bg='white', fg='white')

        vol_up_image = ImageTk.PhotoImage(Image.open("ui_elements/volume_full.png").convert(mode="RGBA").resize(
            (self.winfo_screenheight() // 15, self.winfo_screenheight() // 15)))
        volume_full_btn = tk.Button(self, image=vol_up_image,
                                    command=lambda: volume_slider.set(100), highlightthickness=0, bd=0, bg="white",
                                    activebackground='white')
        volume_full_btn.image = vol_up_image
        volume_full_btn.place(relx=0.75, rely=0.5,
                              anchor='center')
        volume_full_btn.configure(bg='white', fg='white')

        text = tk.Label(self, text="SFX Volume")
        text.config(font=("Helvetica", 16), bd=0, bg="white", activebackground='white', foreground="#223063")
        text.place(relx=0.5, rely=0.55, anchor='center')

        mic_image = ImageTk.PhotoImage(Image.open("ui_elements/mic_test.png").convert(mode="RGBA").resize(
            (self.winfo_screenheight() // 10, self.winfo_screenheight() // 10)))
        mic_rec_btn = tk.Button(self, text="TEST MIC", image=mic_image, compound='top',
                                command=lambda: self.mic_test(), font=("Helvetica", 16), highlightthickness=0, bd=0,
                                bg="white", activebackground='white', foreground="#223063")
        mic_rec_btn.image = mic_image
        mic_rec_btn.place(relx=.5, rely=0.75, anchor='center')

        next_btn_image = ImageTk.PhotoImage(Image.open("ui_elements/next_btn.png").convert(mode="RGBA").resize(
            (self.winfo_screenheight() // 15, self.winfo_screenheight() // 15)))
        next_btn = tk.Button(self, image=next_btn_image, command=lambda: app.change_page_to_n(ExercisePage, ""),
                             font=("Helvetica", 10), highlightthickness=0, bd=0, bg="white", activebackground='white')
        next_btn.image = next_btn_image
        next_btn.place(relx=(1 - (self.winfo_screenwidth() // 20) / self.winfo_screenwidth() * 9 / 16),
                       rely=(1 - (self.winfo_screenheight() // 20) / self.winfo_screenheight()), anchor='center')

    def mic_test(self):
        """
        Functional call for Mic Test Button, calls voice recongition function
        :return: void
        """
        speak("Listening")
        speak("You said " + get_command())


class ExercisePage(tk.Frame):
    name = "Exercise"

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='white')

        backbtn_image = ImageTk.PhotoImage(Image.open("ui_elements/back_btn.png").convert(mode="RGBA").resize(
            (self.winfo_screenheight() // 15, self.winfo_screenheight() // 15)))
        backbtn = tk.Button(self, image=backbtn_image, command=lambda: app.change_page_to_n(SetupPage, ""),
                            font=("Helvetica", 10), highlightthickness=0, bd=0, bg="white", activebackground='white')
        backbtn.image = backbtn_image
        backbtn.place(relx=((self.winfo_screenwidth() // 20) / self.winfo_screenwidth() * 9 / 16),
                      rely=(1 - (self.winfo_screenheight() // 20) / self.winfo_screenheight()), anchor='center')

        image = Image.open("exercises/curls.png")
        temp_image = image.resize(
            (self.winfo_screenwidth() // 5, int(self.winfo_screenwidth() // 5) * 16 // 9))
        bicep_image = ImageTk.PhotoImage(temp_image)
        bicep_btn = tk.Button(self, image=bicep_image, compound="top",
                              command=lambda: self.select_exercise("bicep_curls"), highlightthickness=0, bd=0,
                              bg="white", activebackground='white')
        bicep_btn.image = bicep_image
        bicep_btn.place(relx=0.14, rely=0.5, anchor='center',
                        relheight=(int(self.winfo_screenwidth() // 5) * 16 // 9 / self.winfo_screenheight()),
                        relwidth=((self.winfo_screenwidth() // 5) / self.winfo_screenwidth()))
        bicep_btn.configure(bg='white', fg='black')

        image = Image.open("exercises/lunges.png")
        temp_image = image.resize(
            (self.winfo_screenwidth() // 5, int(self.winfo_screenwidth() // 5) * 16 // 9))
        lunges_image = ImageTk.PhotoImage(temp_image)
        lunge_btn = tk.Button(self, image=lunges_image, compound="top",
                              command=lambda: self.select_exercise("lunges"), font=("Helvetica", 40),
                              highlightthickness=0, bd=0, bg="white", activebackground='white')
        lunge_btn.image = lunges_image
        lunge_btn.place(relx=0.38, rely=0.5, anchor='center',
                        relheight=(int(self.winfo_screenwidth() // 5) * 16 // 9 / self.winfo_screenheight()),
                        relwidth=((self.winfo_screenwidth() // 5) / self.winfo_screenwidth()))
        lunge_btn.configure(bg='white', fg='black')

        image = Image.open("exercises/squat.png")
        temp_image = image.resize(
            (self.winfo_screenwidth() // 5, int(self.winfo_screenwidth() // 5) * 16 // 9))
        squats_image = ImageTk.PhotoImage(temp_image)
        squat_btn = tk.Button(self, image=squats_image, compound="top",
                              command=lambda: self.select_exercise("squats"), font=("Helvetica", 40),
                              highlightthickness=0, bd=0, bg="white", activebackground='white')
        squat_btn.image = squats_image
        squat_btn.place(relx=0.62, rely=0.5, anchor='center',
                        relheight=(int(self.winfo_screenwidth() // 5) * 16 // 9 / self.winfo_screenheight()),
                        relwidth=((self.winfo_screenwidth() // 5) / self.winfo_screenwidth()))
        squat_btn.configure(bg='white', fg='black')

        image = Image.open("exercises/jumping-jacks.png")
        temp_image = image.resize(
            (self.winfo_screenwidth() // 5, int(self.winfo_screenwidth() // 5) * 16 // 9))
        jumping_image = ImageTk.PhotoImage(temp_image)
        jumping_btn = tk.Button(self, image=jumping_image, compound="top",
                                command=lambda: self.select_exercise("jumping_jacks"), font=("Helvetica", 40),
                                highlightthickness=0, bd=0, bg="white", activebackground='white')
        jumping_btn.image = jumping_image
        jumping_btn.place(relx=0.86, rely=0.5, anchor='center',
                          relheight=(int(self.winfo_screenwidth() // 5) * 16 // 9 / self.winfo_screenheight()),
                          relwidth=((self.winfo_screenwidth() // 5) / self.winfo_screenwidth()))
        jumping_btn.configure(bg='white', fg='black')

    def select_exercise(self, exercise_name):
        """
        Selects the current exercise and updates frame
        :param exercise_name: Exercise selected
        :return: void
        """
        app.change_page_to_n(VideoPage, "")
        app.selected_exercise = exercise_name
        if TEST:
            app.exercise_start_time = datetime.datetime.now()
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
        """
        Updates the video source file
        :return: void
        """

        # garbage collection
        clean_video()
        self.stream_widgets.clear()

        if DEBUG:
            print("updating to", app.selected_exercise)
        for number, (text, source, exercise_type) in enumerate(self.get_sources(app.selected_exercise)):
            widget = tkCamera(self, text, source, self.width,
                              self.height, exercise_type=exercise_type)
            widget.set_app(app)
            widget.grid(row=0, column=number)
            self.stream_widgets.append(widget)

            backbtn_image = ImageTk.PhotoImage(Image.open("ui_elements/back_btn.png").convert(mode="RGBA").resize(
                (self.winfo_screenheight() // 15, self.winfo_screenheight() // 15)))
            backbtn = tk.Button(self, image=backbtn_image, command=lambda: app.change_page_to_n(ExercisePage, ""),
                                font=("Helvetica", 10), highlightthickness=0, bd=0, bg="white",
                                activebackground='white')
            backbtn.image = backbtn_image
            backbtn.place(relx=((self.winfo_screenwidth() // 20) / self.winfo_screenwidth() * 9 / 16),
                          rely=(1 - (self.winfo_screenheight() // 20) / self.winfo_screenheight()), anchor='center')

    def get_sources(self, exercise):
        """
        Formats source file for video player
        :param exercise: name of exercise
        :return: source dict in proper format
        """
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


class Scoreboard(tk.Frame):
    name = "Scoreboard"

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


def write_data(file, data: str):
    """
    Appends data to file, assumes file exists
    :param file: filepath
    :param data: data to be written
    :return: void
    """
    with open(file, 'a') as f:
        f.write(data)
        f.write('\n')


if __name__ == "__main__":
    # initialize app
    app = VFITApp()

    # Data collection metrics file location
    filepath = "./data/"
    ct = datetime.datetime.now()
    id_num = ct.strftime("%y%m%d%H%M")
    filename = id_num + '.txt'
    app.filepath = filepath+filename
    os.makedirs(os.path.dirname(app.filepath), exist_ok=True)
    with open(app.filepath, "w") as f:
        f.write(ct.strftime("%m/%d/%y)") + '\n')
        f.write("Data Begins Below\n")

    engine = pyttsx3.init('sapi5')  # Windows
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    # run voice recognition thread
    # it has to be `,` in `(queue,)` to create tuple with one value
    task = threading.Thread(target=get_voice_command, args=())
    task.start()  # start thread
    app.mainloop()  # start GUI thread
