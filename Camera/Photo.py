from djitellopy import Tello
from datetime import datetime
import logging
from Util import Log
from Util import Utility
import cv2
import time

def cv2TextBoxWithBackground(img, text,
        font=cv2.FONT_HERSHEY_PLAIN,
        pos=(0, 0),
        font_scale=1,
        font_thickness=1,
        text_color=(30, 255, 205),
        text_color_bg=(48, 48, 48)):
    x, y = pos
    (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_pos = (x, y + text_h + font_scale)
    box_pt1 = pos
    box_pt2 = (x + text_w+2, y + text_h+2)
    cv2.rectangle(img, box_pt1, box_pt2, text_color_bg, cv2.FILLED)
    cv2.putText(img, text, text_pos, font, font_scale, text_color, font_thickness)
    return img


def take_photo(drone):
    drone.streamon()
    camera = drone.get_frame_read()

    print('Taking picture in 3s... ', end='', flush=True)
    time.sleep(1)
    print('2s... ', end='', flush=True)
    time.sleep(1)
    print("1s... ")
    time.sleep(1)
    print("**********")
    print("* CLICK! *")
    print("**********")

    image = camera.frame
    text = datetime.now().strftime("%Y-%m-%d %H:%m.%S")
    cv2TextBoxWithBackground(image, text)
    cv2.imwrite("my_drone_photo.png", image)

    cv2.imshow("My Drone Photograph", image)
    time.sleep(0.001)

    # Wait for the user to close the image window or press the ESCAPE key
    #   Start a while loop that finishes when the window is closed by clicking on
    #   the X button. Every time through the loop, we wait 100 ms for the user to
    #   press a key. If the key was ESCAPE then we quit. Otherwise we continue the
    #   loop again. It's important to wait some time so that the CPU does not spin
    #   around really fast in this loop and hog resources that would be better used
    #   elsewhere.

    value = 1.0
    while value >= 1.0:
        value = cv2.getWindowProperty("My Drone Photograph", cv2.WND_PROP_VISIBLE)
        key_code = cv2.waitKey(100)
        if key_code & 0xFF == 27:
            break


    # Turn off the video stream and the drone


def record(drone, fps):
    # Turn on video stream and get the BackgroundFrameRead object

    drone.streamon()
    camera = drone.get_frame_read()

    # To make the movie play at 'real life' speed, choose a frame rate and then
    # calculate the time delay between each frame. The video capture loop will have
    # to regulate itsejlf to write frames at the this frequency.

    movie_name = 'drone_capture.avi'
    movie_codec = cv2.VideoWriter_fourcc(*'mp4v')
    movie_fps = fps
    frame_wait = 1 / movie_fps
    movie_size = (360, 240)

    print(f"Recording movie at {movie_fps} FPS or 1/{frame_wait:.3f}s")

    # Show video by looping and showing frame by frame (animation style)
    # Notice that we can't do anything else except take video... if we want the
    #drone to do something else while taking video, we'll need to use threads

    frame_counter = 0
    time_prev = time.time()
    cv2.namedWindow("Drone Video Feed")
    movie = cv2.VideoWriter(movie_name, movie_codec, movie_fps, movie_size, True)

    while frame_counter < 10 * movie_fps:
        time_curr = time.time()
        time_elapsed = time_curr - time_prev
        if time_elapsed > frame_wait:
            image = camera.frame
            image = cv2.resize(image, movie_size)
            cv2.imshow("Drone Video Feed", image)
            cv2.waitKey(1)
            movie.write(image)
            time_prev = time_curr
            frame_counter += 1
            if frame_counter % movie_fps == 0:
                print(f"FRAME: {frame_counter} @ {time_elapsed}")
        cv2.waitKey(5)

    print("Finished!")