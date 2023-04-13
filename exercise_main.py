#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author: Bartlomiej "furas" Burek (https://blog.furas.pl)
# date: 2021.01.26

import os
import tkinter
from TKCamera import TKCamera


"""TODO: add docstring"""


HOME = os.path.dirname(os.path.abspath(__file__))


class App:
    def __init__(self, parent, title, sources):
        """TODO: add docstring"""

        self.parent = parent

        self.parent.title(title)

        self.stream_widgets = []

        width = 640
        height = 720

        columns = 2
        for number, (text, source, exercise_type) in enumerate(sources):
            widget = TKCamera(self.parent, text, source, width, height, exercise_type = exercise_type)
            row = number // columns
            col = number % columns
            widget.grid(row=row, column=col)
            self.stream_widgets.append(widget)

        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self, event=None):
        """TODO: add docstring"""

        print("[App] stoping threads")
        for widget in self.stream_widgets:
            widget.vid.running = False

        print("[App] exit")
        self.parent.destroy()


if __name__ == "__main__":

    ## John this var should have value passed by button click instead of hard coded.........so instead of bicep_curls str, it should be val passed by button press/exercise select......
    exercise = "bicep_curls"

    sources = [  # (text, source)
        # local webcams
        ("me", 0, exercise),
        # remote videos (or streams)
        (
            "Zakopane, Poland",
            "./exercises/" + exercise + ".mp4", "None"
        ),
    ]

    root = tkinter.Tk()
    App(root, "Tkinter and OpenCV", sources)
    root.mainloop()
