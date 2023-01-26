#!/usr/bin/env python3

# Standard python modules
import time
import logging
import json
import cv2, math, time
import Log
# Custom modules for the drones
from djitellopy import Tello
from headsupflight import HeadsUpTello


#-------------------------------------------------------------------------------
# LED Matrix Display Pictures
#-------------------------------------------------------------------------------
class Flight():

    # Two ways of storing the same logo... second one is easier to see, right?
    huf_logo1 = "000**000000**0000******00******0000**000000**000000**000000**000"
    huf_logo2 = "*000000*" +\
            "*000000*" +\
            "*00**00*" +\
            "********" +\
            "********" +\
            "*00**00*" +\
            "*000000*" +\
            "*000000*"


    huf_logo3 = "*0*00000" +\
            "***00000" +\
            "*0*00000" +\
            "00000000" +\
            "00000000" +\
            "00000000" +\
            "00000000" +\
            "00000000"

    #----------------------------------currentHeight


    def __init__(self):

        mission_obj = {'ceiling': 160, 'floor': 50}
        # mission_obj = {'ceiling':150, 'floor':100}
        # mission_obj = {'ceiling':200, 'floor':100}
        self.mission_name = 'Mission 05'

        # Connect to the DJI RoboMaster drone using a HeadsUpTello object
        # Try passing logging.INFO and see how your output changesy
        self.my_robomaster = Tello()
        self.drone = HeadsUpTello(self.my_robomaster, mission_obj, logging.INFO)

        self.inAir = False

    def read_json(self):
        """
        Reads data from the mission01 json file
        returns it as a dictionary
        """
        # Opening JSON file
        with open('mission_obj.json') as json_file:
            data = json.load(json_file)
        return data

    def mission_01(self):
        """
        Requirements for Mission 01:
          >> Display team logo for 5 seconds
          >> Print out the battery level
        There are a few extra features I've included for fun.
        """


        print(f"Battery: {self.drone.get_battery()}%")
        print(f"Temp °F: {self.drone.get_temperature()}")
        self.drone.takeoff()


        self.drone.goToPoisitionRotation(50,50)
        self.drone.goToPoisitionRotation(60,60)
        time.sleep(1)


        self.drone.goHome()

        time.sleep(1)

        self.drone.land()
        self.drone.disconnect()
        return


    def controller(self):
        self.drone.streamon()
        frame_read = self.drone.get_frame_read()

        self.drone.takeoff()

        while True:

            img = frame_read.frame
            cv2.imshow("drone", img)

            key = cv2.waitKey(1) & 0xff
            if key == 27:  # ESC
                break
            elif key == ord('w'):
                print("w pressed")
                self.drone.move_forward(30)
            elif key == ord('s'):
                self.drone.move_back(30)
            elif key == ord('a'):
                self.drone.move_left(30)
            elif key == ord('d'):
                self.drone.move_right(30)
            #  elif key == ord('e'):
            # self.drone.rotate_clockwise(30)
            # elif key == ord('q'):
            #  self.drone.rotate_counter_clockwise(30)
            elif key == ord('r'):
                self.drone.move_up(30)
            elif key == ord('f'):
                self.drone.move_down(30)

    """
    method to turn on the drone leds
    """

    def led(self):
        # Turn the top LED bright green and show our logo on the matrix display

        self.drone.matrix_pattern(self.huf_logo2, 'b')
        r = 0
        g = 200
        b = 50
        self.drone.top_led_color(r, g, b)

        # Slowly dim the top LED without changing the LED matrix
        # The loop runs 100 times with a 0.05 second delay => 5 seconds
        # These colors don't exactly match up to true RGB colors
        for i in range(10):
            g -= 20
            b -= 5

            self.drone.top_led_color(r, g, b)
            time.sleep(1)

        # Turn off the LED matrix and make the top LED red for two seconds
        self.drone.top_led_color(200, 10, 10)
        time.sleep(2)

        self.drone.matrix_off()
        self.drone.top_led_off()

#-------------------------------------------------------------------------------
# Python Entry Point
#-------------------------------------------------------------------------------

if __name__ == '__main__':
    try:
        flight = Flight()
        flight.mission_01()
        print(f"Mission completed")
    except Exception as excp:
        print(excp)
        print(f"Mission aborted")


