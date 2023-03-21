import cv2
import mediapipe as mp
import numpy as np
import time

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
cv2.namedWindow('Merge View', cv2.WINDOW_NORMAL)
cv2.setWindowProperty(
    'Merge View', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # this is the magic!

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
prev_frame_time = 0
new_frame_time = 0
with mp_pose.Pose(
        model_complexity=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
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
            blank_image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

        # Flip the image horizontally for a selfie-view display.
        if results.pose_landmarks != None:
            print("nose:\n", results.pose_landmarks.landmark[0])
        else:
            print("please stand in the center of the frame!")
        new_frame_time = time.time()
        fps = 1/(new_frame_time-prev_frame_time)
        prev_frame_time = new_frame_time

        # converting the fps into integer
        fps = int(fps)

        # converting the fps to string so that we can display it on frame
        # by using putText function
        fps = str(fps)

        # Good Merge view implmentation - No FPS loss
        # cv2.imshow('Merge View', blank_image)
        dst = cv2.addWeighted(image, 1, blank_image, 1, 0)
        verti = np.concatenate((blank_image, dst), axis=0)
        # INTER_CUBIC interpolation
        verti = cv2.resize(verti, (320, 360), interpolation=cv2.INTER_CUBIC)
        # cv2.imshow('Test View', verti)
        hori = np.concatenate((image[:, 120:520], verti), axis=1)
        # INTER_CUBIC interpolation
        hori = cv2.resize(hori, (1920, 1080), interpolation=cv2.INTER_CUBIC)
        cv2.putText(img=hori, text=fps, org=(
            0, 70), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=2, color=(0, 255, 0), thickness=1)
        cv2.imshow('Merge View', hori)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
