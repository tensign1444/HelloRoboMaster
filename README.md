# HelloRoboMaster

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

A simple program that connects to a RoboMaster TT Drone and displays a logo on the 8x8 LED matrix. All communication with the drone is through the DJITelloPy module.

## Table of Contents
- [Install](#install)
- [Usage](#usage)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Install
Download the files to a directory on your computer. The quickest way to do this is using git. Then you must pip install the DJI `djitellopy` module that allows you to easily interface with the RoboMaster TT Drone without having to worry about UDP packets. The DJI module handles this all for you under the hood.

To see the specific compile steps, view the Makefile using a command like `cat Makefile`. The most basic compiling command would something like this:
```
git clone https://github.com/prof-tallman/HelloRoboMaster
cd HelloRoboMaster
pip install djitellopy
```

Once you have downloaded the files and installed the dependencies (`djitellopy`), grab the drone.
1. Mount the Expansion Kit on top of the Tello Talent like a Lego brick.
1. Then plug the micro USB connector into the side of the drone. The connector is on the opposite side of the power button.
1. Install a fresh battery and turn on the drone. The front lights on the front should flash.

The drone should have created a WiFi access point. You'll need to join this WiFi network from your computer. By default, the AP will be named RMTT-XXXXXX since you have the Expansion Kit attached. If the Expansion Kit were missing, the AP would have been named TELLO-XXXXXX.

You'll need to open two UDP ports on your computer. The first port is probably easiest because it is an outgoing connection from your computer to the drone. But the second port need to be opened manually because it is an incoming connections from the drone.
* UDP port 8889
* UDP port 8890
Note: there is a third port for the drone's camera, but we don't use it here.

## Usage
Run the program through the Python3 interpreter. From the command line, it would be:
```
python3 mission_01.py
```
You should see the LEDs on your RoboMaster Drone light up and change colors. The program takes 5-10 seconds to run.

## Maintainers
[@JoshuaTallman](https://github.com/prof-tallman)

## Contributing
This program is written as an example for students.

## License
[MIT](LICENSE) © [@JoshuaTallman](https://github.com/prof-tallman)
