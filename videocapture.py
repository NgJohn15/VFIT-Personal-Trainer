#!/usr/bin/env python

# author: Bartlomiej "furas" Burek (https://blog.furas.pl)
# date: 2021.01.26

import time
import threading
import cv2
import PIL.Image
import mediapipe as mp
import numpy as np
import keyboard
import os
import math


"""TODO: add docstring"""


class VideoCapture:

    def __init__(self, video_source=0, width=None, height=None, fps=None, exercise_type="None"):
        """TODO: add docstring"""

        self.video_source = video_source
        self.width = width
        self.height = height
        self.fps = fps
        self.exercise_type = exercise_type

        self.running = False

        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError(
                "[MyVideoCapture] Unable to open video source", video_source)

        # Get video source width and height
        if not self.width:
            # convert float to int
            self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        if not self.height:
            # convert float to int
            self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if not self.fps:
            # convert float to int
            self.fps = int(self.vid.get(cv2.CAP_PROP_FPS))

        # default value at start
        self.ret = False
        self.frame = None

        self.convert_color = cv2.COLOR_BGR2RGB
        # self.convert_color = cv2.COLOR_BGR2GRAY
        self.convert_pillow = True

        # default values for recording
        self.recording = False
        self.recording_filename = 'output.mp4'
        self.recording_writer = None

        # start thread
        self.running = True
        self.thread = threading.Thread(target=self.process)
        self.thread.start()

    exercise_state = None
    exercise_counter = 0
    feedback = None
    exercise_set = 1
    score = 0

    def get_data(self):
        return [self.exercise_state, self.exercise_counter, self.feedback, self.exercise_set, self.score, self.exercise_type]

    def process(self):
        """TODO: add docstring"""
        if self.video_source == 0:
            def print_text(text, image_name):
                font = cv2.FONT_HERSHEY_DUPLEX
                textsize = cv2.getTextSize(text, font, 1, 1)[0]
                textX = (image_name.shape[1] - textsize[0]) // 4
                textY = (image_name.shape[0]) // 2
                cv2.putText(image_name, text, (textX, textY),
                            font, 1, (0, 255, 0), 1)

            def get_angle(a, b, c):
                a = np.array(a)
                b = np.array(b)
                c = np.array(c)

                radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - \
                    np.arctan2(a[1] - b[1], a[0] - b[0])
                angle = np.abs(radians*180.0/np.pi)

                if angle > 180:
                    angle = 360 - angle
                return angle

            def bicep_curls(joint_arr, angles_arr_stream, state, count):
                if (joint_arr[14].visibility >= 0.9):
                    if angles_arr_stream[0] > 160 and angles_arr_stream[2] < 10:
                        state = "down"
                    elif angles_arr_stream[0] < 45 and state == "down" and angles_arr_stream[2] < 10:
                        state = "up"
                        count += 1
                        self.score +=100
                    elif angles_arr_stream[2] > 10:
                        self.feedback = "Keep your upper arm stationary and your elbow close to your body!"
                elif (joint_arr[13].visibility >= 0.9):
                    if angles_arr_stream[1] > 160 and angles_arr_stream[3] < 10:
                        state = "down"
                    elif angles_arr_stream[1] < 45 and state == "down" and angles_arr_stream[3] < 10:
                        state = "up"
                        count += 1
                        self.score +=100
                    elif angles_arr_stream[3] > 10:
                        self.feedback = "Keep your upper arm stationary and your elbow close to your body!"
                return state, count

            def squats(joint_arr, angles_arr_stream, state, count):
                if (joint_arr[26].visibility >= 0.9):
                    if angles_arr_stream[6] > 160 and (angles_arr_stream[2] > 60 and angles_arr_stream[2] < 120):
                        state = "up"
                    elif angles_arr_stream[6] < 100 and state == "up" and (angles_arr_stream[2] > 60 and angles_arr_stream[2] < 120) and (angles_arr_stream[4] < 160 and angles_arr_stream[4] > 50):
                        state = "down"
                        count += 1
                        self.score +=100
                    elif (angles_arr_stream[2] < 60 or angles_arr_stream[2] > 120):
                        self.feedback = "Keep your arms extended, perpendicular to your body!"
                    elif (angles_arr_stream[6] < 100 and state == "up" and (angles_arr_stream[4] > 160 or angles_arr_stream[4] < 50)):
                        self.feedback = "Keep an eye on your lower back posture! Bend your torso like in the reference video"

                elif (joint_arr[25].visibility >= 0.9):
                    if angles_arr_stream[7] > 160 and (angles_arr_stream[3] > 60 and angles_arr_stream[3] < 120):
                        state = "up"
                    elif angles_arr_stream[7] < 100 and state == "up" and (angles_arr_stream[3] > 60 and angles_arr_stream[3] < 120) and (angles_arr_stream[5] < 160 and angles_arr_stream[5] > 50):
                        state = "down"
                        count += 1
                        self.score +=100
                    elif (angles_arr_stream[3] < 60 or angles_arr_stream[3] > 120):
                        self.feedback = "Keep your arms extended, perpendicular to your body!"
                    elif (angles_arr_stream[7] < 100 and state == "up" and (angles_arr_stream[5] > 160 or angles_arr_stream[5] < 50)):
                        self.feedback = "Keep an eye on your lower back posture! Bend your torso like in the reference video"
                return state, count

            def lunges(joint_arr, angles_arr_stream, state, count):
                if (joint_arr[26].visibility >= 0.9):
                    if ((angles_arr_stream[6] > 160 and angles_arr_stream[7] > 160) and angles_arr_stream[2] < 15 and angles_arr_stream[4] > 160):
                        state = "up"
                    elif ((angles_arr_stream[6] < 100 and angles_arr_stream[7] < 100) and state == "up" and angles_arr_stream[2] < 15 and angles_arr_stream[4] > 160):
                        state = "down"
                        count += 1
                        self.score +=100
                    elif ((angles_arr_stream[6] < 140 and angles_arr_stream[6] > 100) or (angles_arr_stream[7] < 140 and angles_arr_stream[7] > 100)):
                        self.feedback = "Go down deeper!"
                elif (joint_arr[25].visibility >= 0.9):
                    if ((angles_arr_stream[6] > 160 and angles_arr_stream[7] > 160) and angles_arr_stream[3] < 15 and angles_arr_stream[5] > 160):
                        state = "up"
                    elif ((angles_arr_stream[6] < 100 and angles_arr_stream[7] < 100) and state == "up" and angles_arr_stream[3] < 15 and angles_arr_stream[5] > 160):
                        state = "down"
                        count += 1
                        self.score +=100
                    elif ((angles_arr_stream[6] < 140 and angles_arr_stream[6] > 100) or (angles_arr_stream[7] < 140 and angles_arr_stream[7] > 100)):
                        self.feedback = "Go down deeper!"
                return state, count

            def jumping_jacks(joint_arr, angles_arr_stream, state, count):
                if (joint_arr[24].visibility >= 0.9 and joint_arr[23].visibility >= 0.9):
                    if ((angles_arr_stream[4] > 172) and angles_arr_stream[2] < 15):
                        state = "down"
                    elif (angles_arr_stream[4] < 170 and state == "down" and angles_arr_stream[2] > 160):
                        state = "up"
                        count += 1
                        self.score +=100
                return state, count
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing_styles = mp.solutions.drawing_styles
            mp_pose = mp.solutions.pose

            with mp_pose.Pose(
                    model_complexity=1,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5) as pose:

                prev_frame_time = 0
                new_frame_time = 0
                start_time = 0
                end_time = 0
                old_excercise_counter = 0
                loopover_temp_arr = 0
                while self.running:
                    ret, frame = self.vid.read()

                    if ret:

                        if self.exercise_counter > 15:
                            self.exercise_counter = 1
                            self.exercise_set += 1

                        # process image
                        # To improve performance, optionally mark the image as not writeable to
                        # pass by reference.
                        frame.flags.writeable = False
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        frame = cv2.flip(frame, 1)
                        results = pose.process(frame)

                        # Draw the pose annotation on the image.
                        frame.flags.writeable = True
                        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                        blank_image = np.zeros((360, 640, 3), np.uint8)
                        mp_drawing.draw_landmarks(
                            frame,
                            results.pose_landmarks,
                            mp_pose.POSE_CONNECTIONS,
                            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

                        if results.pose_landmarks != None:
                            self.feedback = "None"
                            # INTER_CUBIC interpolation
                            frame = cv2.resize(frame, (1920, 1080),
                                               interpolation=cv2.INTER_CUBIC)

                            # Reading and Printing Joint Angle data
                            joints = results.pose_landmarks.landmark
                            angles_needed = [[16, 14, 12], [15, 13, 11], [14, 12, 24], [13, 11, 23], [12, 24, 26],
                                             [11, 23, 25], [24, 26, 28], [23, 25, 27], [26, 28, 32], [25, 27, 31], [20, 16, 14], [19, 15, 13]]
                            angles_arr = []

                            for joint in angles_needed:
                                angle = get_angle([joints[joint[0]].x, joints[joint[0]].y], [
                                    joints[joint[1]].x, joints[joint[1]].y], [joints[joint[2]].x, joints[joint[2]].y])
                                angle = round(angle, 2)
                                angles_arr.append(angle)
                                """cv2.putText(frame, str(angle), tuple(np.multiply([joints[joint[1]].x, joints[joint[1]].y], [
                                            1920, 1080]).astype(int)), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)"""

                            frame = frame[:, 480:1440]
                            old_excercise_counter = self.exercise_counter
                            if self.exercise_type == "bicep_curls":
                                if (joints[13].visibility > 0.9 and joints[14].visibility > 0.9):
                                    '''print_text(
                                        "Please turn to one of your sides!", frame)'''
                                    self.feedback = "Please turn to one of your sides!"
                                self.exercise_state, self.exercise_counter = bicep_curls(
                                    joints, angles_arr, self.exercise_state, self.exercise_counter)
                            elif self.exercise_type == "squats":
                                if (joints[26].visibility > 0.9 and joints[25].visibility > 0.9):
                                    '''print_text(
                                        "Please turn to one of your sides!", frame)'''
                                    self.feedback = "Please turn to one of your sides!"
                                self.exercise_state, self.exercise_counter = squats(
                                    joints, angles_arr, self.exercise_state, self.exercise_counter)
                            elif self.exercise_type == "lunges":
                                self.exercise_state, self.exercise_counter = lunges(
                                    joints, angles_arr, self.exercise_state, self.exercise_counter)
                            elif self.exercise_type == "jumping_jacks":
                                self.exercise_state, self.exercise_counter = jumping_jacks(
                                    joints, angles_arr, self.exercise_state, self.exercise_counter)

                        else:
                            frame = np.zeros((1080, 960, 3), np.uint8)
                            print_text(
                                "please stand in the center of the frame!", frame)
                            self.feedback = "please stand in the center of the frame!"

                        new_frame_time = time.time()
                        fps = 1/(new_frame_time-prev_frame_time)
                        prev_frame_time = new_frame_time

                        # converting the fps into integer
                        fps = int(fps)

                        # converting the fps to string so that we can display it on frame
                        # by using putText function
                        fps = str(fps)

                        if self.feedback != "None":
                            cv2.rectangle(frame, (0, 0), (frame.shape[1],frame.shape[0]), color = (0,0,255), thickness = 15)

                        self.get_data()
                        if old_excercise_counter != self.exercise_counter:
                            cv2.rectangle(frame, (0, 0), (frame.shape[1],frame.shape[0]), color = (0,255,0), thickness = 15)

                        cv2.putText(frame, text="Score: " + str(self.score), org=(0, 30),
                                    fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1, color=(0, 255, 0), thickness=1)
                        cv2.putText(frame, text="Set: " + str(self.exercise_set), org=(
                            850, 30), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1, color=(255, 0, 0), thickness=1)
                        cv2.putText(frame, text="Rep: " + str(self.exercise_counter), org=(
                            680, 30), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1, color=(255, 0, 0), thickness=1)

                        frame = cv2.resize(frame, (self.width, self.height))

                        if self.convert_pillow:
                            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            frame = PIL.Image.fromarray(frame)

                    # assign new frame
                    self.ret = ret
                    self.frame = frame

        else:

            while self.running:
                ret, frame = self.vid.read()

                if ret:
                    # process image
                    frame = cv2.resize(
                        frame[:, (frame.shape[1]//4):(frame.shape[1] - (frame.shape[1]//4))], (self.width, self.height))

                    # it has to record before converting colors
                    if self.recording:
                        self.record(frame)

                    if self.convert_pillow:
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        frame = PIL.Image.fromarray(frame)
                else:
                    # print('[MyVideoCapture] stream end:', self.video_source)
                    # TODO: reopen stream
                    self.vid.set(cv2.CAP_PROP_POS_FRAMES, 0)

                # assign new frame
                self.ret = ret
                self.frame = frame

                # sleep for next frame
                time.sleep(1/self.fps)

    def get_frame(self):
        """TODO: add docstring"""

        return self.ret, self.frame

    # Release the video source when the object is destroyed
    def __del__(self):
        """TODO: add docstring"""

        # stop thread
        if self.running:
            self.running = False
            self.thread.join()

        # relase stream
        if self.vid.isOpened():
            self.vid.release()
