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
from TKCamera import TKCamera
from PIL import Image, ImageTk
import pandas as pd
import textwrap3
from playsound import playsound
import json

DEBUG = True
TEST = True


def increment_click_total():
    app.total_click_commands += 1


def wrap(string, length=50):
    return '\n'.join(textwrap3.wrap(string, length))


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
        r.adjust_for_ambient_noise(source)
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


def exit_program():
    save_user_data()
    threading.Thread(target=speak, args=("exiting V-FIT PT",)).start()
    if app.current_page == "Video":
        clean_video()
    app.destroy()


def get_voice_command() -> None:
    while True:
        query = get_command().lower()
        # exit
        if 'kill the program' in query or 'close the program' in query:
            # save UI data
            save_user_data()
            threading.Thread(target=speak, args=("exiting V-FIT PT",)).start()
            if app.current_page == "Video":
                clean_video()
            # kill voice recognition thread
            # Close the GUI
            app.destroy()
            return

        # GO TO --> PAGE
        elif 'go to' in query:
            if 'welcome page' in query:
                app.total_voice_commands += 1
                app.change_page_to_n(WelcomePage, "Changing to Welcome Page")
            elif 'set up page' in query or 'setup page' in query:
                app.total_voice_commands += 1
                app.change_page_to_n(SetupPage, "Changing to Setup Page")
            elif 'exercise selection' in query:
                app.total_voice_commands += 1
                app.change_page_to_n(
                    ExercisePage, "Changing to Exercise Selection")
            elif 'scoreboard' in query:
                app.total_voice_commands += 1
                app.change_page_to_n(ScoreboardPage, "Changing to Scoreboard")
            elif 'help' in query:
                app.total_voice_commands += 1
                app.change_page_to_n(HelpPage, "Changing to Help Screen")
            elif "tutorial" in query:
                app.total_voice_commands += 1
                app.change_page_to_n(TutorialPage, "Let's start with the tutorial. Click the button.")

        # Go back
        elif 'go back' in query:
            app.total_voice_commands += 1
            # Setup Page
            if app.current_page == "Setup":
                app.change_page_to_n(WelcomePage, "Welcome to V-FIT PT")
            # Exercise Selection
            elif app.current_page == "Exercise":
                app.change_page_to_n(SetupPage, "Setup")
            # Video
            elif app.current_page == "Video":
                app.change_page_to_n(ExercisePage, "Click or say an exercise to begin")
            elif app.current_page == "Help":
                app.change_page_to_n(SetupPage, "Setup")
            elif app.current_page == "Scoreboard":
                app.change_page_to_n(ExercisePage, "Click or say an exercise to begin")
            elif app.current_page == "Tutorial":
                app.change_page_to_n(SetupPage, "Setup")
            elif app.current_page == "Tutorial1":
                app.change_page_to_n(TutorialPage, "Good job! Now try saying go next.")
            elif app.current_page == "Tutorial2":
                app.change_page_to_n(TutorialPage1, "")

        # Go next
        elif 'next' in query:
            app.total_voice_commands += 1
            # Welcome Page
            if app.current_page == "Welcome":
                app.change_page_to_n(SetupPage, "Setup")
            # Setup Page
            elif app.current_page == "Setup":
                app.change_page_to_n(ExercisePage, "Select or say an exercise to begin")
            # Exercise Selection
            elif app.current_page == "Exercise":
                threading.Thread(target=speak, args=("Select or say an exercise to begin",)).start()
            # Video
            elif app.current_page == "Video":
                app.change_page_to_n(ScoreboardPage, "")
            elif app.current_page == "Tutorial":
                app.change_page_to_n(TutorialPage1, "Good job! Now you know how to use voice commands.")
            elif app.current_page == "Tutorial1":
                app.change_page_to_n(TutorialPage2, "Are you ready to get Fit?!")

        # CLICK ON --> BTN
        elif 'click on' in query:
            if 'welcome button' in query and app.current_page == "Welcome":
                app.total_voice_commands += 1
                app.change_page_to_n(SetupPage, "Setup")
            elif 'tutorial button' in query and app.current_page == "Setup":
                app.total_voice_commands += 1
                app.change_page_to_n(TutorialPage, "Let's start with the tutorial. Click the button.")
            elif 'test button' in query and app.current_page == "Tutorial":
                app.change_page_to_n(TutorialPage1,
                                     "Nice job! You clicked the button! Now you can either test the microphone or use "
                                     "voice to go back and next by saying, go back or go next")
            elif 'ready' in query and app.current_page == "Tutorial2":
                app.change_page_to_n(ExercisePage, "Select or say an exercise to begin")
            elif 'test microphone' in query and app.current_page == "Tutorial1":
                TutorialPage1.mic_test("")

        # SETUP Page
        elif app.current_page == "Setup" and "ready" in query:
            app.total_voice_commands += 1
            app.change_page_to_n(ExercisePage, "Select or say an exercise to begin")

        # Start Tutorial form SETUP page
        elif app.current_page == "Setup" and "tutorial" in query:
            app.total_voice_commands += 1
            app.change_page_to_n(TutorialPage, "Let's start with the tutorial. Click the button.")        

        # Microphone Tutorial
        elif app.current_page == "Tutorial1" and "test microphone" in query:
            TutorialPage1.mic_test("")

        # Last page tutorial
        elif app.current_page == "Tutorial2" and "ready" in query:
            app.change_page_to_n(ExercisePage, "Select or say an exercise to begin")

        # WELCOME Page
        elif app.current_page == "Welcome" and "let's begin" in query:
            app.total_voice_commands += 1
            app.change_page_to_n(SetupPage, "Setup")

        # Exercise Page
        elif app.current_page == "Exercise":
            # exercise selection
            if 'bicep curls' in query:
                app.total_voice_commands += 1
                threading.Thread(target=speak, args=("Let's do some curls!",)).start()
                app.frames[ExercisePage].select_exercise('bicep_curls')
            elif 'lunges' in query:
                app.total_voice_commands += 1
                threading.Thread(target=speak, args=("Here we go!",)).start()
                app.frames[ExercisePage].select_exercise('lunges')
            elif 'squats' in query:
                app.total_voice_commands += 1
                threading.Thread(target=speak, args=("Let's go!",)).start()
                app.frames[ExercisePage].select_exercise('squats')
            elif 'jumping jacks' in query:
                app.total_voice_commands += 1
                threading.Thread(target=speak, args=("Let's get to it!",)).start()
                app.frames[ExercisePage].select_exercise('jumping_jacks')
        # Video Page
        elif app.current_page == "Video":
            if 'exit' in query or "another exercise" in query:
                app.total_voice_commands += 1
                app.change_page_to_n(
                    ExercisePage, 'Pick or say an exercise to begin!')
        # Ignore empty prompts
        elif "" == query:
            pass
        # Inform user
        else:
            pass


def clean_video():
    # garbage collection
    for widget in app.frames[VideoPage].stream_widgets:
        widget.vid.running = False
        widget.vid.__del__()
        widget.destroy()

    app.frames[VideoPage].stream_widgets.clear()


def write_data(filepath, data: str):
    """
    Appends data to file, assumes file exists
    :param filepath: filepath
    :param data: data to be written
    :return: void
    """
    with open(filepath, 'a') as file:
        file.write(data)
        file.write('\n')


def save_user_data():
    """
    Save user data from UI interactions
    :return: void
    """

    write_data(app.filepath, "Voice_Total " + str(app.total_voice_commands))
    write_data(app.filepath, "Mouse_Total " + str(app.total_click_commands))


def get_score_load_scoreboard(self):
    data_exercise = self.stream_widgets[0].vid.get_data()
    final_score = data_exercise[4]
    exercise = data_exercise[5]
    scoreboard_directory = "data/leaderboard_data.txt"

    with open(scoreboard_directory, "r+") as template_file:
        score_dict = json.loads(template_file.readline())
        for index, score in enumerate(score_dict[exercise]):
            if final_score >= score:
                score_dict[exercise].insert(index, final_score)
                score_dict[exercise] = score_dict[exercise][0:10]
                break
        template_file.seek(0)
        template_file.write(json.dumps(score_dict))
    app.frames[ScoreboardPage].update_leaderboard()
    app.change_page_to_n(ScoreboardPage, "")


class VFITApp(ThemedTk):
    current_page = ""
    previous_page = ""
    selected_exercise = "bicep_curls"
    volume = 50
    voice_thread = None

    prev_state = "None"
    prev_counter = 0
    prev_feedback = "None"
    dummy_var = [None, 0, None, 1, 0]

    exercise_start_time = None
    src_filepath = None

    # User Data
    negative_feedback_count = 0
    total_voice_commands = 0
    total_click_commands = 0
    squat_completion_time = None
    bicep_curl_completion_time = None
    jumping_jack_completion_time = None
    lunge_completion_time = None

    def play_sound(self):
        playsound(os.path.dirname(__file__) + "/sounds/ding.wav", block=False)
        return

    def gamification_data(self, data):
        if data[0:5] != app.dummy_var:
            if data[1] != app.prev_counter:
                sound_process = threading.Thread(target=self.play_sound())
                sound_process.start()
                if data[1] == 0:
                    app.prev_counter = data[1]
                elif data[1] % 15 == 0:
                    if TEST:
                        if app.selected_exercise == 'bicep_curls':
                            app.bicep_curl_completion_time = datetime.datetime.now() - app.exercise_start_time
                            write_data(app.filepath,
                                       "BicepCurls_Completion_Time " + str(app.bicep_curl_completion_time))
                            write_data(app.filepath, "BicepCurls_Negative_Feedback " + str(app.negative_feedback_count))
                        elif app.selected_exercise == 'jumping_jacks':
                            app.jumping_jack_completion_time = datetime.datetime.now() - app.exercise_start_time
                            write_data(app.filepath,
                                       "JumpingJacks_Completion_time " + str(app.jumping_jack_completion_time))
                            write_data(app.filepath,
                                       "JumpingJacks_Negative_Feedback " + str(app.negative_feedback_count))
                        elif app.selected_exercise == 'squats':
                            app.squat_completion_time = datetime.datetime.now() - app.exercise_start_time
                            write_data(app.filepath, "Squats_Completion_Time " + str(app.squat_completion_time))
                            write_data(app.filepath, "Squats_Negative_Feedback " + str(app.negative_feedback_count))
                        elif app.selected_exercise == 'lunges':
                            app.lunge_completion_time = datetime.datetime.now() - app.exercise_start_time
                            write_data(app.filepath, "Lunges_Completion_Time " + str(app.lunge_completion_time))
                            write_data(app.filepath, "Lunges_Negative_Feedback " + str(app.negative_feedback_count))

                    text = (
                        "Nice job. You're all done with set {}! You may now return to the exercise menu, "
                        "or do another set.").format(
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
                    if TEST:
                        # increment feedback counter
                        app.negative_feedback_count += 1
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

        scoreboard_directory = "data/leaderboard_data.txt"
        # creates an empty Data folder should one not exist
        os.makedirs(os.path.dirname("./data/"), exist_ok=True)
        if not os.path.isfile(scoreboard_directory):
            with open(scoreboard_directory, "w") as template_file:
                template_file.write(json.dumps(
                    {"bicep_curls": [0] * 10, "squats": [0] * 10, "lunges": [0] * 10, "jumping_jacks": [0] * 10}))

        welcome_frame = WelcomePage(container, self)
        introduction_frame = HelpPage(container, self)
        setup_frame = SetupPage(container, self)
        exercise_frame = ExercisePage(container, self)
        video_frame = VideoPage(container, self)
        scoreboard_frame = ScoreboardPage(container, self)
        tutorial_frame = TutorialPage(container, self)
        tutorial1_frame = TutorialPage1(container, self)
        tutorial2_frame = TutorialPage2(container, self)

        self.frames[WelcomePage] = welcome_frame
        self.frames[HelpPage] = introduction_frame
        self.frames[SetupPage] = setup_frame
        self.frames[ExercisePage] = exercise_frame
        self.frames[VideoPage] = video_frame
        self.frames[ScoreboardPage] = scoreboard_frame
        self.frames[TutorialPage] = tutorial_frame
        self.frames[TutorialPage1] = tutorial1_frame
        self.frames[TutorialPage2] = tutorial2_frame

        setup_frame.grid(row=0, column=0, sticky="nsew")
        welcome_frame.grid(row=0, column=0, sticky="nsew")
        introduction_frame.grid(row=0, column=0, sticky="nsew")
        exercise_frame.grid(row=0, column=0, sticky="nsew")
        video_frame.grid(row=0, column=0, sticky="nsew")
        scoreboard_frame.grid(row=0, column=0, sticky="nsew")
        tutorial_frame.grid(row=0, column=0, sticky="nsew")
        tutorial1_frame.grid(row=0, column=0, sticky="nsew")
        tutorial2_frame.grid(row=0, column=0, sticky="nsew")

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
        threading.Thread(target=speak, args=(msg,)).start()


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
                                command=lambda: [app.change_page_to_n(SetupPage, ""), increment_click_total()],
                                highlightthickness=0, bd=0, bg="white", activebackground='white')
        welcome_btn.image = welcome_image
        welcome_btn.place(relx=.5, rely=.5, anchor='center',
                          relheight=1, relwidth=1)
        
        welcome_heading = tk.Label(self, text="Click Anywhere or Say 'Lets begin!' to start.")
        welcome_heading.config(
            font=("Helvetica", 24), bd=0, bg="white", activebackground='white', foreground="#223063")
        welcome_heading.place(relx=0.5, rely=0.8, anchor="center")


class HelpPage(tk.Frame):
    name = "Help"

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg='white')

        back_btn_image = ImageTk.PhotoImage(Image.open("ui_elements/back_btn.png").convert(mode="RGBA").resize(
            (self.winfo_screenheight() // 15, self.winfo_screenheight() // 15)))
        back_btn = tk.Button(self, image=back_btn_image,
                             command=lambda: app.change_page_to_n(SetupPage, ""),
                             highlightthickness=0, bd=0, bg="white", activebackground='white')
        back_btn.image = back_btn_image
        back_btn.place(relx=((self.winfo_screenwidth() // 20) / self.winfo_screenwidth() * 9 / 16),
                       rely=(1 - (self.winfo_screenheight() // 20) / self.winfo_screenheight()), anchor='center')
        voice_commands_list = tk.Label(self, text="Supported Voice Commands")
        voice_commands_list.config(
            font=("Helvetica", 24), bd=0, bg="white", activebackground='white', foreground="#223063")
        voice_commands_list.place(relx=0.5, rely=0.05, anchor="center")

        df = pd.read_excel("excelfiles/commands.xlsx")

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


class ScoreboardPage(tk.Frame):
    name = "Scoreboard"

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg='white')

        back_btn_image = ImageTk.PhotoImage(Image.open("ui_elements/back_btn.png").convert(mode="RGBA").resize(
            (self.winfo_screenheight() // 15, self.winfo_screenheight() // 15)))
        back_btn = tk.Button(self, image=back_btn_image,
                             command=lambda: [app.change_page_to_n(ExercisePage, ""), increment_click_total()],
                             highlightthickness=0, bd=0, bg="white", activebackground='white')
        back_btn.image = back_btn_image
        back_btn.place(relx=((self.winfo_screenwidth() // 20) / self.winfo_screenwidth() * 9 / 16),
                       rely=(1 - (self.winfo_screenheight() // 20) / self.winfo_screenheight()), anchor='center')
        scoreboard_heading = tk.Label(self, text="Exercise High Scores")
        scoreboard_heading.config(
            font=("Helvetica", 24), bd=0, bg="white", activebackground='white', foreground="#223063")
        scoreboard_heading.place(relx=0.5, rely=0.05, anchor="center")

        scoreboard_directory = "data/leaderboard_data.txt"

        with open(scoreboard_directory, "r+") as template_file:
            score_dict = json.loads(template_file.readline())

        temp_data = []
        for index, value in enumerate(score_dict["bicep_curls"]):
            temp_arr = []
            for key in list(score_dict.keys()):
                temp_arr.append(str(score_dict[key][index]))
            temp_data.append([str(index + 1)] + temp_arr)
            # print([index + 1] + score_dict[key][index] for key in list(score_dict.keys()))
            # temp_data.append([index + 1] + score_dict[key][index] for key in score_dict.keys())
        df_score = pd.DataFrame(temp_data, columns=['Position', "Bicep Curls", "Squats", "Lunges", "Jumping Jacks"])

        tree = ttk.Treeview(self)
        tree['show'] = 'headings'
        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview",
                        font=("Helvetica", 16),
                        rowheight=64,
                        background="#223063",
                        foreground="white",
                        fieldbackground="#223063")

        style.map("Treeview", background=[('selected', 'grey')])
        tree["columns"] = list(df_score.columns)

        style.configure('Treeview.Heading',
                        background="white",
                        foreground="#223063",
                        font=("Helvetica", 16),
                        rowheight=64,
                        fieldbackground="white")
        # Add column headings
        for col in df_score.columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center')

        # Add rows to the table
        for i, row in df_score.iterrows():
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

        exit_btn_image = ImageTk.PhotoImage(Image.open("ui_elements/exit_btn.png").convert(mode="RGBA").resize(
            (self.winfo_screenheight() // 15, self.winfo_screenheight() // 15)))
        exit_btn = tk.Button(self, image=exit_btn_image,
                             command=lambda: [increment_click_total(), exit_program()],
                             font=("Helvetica", 10), highlightthickness=0, bd=0, bg="white", activebackground='white')
        exit_btn.image = exit_btn_image
        exit_btn.place(relx=(1 - (self.winfo_screenwidth() // 20) / self.winfo_screenwidth() * 9 / 16),
                       rely=(1 - (self.winfo_screenheight() // 20) / self.winfo_screenheight()), anchor='center')

    def update_leaderboard(self):
        scoreboard_directory = "data/leaderboard_data.txt"
        with open(scoreboard_directory, "r+") as template_file:
            score_dict = json.loads(template_file.readline())

        temp_data = []
        for index, value in enumerate(score_dict["bicep_curls"]):
            temp_arr = []
            for key in list(score_dict.keys()):
                temp_arr.append(str(score_dict[key][index]))
            temp_data.append([str(index + 1)] + temp_arr)
        df_score = pd.DataFrame(temp_data, columns=['Position', "Bicep Curls", "Squats", "Lunges", "Jumping Jacks"])

        tree = ttk.Treeview(self)
        tree['show'] = 'headings'
        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview",
                        font=("Helvetica", 16),
                        rowheight=64,
                        background="#223063",
                        foreground="white",
                        fieldbackground="#223063")

        style.map("Treeview", background=[('selected', 'grey')])
        tree["columns"] = list(df_score.columns)

        style.configure('Treeview.Heading',
                        background="white",
                        foreground="#223063",
                        font=("Helvetica", 16),
                        rowheight=64,
                        fieldbackground="white")
        # Add column headings
        for col in df_score.columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center')

        # Add rows to the table
        for i, row in df_score.iterrows():
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


class SetupPage(tk.Frame):
    name = "Setup"

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='white')

        # WelcomeButton
        back_btn_image = ImageTk.PhotoImage(Image.open("ui_elements/back_btn.png").convert(mode="RGBA").resize(
            (self.winfo_screenheight() // 15, self.winfo_screenheight() // 15)))
        back_btn = tk.Button(self, image=back_btn_image,
                             command=lambda: [app.change_page_to_n(WelcomePage, ""), increment_click_total()],
                             font=("Helvetica", 10), highlightthickness=0, bd=0, bg="white", activebackground='white')
        back_btn.image = back_btn_image
        back_btn.place(relx=((self.winfo_screenwidth() // 20) / self.winfo_screenwidth() * 9 / 16),
                       rely=(1 - (self.winfo_screenheight() // 20) / self.winfo_screenheight()), anchor='center')

        help_btn_image = ImageTk.PhotoImage(Image.open("ui_elements/help_btn.png").convert(mode="RGBA").resize(
            (self.winfo_screenheight() // 15, self.winfo_screenheight() // 15)))
        help_btn = tk.Button(self, image=help_btn_image,
                             command=lambda: [app.change_page_to_n(HelpPage, ""), increment_click_total()],
                             font=("Helvetica", 10), highlightthickness=0, bd=0, bg="white", activebackground='white')
        help_btn.image = help_btn_image
        help_btn.place(relx=(1 - (self.winfo_screenwidth() // 20) / self.winfo_screenwidth() * 9 / 16),
                       rely=((self.winfo_screenheight() // 20) / self.winfo_screenheight()), anchor='center')

        pygame.mixer.init()

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
            # set TTS volume
            engine.setProperty("volume", volume_slider.get() / 100.0)
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
                                    command=lambda: [volume_slider.set(0), increment_click_total()],
                                    highlightthickness=0, bd=0, bg="white", activebackground='white')
        volume_zero_btn.image = vol_down_image
        volume_zero_btn.place(relx=0.25, rely=0.5,
                              anchor='center')
        volume_zero_btn.configure(bg='white', fg='white')

        vol_up_image = ImageTk.PhotoImage(Image.open("ui_elements/volume_full.png").convert(mode="RGBA").resize(
            (self.winfo_screenheight() // 15, self.winfo_screenheight() // 15)))
        volume_full_btn = tk.Button(self, image=vol_up_image,
                                    command=lambda: [volume_slider.set(100), increment_click_total()],
                                    highlightthickness=0, bd=0, bg="white", activebackground='white')
        volume_full_btn.image = vol_up_image
        volume_full_btn.place(relx=0.75, rely=0.5, anchor='center')
        volume_full_btn.configure(bg='white', fg='white')

        text = tk.Label(self, text="System Volume")
        text.config(font=("Helvetica", 16), bd=0, bg="white", activebackground='white', foreground="#223063")
        text.place(relx=0.5, rely=0.55, anchor='center')

        tutorial_image = ImageTk.PhotoImage(Image.open("ui_elements/tutorial_btn.png").convert(mode="RGBA").resize(
            (self.winfo_screenheight() // 10, self.winfo_screenheight() // 10)))
        tutorial_btn = tk.Button(self, text="Click here for a tutorial! \n or \n Say 'Start Tutorial'",
                                 image=tutorial_image, compound='top',
                                 command=lambda: app.change_page_to_n(TutorialPage,
                                                                      "Let's start with the tutorial. Click the button."),
                                 font=("Helvetica", 16),
                                 highlightthickness=0, bd=0,
                                 bg="white", activebackground='white', foreground="#223063")
        tutorial_btn.image = tutorial_image
        tutorial_btn.place(relx=.5, rely=0.75, anchor='center')

        next_btn_image = ImageTk.PhotoImage(Image.open("ui_elements/next_btn.png").convert(mode="RGBA").resize(
            (self.winfo_screenheight() // 15, self.winfo_screenheight() // 15)))
        next_btn = tk.Button(self, image=next_btn_image,
                             command=lambda: [app.change_page_to_n(ExercisePage, ""), increment_click_total()],
                             font=("Helvetica", 10), highlightthickness=0, bd=0, bg="white", activebackground='white')
        next_btn.image = next_btn_image
        next_btn.place(relx=(1 - (self.winfo_screenwidth() // 20) / self.winfo_screenwidth() * 9 / 16),
                       rely=(1 - (self.winfo_screenheight() // 20) / self.winfo_screenheight()), anchor='center')

        # Tutorial Page


class TutorialPage(tk.Frame):
    name = "Tutorial"

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='white')

        # WelcomeButton
        back_btn_image = ImageTk.PhotoImage(Image.open("ui_elements/back_btn.png").convert(mode="RGBA").resize(
            (self.winfo_screenheight() // 15, self.winfo_screenheight() // 15)))
        back_btn = tk.Button(self, image=back_btn_image,
                             command=lambda: app.change_page_to_n(SetupPage, ""),
                             font=("Helvetica", 10), highlightthickness=0, bd=0, bg="white", activebackground='white')
        back_btn.image = back_btn_image
        back_btn.place(relx=((self.winfo_screenwidth() // 20) / self.winfo_screenwidth() * 9 / 16),
                       rely=(1 - (self.winfo_screenheight() // 20) / self.winfo_screenheight()), anchor='center')

        print_text = tk.Label(self, text="Try saying 'Click on test button'")
        print_text.config(
            font=("Helvetica", 24), bd=0, bg="white", activebackground='white', foreground="#223063")
        print_text.place(relx=0.5, rely=0.25, anchor="center")

        test_image = ImageTk.PhotoImage(Image.open("ui_elements/test_btn.png").convert(mode="RGBA").resize(
            (self.winfo_screenheight() // 5, self.winfo_screenheight() // 5)))
        test_btn = tk.Button(self, text="Test button!", image=test_image, compound='top',
                             command=lambda: app.change_page_to_n(TutorialPage1,
                                                                  "Nice job! You clicked the button! Now you can "
                                                                  "either test the microphone or use voice to go "
                                                                  "back and next by saying, go back or go next"),
                             font=("Helvetica", 16),
                             highlightthickness=0, bd=0,
                             bg="white", activebackground='white', foreground="#223063")
        test_btn.image = test_image
        test_btn.place(relx=.5, rely=0.5, anchor='center')

        next_btn_image = ImageTk.PhotoImage(Image.open("ui_elements/next_btn.png").convert(mode="RGBA").resize(
            (self.winfo_screenheight() // 15, self.winfo_screenheight() // 15)))
        next_btn = tk.Button(self, image=next_btn_image,
                             command=lambda: app.change_page_to_n(TutorialPage1,
                                                                  "Now you can either test the microphone or use "
                                                                  "voice to go back and next"),
                             font=("Helvetica", 10), highlightthickness=0, bd=0, bg="white", activebackground='white')
        next_btn.image = next_btn_image
        next_btn.place(relx=(1 - (self.winfo_screenwidth() // 20) / self.winfo_screenwidth() * 9 / 16),
                       rely=(1 - (self.winfo_screenheight() // 20) / self.winfo_screenheight()), anchor='center')


class TutorialPage1(tk.Frame):
    name = "Tutorial1"

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='white')

        # WelcomeButton
        back_btn_image = ImageTk.PhotoImage(Image.open("ui_elements/back_btn.png").convert(mode="RGBA").resize(
            (self.winfo_screenheight() // 15, self.winfo_screenheight() // 15)))
        back_btn = tk.Button(self, image=back_btn_image,
                             command=lambda: app.change_page_to_n(TutorialPage, ""),
                             font=("Helvetica", 10), highlightthickness=0, bd=0, bg="white", activebackground='white')
        back_btn.image = back_btn_image
        back_btn.place(relx=((self.winfo_screenwidth() // 20) / self.winfo_screenwidth() * 9 / 16),
                       rely=(1 - (self.winfo_screenheight() // 20) / self.winfo_screenheight()), anchor='center')

        print_text = tk.Label(self, text="Try saying 'Test Microphone' or Clicking on the button")
        print_text.config(
            font=("Helvetica", 24), bd=0, bg="white", activebackground='white', foreground="#223063")
        print_text.place(relx=0.5, rely=0.25, anchor="center")

        mic_image = ImageTk.PhotoImage(Image.open("ui_elements/mic_test.png").convert(mode="RGBA").resize(
            (self.winfo_screenheight() // 5, self.winfo_screenheight() // 5)))
        mic_rec_btn = tk.Button(self, text="Test Microphone!", image=mic_image, compound='top',
                                command=lambda: (self.mic_test(), ""),
                                font=("Helvetica", 16),
                                highlightthickness=0, bd=0,
                                bg="white", activebackground='white', foreground="#223063")
        mic_rec_btn.image = mic_image
        mic_rec_btn.place(relx=.5, rely=0.5, anchor='center')

        next_btn_image = ImageTk.PhotoImage(Image.open("ui_elements/next_btn.png").convert(mode="RGBA").resize(
            (self.winfo_screenheight() // 15, self.winfo_screenheight() // 15)))
        next_btn = tk.Button(self, image=next_btn_image,
                             command=lambda: app.change_page_to_n(TutorialPage2, "Are you ready to get Fit?!"),
                             font=("Helvetica", 10), highlightthickness=0, bd=0, bg="white", activebackground='white')
        next_btn.image = next_btn_image
        next_btn.place(relx=(1 - (self.winfo_screenwidth() // 20) / self.winfo_screenwidth() * 9 / 16),
                       rely=(1 - (self.winfo_screenheight() // 20) / self.winfo_screenheight()), anchor='center')

    def mic_test(self):
        """
        Functional call for Mic Test Button, calls voice recognition function
        :return: void
        """
        speak("Say something, and i'll repeat it back!")
        speak("You said " + get_command())


class TutorialPage2(tk.Frame):
    name = "Tutorial2"

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='white')

        # WelcomeButton
        back_btn_image = ImageTk.PhotoImage(Image.open("ui_elements/back_btn.png").convert(mode="RGBA").resize(
            (self.winfo_screenheight() // 15, self.winfo_screenheight() // 15)))
        back_btn = tk.Button(self, image=back_btn_image,
                             command=lambda: app.change_page_to_n(TutorialPage1, ""),
                             font=("Helvetica", 10), highlightthickness=0, bd=0, bg="white", activebackground='white')
        back_btn.image = back_btn_image
        back_btn.place(relx=((self.winfo_screenwidth() // 20) / self.winfo_screenwidth() * 9 / 16),
                       rely=(1 - (self.winfo_screenheight() // 20) / self.winfo_screenheight()), anchor='center')

        ready_image = ImageTk.PhotoImage(Image.open("ui_elements/start_btn.png").convert(mode="RGBA").resize(
            (self.winfo_screenheight() // 5, self.winfo_screenheight() // 5)))
        ready_btn = tk.Button(self, text="I'm Ready!", image=ready_image, compound='top',
                              command=lambda: app.change_page_to_n(ExercisePage, ""),
                              font=("Helvetica", 16),
                              highlightthickness=0, bd=0,
                              bg="white", activebackground='white', foreground="#223063")
        ready_btn.image = ready_image
        ready_btn.place(relx=.5, rely=0.5, anchor='center')

        next_btn_image = ImageTk.PhotoImage(Image.open("ui_elements/next_btn.png").convert(mode="RGBA").resize(
            (self.winfo_screenheight() // 15, self.winfo_screenheight() // 15)))
        next_btn = tk.Button(self, image=next_btn_image,
                             command=lambda: app.change_page_to_n(ExercisePage, ""),
                             font=("Helvetica", 10), highlightthickness=0, bd=0, bg="white", activebackground='white')
        next_btn.image = next_btn_image
        next_btn.place(relx=(1 - (self.winfo_screenwidth() // 20) / self.winfo_screenwidth() * 9 / 16),
                       rely=(1 - (self.winfo_screenheight() // 20) / self.winfo_screenheight()), anchor='center')


class ExercisePage(tk.Frame):
    name = "Exercise"

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='white')

        back_btn_image = ImageTk.PhotoImage(Image.open("ui_elements/back_btn.png").convert(mode="RGBA").resize(
            (self.winfo_screenheight() // 15, self.winfo_screenheight() // 15)))
        back_btn = tk.Button(self, image=back_btn_image,
                             command=lambda: [app.change_page_to_n(SetupPage, ""), increment_click_total()],
                             font=("Helvetica", 10), highlightthickness=0, bd=0, bg="white", activebackground='white')
        back_btn.image = back_btn_image
        back_btn.place(relx=((self.winfo_screenwidth() // 20) / self.winfo_screenwidth() * 9 / 16),
                       rely=(1 - (self.winfo_screenheight() // 20) / self.winfo_screenheight()), anchor='center')

        image = Image.open("exercises/curls.png")
        temp_image = image.resize(
            (self.winfo_screenwidth() // 5, int(self.winfo_screenwidth() // 5) * 16 // 9))
        bicep_image = ImageTk.PhotoImage(temp_image)
        bicep_btn = tk.Button(self, image=bicep_image, compound="top",
                              command=lambda: [self.select_exercise("bicep_curls"), increment_click_total()],
                              highlightthickness=0, bd=0, bg="white", activebackground='white')
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
                              command=lambda: [self.select_exercise("lunges"), increment_click_total()],
                              font=("Helvetica", 40), highlightthickness=0, bd=0, bg="white", activebackground='white')
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
                              command=lambda: [self.select_exercise("squats"), increment_click_total()],
                              font=("Helvetica", 40), highlightthickness=0, bd=0, bg="white", activebackground='white')
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
                                command=lambda: [self.select_exercise("jumping_jacks"), increment_click_total()],
                                font=("Helvetica", 40), highlightthickness=0, bd=0, bg="white",
                                activebackground='white')
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
            # reset feedback_counter
            app.negative_feedback_count = 0
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

        if DEBUG:
            print("updating to", app.selected_exercise)
        for number, (source, exercise_type) in enumerate(self.get_sources(app.selected_exercise)):
            widget = TKCamera(self, source, self.width,
                              self.height, exercise_type=exercise_type)
            widget.set_app(app)
            widget.grid(row=0, column=number)
            self.stream_widgets.append(widget)

            back_btn_image = ImageTk.PhotoImage(Image.open("ui_elements/back_btn.png").convert(mode="RGBA").resize(
                (self.winfo_screenheight() // 15, self.winfo_screenheight() // 15)))
            back_btn = tk.Button(self, image=back_btn_image,
                                 command=lambda: [app.change_page_to_n(ExercisePage, ""), increment_click_total()],
                                 font=("Helvetica", 10), highlightthickness=0, bd=0, bg="white",
                                 activebackground='white')
            back_btn.image = back_btn_image
            back_btn.place(relx=((self.winfo_screenwidth() // 20) / self.winfo_screenwidth() * 9 / 16),
                           rely=(1 - (self.winfo_screenheight() // 20) / self.winfo_screenheight()), anchor='center')

            scoreboard_btn_image = ImageTk.PhotoImage(
                Image.open("ui_elements/scoreboard_btn.png").convert(mode="RGBA").resize(
                    (self.winfo_screenheight() // 15, self.winfo_screenheight() // 15)))
            scoreboard_btn = tk.Button(self, image=scoreboard_btn_image,
                                       command=lambda: [get_score_load_scoreboard(self), increment_click_total()],
                                       font=("Helvetica", 10), highlightthickness=0, bd=0, bg="white",
                                       activebackground='white')
            scoreboard_btn.image = scoreboard_btn_image
            scoreboard_btn.place(relx=(1 - (self.winfo_screenwidth() // 20) / self.winfo_screenwidth() * 9 / 16),
                                 rely=(1 - (self.winfo_screenheight() // 20) / self.winfo_screenheight()),
                                 anchor='center')

    def get_sources(self, exercise):
        """
        Formats source file for video player
        :param exercise: name of exercise
        :return: source dict in proper format
        """
        sources = [
            (0, str(exercise)),
            ("./exercises/" + str(exercise) + ".mp4", "None")
        ]
        return sources


if __name__ == "__main__":
    # initialize TTS
    engine = pyttsx3.init('sapi5')  # Windows
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    # initialize app
    app = VFITApp()

    # Data Collection
    if TEST:
        # Data collection metrics file location
        src_filepath = "./data/"
        ct = datetime.datetime.now()
        id_num = ct.strftime("%y%m%d%H%M")
        filename = id_num + '.txt'
        app.filepath = src_filepath + filename
        os.makedirs(os.path.dirname(app.filepath), exist_ok=True)
        with open(app.filepath, "w") as f:
            f.write(ct.strftime("%m/%d/%y") + '\n')
            f.write("Data Begins Below\n")
    engine.setProperty("volume", 0.5)
    threading.Thread(target=speak, args=("Welcome to V-FIT PT",)).start()
    # run voice recognition thread
    app.voice_thread = threading.Thread(target=get_voice_command, args=())
    app.voice_thread.start()  # start thread
    app.mainloop()  # start GUI thread
