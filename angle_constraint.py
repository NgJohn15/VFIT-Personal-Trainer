import cv2
import mediapipe as mp
import numpy as np
import time
import keyboard
import os
import math

from scipy.spatial.distance import euclidean
from fastdtw import fastdtw


def print_text(text, image_name):
    font = cv2.FONT_HERSHEY_DUPLEX
    textsize = cv2.getTextSize(text, font, 1, 2)[0]
    textX = (image_name.shape[1] - textsize[0]) // 4
    textY = (image_name.shape[0]) // 2
    cv2.putText(image_name, text, (textX, textY), font, 2, (0, 255, 0), 1)


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


def bicep_curl(joint_arr, angles_arr_stream, state, count):
    if (joint_arr[14].visibility >= 0.9):
        if angles_arr_stream[0] > 160 and angles_arr_stream[2] < 10:
            state = "down"
        elif angles_arr_stream[0] < 30 and state == "down" and angles_arr_stream[2] < 10:
            state = "up"
            count += 1
    elif (joint_arr[13].visibility >= 0.9):
        if angles_arr_stream[1] > 160 and angles_arr_stream[3] < 10:
            state = "down"
        elif angles_arr_stream[1] < 30 and state == "down" and angles_arr_stream[3] < 10:
            state = "up"
            count += 1
    return state, count


def record(exercise_type):

    cv2.namedWindow('Inference Window', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(
        'Inference Window', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # this is the magic!

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)
    prev_frame_time = 0
    new_frame_time = 0

    start_time_dtw = time.time()
    end_time_dtw = 0
    dtw_array = []

    with mp_pose.Pose(
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:

        exercise_state = None
        exercise_counter = 0

        start_time = 0
        end_time = 0

        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.flip(image, 1)
            results = pose.process(image)

            # Draw the pose annotation on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            blank_image = np.zeros((360, 640, 3), np.uint8)
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

            if results.pose_landmarks != None:
                # INTER_CUBIC interpolation
                image = cv2.resize(image, (1920, 1080),
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
                    cv2.putText(image, str(angle), tuple(np.multiply([joints[joint[1]].x, joints[joint[1]].y], [
                                1920, 1080]).astype(int)), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

                if exercise_type == "bicep_curl":
                    if (joints[13].visibility > 0.9 and joints[14].visibility > 0.9):
                        print_text(
                            "Please turn to one of your sides!", image)
                    exercise_state, exercise_counter = bicep_curl(
                        joints, angles_arr, exercise_state, exercise_counter)

            else:
                image = np.zeros((1080, 1920, 3), np.uint8)
                print_text(
                    "please stand in the center of the frame!", image)

            new_frame_time = time.time()
            fps = 1/(new_frame_time-prev_frame_time)
            prev_frame_time = new_frame_time

            # converting the fps into integer
            fps = int(fps)

            # converting the fps to string so that we can display it on frame
            # by using putText function
            fps = str(fps)

            cv2.putText(image, text="FPS: " + fps, org=(0, 30),
                        fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1, color=(0, 255, 0), thickness=1)
            cv2.putText(image, text="press q to quit", org=(
                0, 1065), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1, color=(0, 255, 0), thickness=1)
            cv2.putText(image, text=exercise_state, org=(
                1800, 40), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1, color=(0, 255, 0), thickness=1)
            cv2.putText(image, text="Rep: " + str(exercise_counter), org=(
                1600, 40), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1, color=(0, 255, 0), thickness=1)

            cv2.imshow('Inference Window', image)
            if (cv2.waitKey(5) & 0xFF == ord('q')) or (keyboard.is_pressed("q")):
                break

            end_time_dtw = time.time()

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    record("bicep_curl")
