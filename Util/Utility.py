import math
from itertools import product
from math import radians, sin
from Util import dji_matrix as djim
from djitellopy import Tello


def get_battery(drone):
    """ Returns the drone's battery level as a percent. """
    return drone.get_battery()


def get_barometer(drone):
    """ Returns the drone's current barometer reading in cm. """
    return drone.get_barometer()


def get_temperature(drone):
    """ Returns the drone's internal temperature in °F. """
    return drone.get_temperature()


def get_Height(drone, barHeight, useBar):
    """
    Gets the height of the drone either using get height or barometer
    :return: the height of the drone
    """
    if (useBar):
        return drone.get_barometer() - barHeight
    return drone.get_height()


def top_led_off(drone):
    """ Turn off the top LED. """

    cmd = f"EXT led 0 0 0"
    drone.send_control_command(cmd)
    return


def matrix_pattern(drone, flattened_pattern: str, color: str = 'b'):
    """
    Show the flattened pattern on the LED matrix. The pattern should be
    64 letters in a row with values either (r)ed, (b)lue, (p)urple, or (0)
    off. The first 8 characters are the top row, the next 8 are the second
    row, and so on.

    Arguments
        flattened_pattern: see examples in dji_matrix.py
        color:             'r', 'b', or 'p'
    """

    if color.lower() not in "rpb":
        color = 'b'
    cmd = f"EXT mled g {flattened_pattern.replace('*', color.lower())}"
    drone.send_control_command(cmd)
    return


def printHeight(drone, logger, mission_obj):
    """
    Function to print height to log, so we aren't being repetitive.
    :return:
    """
    floorHeight = mission_obj["floor"]
    ceilingHeight = mission_obj["ceiling"]
    currentHeight = get_Height(drone)
    logger.debug(f"ceiling height: {ceilingHeight} || floor height: {floorHeight}")
    logger.debug(f"current height: {currentHeight}")


def check_battery(drone, minBatteryLevel, logger):
    """
    Checks battery level
    returns false if less than 20%, true if > 20%
    """
    if get_battery(drone) < minBatteryLevel:
        logger.error("Battery too low!")
        return False
    else:
        return True


def top_led_color(drone, red: int, green: int, blue: int):
    """
    Change the top LED to the specified color. The colors don't match the
    normal RGB palette very well.

    Arguments
        red:   0-255
        green: 0-255
        blue:  0-255
    """

    r = djim.capped_color(red)
    g = djim.capped_color(green)
    b = djim.capped_color(blue)
    cmd = f"EXT led {r} {g} {b}"
    drone.send_control_command(cmd)
    return


def matrix_off(drone):
    """ Turn off the 64 LED matrix. """

    off_pattern = "0" * 64
    matrix_pattern(drone, off_pattern)
    return


def get_unknown_sides(a1, a2, c):
    """
    Gets sides a and b when given side c and two angles.
    """
    a1, a2 = radians(a1), radians(a2)
    a3 = 3.14159 - a1 - a2

    return (c / sin(a3)) * sin(a1), (c / sin(a3)) * sin(a2)

def get_c(currentX, currentY, x, y):
    """
    Get's new coordinates *work in progress*
    """
    current = [currentX, currentY]
    new = [x, y]
    distance = math.dist(current, new)
    return distance

def get_coords_directflight(angleA, angleC, sideC):
    """
    Gets new x,y coords when direct flight is used.
    Uses the law of sines to find two unknown sides of a
    triangle.
    """
    angleB = 180 - angleC - angleA
    ycoord =  law_of_sines(angleA, angleC, sideC)
    xcoord = law_of_sines(angleB, angleC, sideC)
    return xcoord, ycoord

def law_of_sines(angleA,angleC, sideC):
    """
    Uses the law of sines to find an unknown side given
    two angles and a side of a triangle.
    """
    return int(math.sin(angleA) * sideC/math.sin(angleC))
def isInTether(center_x, center_y, rad, x, y):
    """
    Checks if the points x and y are within a circle
    with center_x and center_y with the given radius
    """
    if ((x - center_x) * (x - center_y) + (y - center_x) * (y - center_y) <= rad * rad):
        return True
    else:
        return False
