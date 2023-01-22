import logging
import os
import sys
import time
class Log:
    def __init__(self, name, drone, floor, ceiling, log_dir=None, debug_level=logging.INFO):
        """
        Constructor for a custom logging class.
        This class will print logs to a file and console.
        """
        self.mission_name = name
        self.drone = drone
        self.floor = floor
        self.ceiling = ceiling

        self.logger = logging.getLogger(f'{self.mission_name}')

        # create formatter
        formatter = logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.CheckForFile(log_dir)
        #file handler
        fileHandler = logging.FileHandler(f"{log_dir}.log")
        fileHandler.setFormatter(formatter)
        self.logger.addHandler(fileHandler)

        #Console Handler
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.INFO)
        consoleHandler.setFormatter(formatter)
        self.logger.addHandler(fileHandler)
        self.BeginLog()


    def CheckForFile(self, log_dir):
        """
        Checks if the log file directy exist. If not it will create one.
        Handle Linux and other OS.
        """
        if not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
            except:
                print('{}: Cannot create directory {}. '.format(
                    self.__class__.__name__, log_dir),
                    end='', file=sys.stderr)
                log_dir = '/tmp' if sys.platform.startswith('linux') else '.'
                print(f'Defaulting to {log_dir}.', file=sys.stderr)


    def BeginLog(self):
        """
        Beginning of the log file.
        """
        self.logger.info(f"------------------------------------")
        self.logger.info(f"|Mission Parameters:               |")
        self.logger.info(f"|  Mission : {self.mission_name}   |")
        self.logger.info(f"|  Drone   : {self.drone}          |")
        self.logger.info(f"|  Floor   : {self.floor}          |")
        self.logger.info(f"| Ceiling  : {self.ceiling}        |")
        self.logger.info(f"------------------------------------")

    def info(self, message):
        """
        Logs an info message to the console and file.
        """
        self.logger.info(message)

    def debug(self, message):
        """
        Logs an debug message to the console and file.
        """
        self.logger.debug(message)

    def warning(self, message):
        """
        Logs an warning message to the console and file.
        """
        self.logger.warning(message)

    def critical(self, message):
        """
        Logs a critical message to the console and file.
        """
        self.logger.critical(message)

    def error(self, message):
        """
        Logs an error message to the console and file.
        """
        self.logger.error(message)
