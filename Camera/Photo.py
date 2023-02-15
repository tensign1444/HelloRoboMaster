from djitellopy import Tello
from datetime import datetime
import logging
from Util import Log
from Util import Utility
import cv2
import time

class Photo():

    def __init__(self, drone_baseobject):
        self.drone = drone_baseobject
        self.logger = Log.Log("Test", "tie", 120, 10, "lilTieLog", logging.INFO)
        try:
            self.drone.connect()
            self.logger.info("****Connected to ")
            self.drone.turn_motor_on()
        except Exception as excp:
            self.logger.error(f"ERROR: could not connect to Trello Drone: {excp}")
            self.logger.critical(f" => Did you pass in a valid drone base object?")
            self.logger.critical(f" => Verify that your firewall allows UDP ports 8889 and 8890")
            self.logger.critical(f"    The Chromebook's firewall reverts to default settings every")
            self.logger.critical(f"    time that you restart the virtual Linux environment.")
            self.logger.critical(f" => You may need to connect to the drone with the Trello App.")
            self.disconnect()
            raise

    def disconnect(self):
        """ Gracefully close the connection with the drone. """
        self.drone.end()
        print(f"Drone connection closed gracefully")
        return


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


    def take_photo(self):
        self.drone.streamon()
        camera = self.drone.get_frame_read()

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
        self.cv2TextBoxWithBackground(image, text)
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

        print("Press the <ESC> key to quit")
        value = 1.0
        while value >= 1.0:
            value = cv2.getWindowProperty("My Drone Photograph", cv2.WND_PROP_VISIBLE)
            key_code = cv2.waitKey(100)
            if key_code & 0xFF == 27:
                break

        print("Destroying all picture windows")
        cv2.destroyAllWindows()

        # Turn off the video stream and the drone



    def close(self):
        print("Closing connection")
        time.sleep(1)
        self.drone.streamoff()
        self.drone.turn_motor_off()
        print(f"Battery level is {self.drone.get_battery()}%")
        self.disconnect()
        print("Mission Complete")