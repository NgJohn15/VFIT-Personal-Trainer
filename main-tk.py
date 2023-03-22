import os
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser

import threading
import queue
import tkinter as tk
from tkinter import ttk
from tkinter import * 
from tkinter.ttk import *
from tkinter import filedialog
import os


LARGEFONT =("Verdana", 35)

# --- functions ---

# def speak(text):
#     engine.say(text)
#     engine.runAndWait()

# def wishme(queue):
#     hour = datetime.datetime.now().hour
#
#     if 0 <= hour < 12:
#         text = "Good Morning sir"
#     elif 12 <= hour < 18:
#         text = "Good Afternoon sir"
#     else:
#         text = "Good Evening sir"
#
#     queue.put(f'{text}.')
#     speak(text)
#
#     queue.put("I am Genos. How can I Serve you?\n")
#     speak("I am Genos. How can I Serve you?")


# def takecommand():
#     # it takes mic input from the user and return string output
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         r.pause_threshold = 1
#         audio = r.listen(source)
#
#     try:
#         print("Recognizing..")
#         query = r.recognize_google(audio, language='en-in')
#         print(f"user Said :{query}\n")
#
#     except Exception as e:
#         print(e)
#
#         speak("Say that again please")
#         return "None"
#
#     return query


# def my_loop(queue):
#     wishme(queue)
#
#     while True:
#         query = takecommand().lower()
#
#         # Logic for executing task based query
#         if 'wikipedia' in query:
#             queue.put('searching Wikipedia....')
#             speak('searching Wikipedia....')
#
#             query = query.replace("wikipedia", "")
#             results = wikipedia.summary(query, sentences=5)
#
#             queue.put("According to wikipedia" + str(results))
#
#             speak("According to wikipedia")
#             print(results)
#             speak(results)
#
#         elif 'button' == query:
#             btn_press(queue)
#
#         elif 'open youtube' in query:
#             queue.put("opening youtube.com")
#             webbrowser.open("youtube.com")
#
#         elif 'open google' in query:
#             queue.put("opening google.com")
#             webbrowser.open("google.com")
#
#         elif 'open stackoverflow' in query:
#             queue.put("opening stackoverflow.com")
#             webbrowser.open("stackoverflow.com")
#
#         elif 'open mailbox' in query:
#             webbrowser.open("gmail.com");
#
#
#         elif 'play music' in query:
#             music_dir = 'D:\\SAHIL\\$ONGS_MJ'
#             songs = os.listdir(music_dir)
#
#             queue.put(f"playing music {songs[0]}")
#
#             print(songs)
#             os.startfile(os.path.join(music_dir, songs[0]))
#
#         elif 'the time' in query:
#             strTime = datetime.datetime.now().strftime("%H:%M:%S")
#
#             speak(f"Sir the time is {strTime}", queue)
#
#         elif 'how are you' in query:
#             queue.put("I am fine sir. How are you?")
#             speak("I am fine sir. How are you?")
#
#         elif 'i am fine' in query:
#             queue.put("that's good to know, how can I help you")
#             speak("that's good to know, how can I help you")
#
#         elif 'goodbye' in query:
#             queue.put("bye Sir")
#             speak("bye Sir")
#             queue.put("\quit")
#             break # exit loop and thread will end
#             #exit()

# def update_text():
#     if not queue.empty():
#         text = queue.get()
#         if text == '\quit':
#             root.destroy() # close window and stop `root.mainloop()`
#             return # don't run `after` again
#         else:
#             t.insert('end', text)
#
#     root.after(200, update_text)
# def btn_press(queue):
#     controller.show_frame(WelcomePage)



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
        excercise_frame = ExcercisePage(container, self)
        video_frame = VideoPage(container, self)

        self.frames[WelcomePage] = welcome_frame
        self.frames[SetupPage] = setup_frame
        self.frames[ExcercisePage] = excercise_frame
        self.frames[VideoPage] = video_frame

        setup_frame.grid(row=0, column=0, sticky="nsew")
        welcome_frame.grid(row=0, column=0, sticky="nsew")
        excercise_frame.grid(row=0, column=0, sticky="nsew")
        video_frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(WelcomePage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class WelcomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # WelcomeButton
        welcomebtn = ttk.Button(self, text="Welcome", command=lambda: controller.show_frame(SetupPage))
        # label = ttk.Label(self, text="Startpage", font=LARGEFONT)
        welcomebtn.place(relx=.5, rely=.5, anchor='center', relheight=0.5, relwidth=0.5)


class SetupPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # WelcomeButton
        setupbtn = ttk.Button(self, text="Mic Test")
        # label = ttk.Label(self, text="Startpage", font=LARGEFONT)
        setupbtn.place(relx=.3, rely=.15, anchor='center', relheight=0.2, relwidth=0.3)
        
        micrecbtn = ttk.Button(self, text="Mic Recognition")
        # label = ttk.Label(self, text="Startpage", font=LARGEFONT)
        micrecbtn.place(relx=.7, rely=.15, anchor='center', relheight=0.2, relwidth=0.3)
        slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient='horizontal', 
        )
        text=Label(self, text = "Audio")
        text.config(font =("Courier", 14))
        text.place(relx=.2, rely=.5, anchor='center', relheight=0.1, relwidth=0.1)
        slider.get()
        slider.place(relx=.6, rely=.5, anchor='center', relheight=0.2, relwidth=0.5)
        readybtn = ttk.Button(self, text="Ready !", command=lambda: controller.show_frame(ExcercisePage))
        # label = ttk.Label(self, text="Startpage", font=LARGEFONT)
        readybtn.place(relx=.5, rely=.75, anchor='center', relheight=0.2, relwidth=0.4)

       
class ExcercisePage(tk.Frame):
    
    def __init__(self, parent, controller):
        bicep = tk.PhotoImage(file='bicep-clipart-11.png')
        tk.Frame.__init__(self, parent)
        bicepbtn = ttk.Button(self, text="Bicep", command=lambda: controller.show_frame(VideoPage))
        # label = ttk.Label(self, text="Startpage", font=LARGEFONT)
        bicepbtn.place(relx=0.2, rely=0.5, anchor='center', relheight=0.75, relwidth=0.15)
        
        lungebtn = ttk.Button(self, text="Lunge", command=lambda: controller.show_frame(VideoPage))
        # label = ttk.Label(self, text="Startpage", font=LARGEFONT)
        lungebtn.place(relx=0.4, rely=0.5, anchor='center', relheight=0.75, relwidth=0.15)
        
        squatbtn = ttk.Button(self, text="Squat", command=lambda: controller.show_frame(VideoPage))
        # label = ttk.Label(self, text="Startpage", font=LARGEFONT)
        squatbtn.place(relx=0.6, rely=0.5, anchor='center', relheight=0.75, relwidth=0.15)
        
        jumpingbtn = ttk.Button(self, text="Jumping", command=lambda: controller.show_frame(VideoPage))
        # label = ttk.Label(self, text="Startpage", font=LARGEFONT)
        jumpingbtn.place(relx=0.8, rely=0.5, anchor='center', relheight=0.75, relwidth=0.15)
        
class VideoPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # insert video feed and ref video
        
        
        


if __name__ == "__main__":
    
    app = VFITApp()
    app.mainloop()

# if __name__ == "__main__":
#
#     engine = pyttsx3.init('sapi5') # Windows
#     voices = engine.getProperty('voices')
#     engine.setProperty('voice', voices[0].id)
#
#     # ---
#
#     root = tk.Tk()
#     queue = queue.Queue()
#
#     t = tk.Text()
#     t.pack()
#
#     button = tk.Button(root, text='button', command=btn_press(queue))
#     button.pack()
#
#     update_text()
#
#     task = threading.Thread(target=my_loop, args=(queue,)) # it has to be `,` in `(queue,)` to create tuple with one value
#     task.start() # start thread
#
#     root.mainloop()
#     task.join() # wait for end of thread