import cv2
import mediapipe as mp
import numpy as np
import time
import keyboard
import os


def print_text(text, image_name):
    font = cv2.FONT_HERSHEY_DUPLEX
    textsize = cv2.getTextSize(text, font, 1, 2)[0]
    textX = (image_name.shape[1] - textsize[0]) // 4
    textY = (image_name.shape[0]) // 2
    cv2.putText(image_name, text, (textX, textY), font, 2, (0, 255, 0), 1)


def record():

    # Saving Exercise name, and starting CV view
    gesture_file_name = str(
        input("Enter the name of the gesture you want to record.\n")) + ".txt"

    with open(gesture_file_name, "w") as template_file:
        template_file.close()

    '''print("Press 'Enter' to start recording")
    keyboard.wait("enter")'''

    t = 5
    cv2.namedWindow('Merge View', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(
        'Merge View', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Countdown to Begin Recording Exercise:
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        # print(timer, end="\r")
        print("Recording will start in {sec} seconds.".format(
            sec=timer), end="\r")
        blank_image = np.zeros((640, 360, 3), np.uint8)
        # INTER_CUBIC interpolation
        blank_image = cv2.resize(
            blank_image, (1920, 1080), interpolation=cv2.INTER_CUBIC)
        print_text("Recording will start in {sec} seconds.".format(
            sec=timer), blank_image)

        cv2.imshow('Merge View', blank_image)
        cv2.waitKey(5)
        time.sleep(1)
        t -= 1

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # this is the magic!
    video_pose = cv2.VideoWriter(gesture_file_name[:len(
        gesture_file_name)-4]+'.avi', cv2.VideoWriter_fourcc(*"MJPG"), 24, (640, 360))

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)
    prev_frame_time = 0
    new_frame_time = 0
    with mp_pose.Pose(
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:

        recording_length = 10
        start_time = time.time()
        end_time = 0
        while cap.isOpened() and (end_time - start_time <= recording_length):
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
                # writing pose data to file
                with open(gesture_file_name, "a") as template_file:
                    temp_text = []
                    for data_point in results.pose_landmarks.landmark:
                        temp_text.append([
                            data_point.x,
                            data_point.y,
                            data_point.z,
                            data_point.visibility,
                        ])
                    template_file.write(str(temp_text) + "\n")
                    template_file.close()
                    video_pose.write(image)

            else:
                print("please stand in the center of the frame!")
                blank_image = np.zeros((640, 360, 3), np.uint8)
                # INTER_CUBIC interpolation
                blank_image = cv2.resize(
                    blank_image, (1920, 1080), interpolation=cv2.INTER_CUBIC)
                print_text(
                    "please stand in the center of the frame!", blank_image)

            new_frame_time = time.time()
            fps = 1/(new_frame_time-prev_frame_time)
            prev_frame_time = new_frame_time

            # converting the fps into integer
            fps = int(fps)

            # converting the fps to string so that we can display it on frame
            # by using putText function
            fps = str(fps)
            # INTER_CUBIC interpolation
            image = cv2.resize(image, (1920, 1080),
                               interpolation=cv2.INTER_CUBIC)
            cv2.putText(image, text="FPS: " + fps, org=(0, 30),
                        fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1, color=(0, 255, 0), thickness=1)
            cv2.putText(image, text="press q to quit", org=(
                0, 1065), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1, color=(0, 255, 0), thickness=1)
            cv2.putText(image, text="Recording will stop in {:02d} seconds.".format(recording_length - int(end_time - start_time)), org=(
                1350, 1065), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1, color=(0, 255, 0), thickness=1)
            cv2.imshow('Merge View', image)
            if (cv2.waitKey(5) & 0xFF == ord('q')) or (keyboard.is_pressed("q")):
                break

            end_time = time.time()

    cap.release()
    video_pose.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    record()
