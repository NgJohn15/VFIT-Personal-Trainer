#!/usr/bin/env python

# author: Bartlomiej "furas" Burek (https://blog.furas.pl)
# date: 2021.01.26

import PIL.ImageTk
import tkinter
import tkinter.filedialog
from videocapture import VideoCapture


"""TODO: add docstring"""

class tkCamera(tkinter.Frame):

    def __init__(self, parent, text="", source=0, width=None, height=None, sources=None, exercise_type = None):
        """TODO: add docstring"""

        super().__init__(parent)

        self.source = source
        self.width  = width
        self.height = height
        self.other_sources = sources
        self.exercise_type = exercise_type

        #self.window.title(window_title)
        self.vid = VideoCapture(self.source, self.width, self.height,exercise_type = self.exercise_type)


        self.canvas = tkinter.Canvas(self, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        # After it is called once, the update method will be automatically called every delay milliseconds
        # calculate delay using `FPS`
        self.delay = int(1000/self.vid.fps)

        #print('[tkCamera] source:', self.source)
        #print('[tkCamera] fps:', self.vid.fps, 'delay:', self.delay)

        self.image = None

        self.dialog = None

        self.running = True
        self.update_frame()


    def update_frame(self):
        """TODO: add docstring"""

        # widgets in tkinter already have method `update()` so I have to use different name -

        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.image = frame
            self.photo = PIL.ImageTk.PhotoImage(image=self.image)
            self.canvas.create_image(0, 0, image=self.photo, anchor='nw')

        if self.running:
            self.after(self.delay, self.update_frame)
