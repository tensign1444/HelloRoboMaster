import math
import logging
from Util import Log
from Util import Utility


# ------------------------- BEGIN HeadsUpTello CLASS ----------------------------

class HeadsUpTello():
    """
    An interface from Team "Heads-Up Flight" to control a DJI Tello RoboMaster 
    Drone. Inherits from the djitellopy.Tello class.
    """

    def __init__(self, drone_baseobject, minBat, mission_obj=None, debug_level=logging.INFO):
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

        # ___________Drone Objects_______________
        self.drone = drone_baseobject
        self.inAir = False
        self.mission_obj = mission_obj
        self.useBar = True
        self.homeX = 0
        self.homeY = 0
        self.homeZ = 0
        self.currentX = 0
        self.currentY = 0
        self.currentRotation = 0
        self.homeRotation = 0
        self.minBatteryLevel = minBat

        self.logger = Log.Log("Test", "tie", 120, 10, "lilTieLog", logging.INFO)
        try:
            self.drone.connect()
            self.logger.info("****Connected to ")
            self.connected = True
            self.barHeight = Utility.get_barometer(self.drone)
        except Exception as excp:
            self.logger.error(f"ERROR: could not connect to Trello Drone: {excp}")
            self.logger.critical(f" => Did you pass in a valid drone base object?")
            self.logger.critical(f" => Verify that your firewall allows UDP ports 8889 and 8890")
            self.logger.critical(f"    The Chromebook's firewall reverts to default settings every")
            self.logger.critical(f"    time that you restart the virtual Linux environment.")
            self.logger.critical(f" => You may need to connect to the drone with the Trello App.")
            self.disconnect()
            raise
        return

    def __del__(self):
        """ Destructor that gracefully closes the connection to the drone. """
        if self.connected:
            self.disconnect()
        exit(0)
        return

    def disconnect(self):
        """ Gracefully close the connection with the drone. """
        self.drone.end()
        self.connected = False
        print(f"Drone connection closed gracefully")
        return

    def takeoff(self):
        """Lifts the drone off the ground by sending the takeoff command. Timeout was added to not error."""
        if Utility:
            self.logger.info("Drone is taking off.")
            self.logger.info(f"current height: {Utility.get_Height(self.drone, self.useBar, self.barHeight)}")
            self.drone.takeoff()
            self.inAir = True

    def land(self):
        """Lands the drone by sending the drone the land command"""
        self.logger.info("Drone is landing.")
        self.drone.land()
        self.inAir = False

    def move(self, direction, cm):
        """Moves the drone"""
        # self.logger.info(f"Moving drone {direction} {cm} cm")
        self.drone.send_control_command(f"{direction} {cm}")

    def fly_up(self, moveAmount=0):
        """
        Moves drone up by the user specified amount.
        """
        ceilingHeight = self.mission_obj["ceiling"]
        currentHeight = Utility.get_Height(self.drone)
        self.logger.info(f"trying to move up {moveAmount}")
        self.logger.debug(f"ceiling height: {ceilingHeight}")
        self.logger.debug(f"current height: {currentHeight}")
        if currentHeight > ceilingHeight:
            self.logger.warning(f"I am higher than the ceiling {ceilingHeight}, Going down...")
            moveAmount = currentHeight - ceilingHeight
            self.move_down(int(moveAmount))
        elif currentHeight == ceilingHeight:
            return
        elif currentHeight + moveAmount > ceilingHeight:
            self.logger.warning(f"Moving {moveAmount} will put me higher than ceiling height...")
            moveAmount = ceilingHeight - currentHeight
            self.logger.info(f"New move amount is {moveAmount}")
            self.move_up(int(moveAmount))
        else:
            self.logger.debug(f"moving: {moveAmount}")
            self.move_up(int(moveAmount))
        self.logger.debug(f"New currentheight: {Utility.get_Height(self.drone, self.useBar)}")

    def checkMoveDown(self, moveAmount, currentHeight, floorHeight):
        """
        Checks that the move amount is valid
        :param moveAmount: the amount to move
        :return:
        """
        Utility.printHeight(self.drone, self.logger, self.mission_obj)
        if currentHeight < floorHeight:
            self.logger.warning(f"I am lower than the floor {floorHeight}, Going up...")
            moveAmount = floorHeight - currentHeight
            self.move_up(int(moveAmount))
        elif currentHeight == floorHeight:
            return
        elif currentHeight - moveAmount < floorHeight:
            self.logger.warning(f"Moving {moveAmount} will put me lower than floor height...")
            moveAmount = currentHeight - floorHeight
            self.logger.info(f"New move amount is {moveAmount}")
            self.move_down(int(moveAmount))
        else:
            self.logger.debug(f"moving: {moveAmount}")
            self.move_down(int(moveAmount))
        self.logger.debug(f"New currentheight: {Utility.get_Height(self.drone, self.useBar)}")

    def move_up(self, amount):
        """
        Custom move up function to tell if the move up amount is less than possible.
        """
        #if Utility.check_battery(self.drone, self.minBatteryLevel, self.logger):
        if amount < 20:
            self.logger.warning("Going to move down 30 then up 30 since move amount was {amount}")
            self.logger.info(f"Moving down {amount} cm.")
            self.drone.move_down(amount + 20)
            self.logger.info(f"Moving up {amount} cm.")
            self.drone.move_up(amount + 20)
        else:
            self.logger.info(f"Moving up {amount} cm.")
            self.drone.move_up(amount)

    def move_down(self, amount):
        """
        Custom move down function to tell if the move amount is less than possible
        test hello
        """
        #if Utility.check_battery(self.drone, self.minBatteryLevel, self.logger):
        if amount < 20:
            self.logger.warning(f"Going to move up 30 then down 30 since move amount was {amount}")
            self.logger.info(f"Moving up {amount} cm.")
            self.drone.move_up(amount + 20)
            self.logger.info(f"Moving down {amount} cm.")
            self.drone.move_down(amount + 20)
        else:
            self.logger.info(f"Moving down {amount} cm.")
            self.drone.move_down(amount)

    def move_right(self, amount):
        """
        Moves the drone to the right
        :param amount: the amount in cm to move the drone to the right.
        :return:
        """
        #if Utility.check_battery(self.drone, self.minBatteryLevel, self.logger):
        self.logger.info(f"Moving right {amount} cm.")
        self.move('right', amount)
        self.currentY -= amount

    def move_left(self, amount):
        """
        Moves the drone to the left
        :param amount: the amount in cm to move drone to the right.
        :return:
        """
        #if Utility.check_battery(self.drone, self.minBatteryLevel, self.logger):
        self.logger.info(f"Moving left {amount} cm.")
        self.move('left', amount)
        self.currentY += amount

    def move_forward(self, amount):
        """
        Move the drone forward
        :param amount: the amount in cm to move drone forward
        :return:
        """
        #if Utility.check_battery(self.drone, self.minBatteryLevel, self.logger):
        self.logger.info(f"Moving forward {amount} cm.")
        self.move('forward', amount)
        self.currentX += amount

    def move_back(self, amount):
        """
        Move the drone backward
        :param amount: the amount in cm to move the drone back
        :return:
        """
        #if Utility.check_battery(self.drone, self.minBatteryLevel, self.logger):
        self.logger.info(f"Moving back {amount} cm.")
        self.move('back', amount)
        self.currentX -= amount

    def goToPosition(self, x, y):
        """
        Custom go to position method. Checks if the new move amount is negative or positive
        this will then dictate the direction to go.

        param: X, x-coordinate to go too.
        param: Y, y-coordinate to go too.
        param: Z, z-coordinate to go too.
        return: none
        """
        self.logger.info(f"Going to position {x},{y} : X, Y, Z")
        newX = x - self.currentX
        newY = y - self.currentY
        if newX < 0:
            self.move_back(abs(newX))
        elif newX > 0:
            self.move_forward(newX)

        if newY < 0:
            self.move_right(abs(newY))
        elif newY > 0:
            self.move_left(newY)

    def go_to_point_rotation(self, x, y):
        """
        Goes to a point with rotation
        """
        self.rotate_to_bearing(self.getRotateAmount(x, y))
        self.move_forward(Utility.get_c(self.currentX,self.currentY,x,y))
        self.currentX = x
        self.currentY = y

    def rotate_ccw(self, degrees):
        """
        Rotates the drone counter-clock wise
        """
        #if Utility.check_battery(self.drone, self.minBatteryLevel, self.logger):
            #self.drone.rotate_counter_clockwise(degrees)
        self.drone.rotate_counter_clockwise(degrees)

    def rotate_cw(self, degrees):
        """
        Rotates the drone clockwise.
        """
        #if Utility.check_battery(self.drone, self.minBatteryLevel, self.logger):
            #self.drone.rotate_clockwise(degrees)
        self.drone.rotate_clockwise(degrees)

    def goHome(self, directFlight):
        """
        Takes the drone home by using a custom go to specific position method.
        """
        self.fly_to_coordinates(self.homeX, self.homeY, directFlight)

    def getRotateAmount(self, x, y):
        """
        Rotates the drone to the exact point. This means the front of the drone will now face that point.
        """
        myradians = math.atan2(x - self.currentX, y - self.currentY)
        mydegrees = abs(int(math.degrees(myradians)))
        return mydegrees

    def rotate_to_bearing(self,degrees):
        """
        Rotates the drone to a specific bearing by finding the shortest rotation path given the amount of degrees.
        """
        ccwRotation = int(degrees)
        cwRotation = 360 - int(degrees)
        if ccwRotation > cwRotation:
            self.rotate_cw(cwRotation)
        else:
            self.rotate_ccw(ccwRotation)

    def newHome(self):
        """
        Sets new home coords for the drone.
        """
        self.homeX, self.homeY, self.homeZ = self.currentX, self.currentY, Utility.get_Height(self.drone, self.useBar)


    def fly_to_coordinates(self,x, y, direct_flight=False):
        """
        Fly the drone to a specific coordinate and decide if you want direct flight.
        """
        if direct_flight:
            self.go_to_point_rotation(x,y)
        else:
            self.goToPosition(x,y)

    def tether_distance(self, direction):
        directions = {'forward', 'backward', 'left', 'right'}
        if not direction in directions:
            return False
        else:




# ------------------------- END OF HeadsUpTello CLASS ---------------------------
