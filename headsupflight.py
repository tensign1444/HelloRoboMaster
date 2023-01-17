import time
from djitellopy import Tello
import dji_matrix as djim
import logging


# ------------------------- BEGIN HeadsUpTello CLASS ----------------------------

class HeadsUpTello():
    """
    An interface from Team "Heads-Up Flight" to control a DJI Tello RoboMaster 
    Drone. Inherits from the djitellopy.Tello class.
    """

    def __init__(self, drone_baseobject, mission_obj = None, debug_level=logging.INFO):
        """
        Constuctor that establishes a connection with the drone. Pass in a new
        djitellopy Tello object give your HeadsUpTello object its wings.

        Arguments
            drone_baseobject: A new djitellopy.Tello() object
            debug_level:      Set the desired logging level.
                              logging.INFO shows every command and response 
                              logging.WARN will only show problems
                              There are other possibilities, see logging module
        """

        # HeadsUpTello class uses the design principal of composition (has-a)
        # instead of inheritance (is-a) so that we can choose between the real
        # drone and a simulator. If we had used inheritance, we would be forced
        # to choose one or the other.
        self.drone = drone_baseobject
        self.drone.LOGGER.setLevel(debug_level)
        self.inAir = False;
        self.mission_obj = mission_obj

        try:
            self.drone.connect()
            self.connected = True
        except Exception as excp:
            print(f"ERROR: could not connect to Trello Drone: {excp}")
            print(f" => Did you pass in a valid drone base object?")
            print(f" => Verify that your firewall allows UDP ports 8889 and 8890")
            print(f"    The Chromebook's firewall reverts to default settings every")
            print(f"    time that you restart the virtual Linux environment.")
            print(f" => You may need to connect to the drone with the Trello App.")
            self.disconnect()
            raise
        return

    def __del__(self):
        """ Destructor that gracefully closes the connection to the drone. """
        if self.connected:
            self.disconnect()
        return

    def disconnect(self):
        """ Gracefully close the connection with the drone. """
        self.drone.end()
        self.connected = False
        print(f"Drone connection closed gracefully")
        return

    def top_led_color(self, red: int, green: int, blue: int):
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
        self.drone.send_control_command(cmd)
        return

    def top_led_off(self):
        """ Turn off the top LED. """

        cmd = f"EXT led 0 0 0"
        self.drone.send_control_command(cmd)
        return

    def matrix_pattern(self, flattened_pattern: str, color: str = 'b'):
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
        self.drone.send_control_command(cmd)
        return

    def matrix_off(self):
        """ Turn off the 64 LED matrix. """

        off_pattern = "0" * 64
        self.matrix_pattern(off_pattern)
        return

    def get_battery(self):
        """ Returns the drone's battery level as a percent. """
        return self.drone.get_battery()

    def get_barometer(self):
        """ Returns the drone's current barometer reading in cm. """
        return self.drone.get_barometer()

    def get_temperature(self):
        """ Returns the drone's internal temperature in °F. """
        return self.drone.get_temperature()

    def takeoff(self):
        """Lifts the drone off the ground by sending the takeoff command. Timeout was added to not error."""
        print("Drone is taking off.")
        print(f"current height: {self.drone.get_height()}")
        self.drone.takeoff()
        self.inAir = True

    def land(self):
        """Lands the drone by sending the drone the land command"""
        print("Drone is landing.")
        self.drone.land()
        self.inAir = False

    def move(self, direction, cm, hold=10):
        """Moves the drone"""
        print(f"Moving drone {direction} {cm} cm")
        self.drone.send_control_command(f"{direction} {cm}")
        time.sleep(hold)

    def fly_to_mission_floor(self):
        """Moves drone to the mission floor"""
        print("Going to floor...")
        floorHeight = self.mission_obj["floor"]
        if(self.inAir):     
            print(f"floor height: {floorHeight}")
           
            currentHeight = self.drone.get_height()
            print(f"current height: {currentHeight}")
            if(currentHeight > floorHeight):
                moveAmount = currentHeight - floorHeight
                print(f"moving: {moveAmount}")
                self.drone.move_down(int(moveAmount))
            elif(currentHeight < floorHeight):
                moveAmount = floorHeight - currentHeight
                print(f"moving: {moveAmount}")
                self.drone.move_up(int(moveAmount))
        print("At floor...")

    def fly_to_mission_ceiling(self):
        """Moves drone to the mission ceiling"""
        print("Going to ceiling...")
        ceilingHeight = self.mission_obj["ceiling"]
        if(self.inAir):
            
            print(f"ceiling height: {ceilingHeight}")          
            currentHeight = self.drone.get_height()
            print(f"current height: {currentHeight}")
            
            if(currentHeight > ceilingHeight):
                moveAmount = currentHeight - ceilingHeight
                print(f"moving: {moveAmount}")
                self.drone.move_down(int(moveAmount))
            elif(currentHeight < ceilingHeight):
                moveAmount = ceilingHeight - currentHeight
                print(f"moving: {moveAmount}")
                self.drone.move_up(int(moveAmount))
        print("At ceiling...")

# ------------------------- END OF HeadsUpTello CLASS ---------------------------
