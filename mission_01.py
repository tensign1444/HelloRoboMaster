#!/usr/bin/env python3

# Standard python modules
import time
import logging
import json

# Custom modules for the drones
from djitellopy import Tello
from headsupflight import HeadsUpTello


#-------------------------------------------------------------------------------
# LED Matrix Display Pictures
#-------------------------------------------------------------------------------

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
def read_json():
    """
    Reads data from the mission01 json file
    returns it as a dictionary
    """
    # Opening JSON file
    with open('mission_obj.json') as json_file:
        data = json.load(json_file)
    return data
    
def mission_01():
    """
    Requirements for Mission 01:
      >> Display team logo for 5 seconds
      >> Print out the battery level
    There are a few extra features I've included for fun.
    """

    mission_obj = {'ceiling':150, 'floor':50}
    #mission_obj = {'ceiling':150, 'floor':100}
    #mission_obj = {'ceiling':200, 'floor':100}

    # Connect to the DJI RoboMaster drone using a HeadsUpTello object
    # Try passing logging.INFO and see how your output changes
    my_robomaster = Tello()
    drone = HeadsUpTello(my_robomaster, mission_obj, logging.WARNING)

   
    # Finish the mission
    print(f"Battery: {drone.get_battery()}%")
    print(f"Temp °F: {drone.get_temperature()}")
    drone.takeoff()
    time.sleep(1)
    drone.fly_to_mission_floor()
    time.sleep(10)
    drone.fly_to_mission_ceiling()
    time.sleep(10)
    drone.land()
    time.sleep(1)
    drone.disconnect()
    return

"""
method to turn on the drone leds
"""
def led(drone):
    # Turn the top LED bright green and show our logo on the matrix display
    drone.matrix_pattern(huf_logo2, 'b')
    r = 0
    g = 200
    b = 50
    drone.top_led_color(r, g, b)

    # Slowly dim the top LED without changing the LED matrix
    # The loop runs 100 times with a 0.05 second delay => 5 seconds
    # These colors don't exactly match up to true RGB colors
    for i in range(10): 
        g -= 20
        b -= 5
        drone.top_led_color(r, g, b)
        time.sleep(1)

    # Turn off the LED matrix and make the top LED red for two seconds  
    drone.top_led_color(200, 10, 10)
    time.sleep(2)
    drone.matrix_off()
    drone.top_led_off()

#-------------------------------------------------------------------------------
# Python Entry Point
#-------------------------------------------------------------------------------

if __name__ == '__main__':
    try:
        mission_01()
        print(f"Mission completed")
    except Exception as excp:
        print(excp)
        print(f"Mission aborted")
