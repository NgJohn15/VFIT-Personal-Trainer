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


def display_angle():
    pass


def record():

    if not os.path.exists('exercises'):
        os.makedirs('exercises')

    # Saving Exercise name, and starting CV view
    gesture_file_name = "exercises/" + str(
        input("Enter the name of the gesture you want to record.\n")) + ".txt"

    file_counter = 1
    filename, extension = os.path.splitext(gesture_file_name)
    while os.path.exists(gesture_file_name):
        gesture_file_name = filename + \
            str("_{}".format(file_counter)) + extension
        file_counter += 1

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

        recording_length = 4
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
                video_pose.write(image)

                # INTER_CUBIC interpolation
                image = cv2.resize(image, (1920, 1080),
                                   interpolation=cv2.INTER_CUBIC)
                # writing pose data to file
                with open(gesture_file_name, "a") as template_file:
                    # Drawing angles to image.
                    joints = results.pose_landmarks.landmark
                    angles_needed = [[16, 14, 12], [15, 13, 11], [14, 12, 24], [13, 11, 23], [12, 24, 26],
                                     [11, 23, 25], [24, 26, 28], [23, 25, 27], [26, 28, 32], [25, 27, 31], [20, 16, 14], [19, 15, 13]]
                    angles_arr = []

                    for joint in angles_needed:
                        angle = get_angle([joints[joint[0]].x, joints[joint[0]].y], [
                                          joints[joint[1]].x, joints[joint[1]].y], [joints[joint[2]].x, joints[joint[2]].y])
                        angles_arr.append(angle)
                        cv2.putText(image, str(angle), tuple(np.multiply([joints[joint[1]].x, joints[joint[1]].y], [
                                    1920, 1080]).astype(int)), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

                    template_file.write(
                        str(angles_arr)[1:len(str(angles_arr))-1] + "\n")
                    template_file.close()

            else:
                image = np.zeros((1920, 1080, 3), np.uint8)
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
