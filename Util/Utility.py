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
