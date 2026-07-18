"""
CONNECT AND STATUS - checking the robot is alive and healthy
==============================================================

Commands covered in this file:
  - EnableRobot()   powers up the robot
  - DisableRobot()  powers down the robot
  - ClearError()    resets an alarm/error state
  - RobotMode()     asks the robot what state it's currently in

Use this file to check your connection and read the robot's
status BEFORE writing any script that makes it move.
"""

from time import sleep
from dobot_library.dobot_api import DobotApiDashboard

IP = "192.168.201.1"
dashboard = DobotApiDashboard(IP, 29999)

# ClearError() should be one of the first things you call in any
# script. It doesn't fix the CAUSE of a past error, it just resets
# the "I'm in an error state" flag, so the robot is willing to
# accept commands again.
print("Clearing errors...")
print(dashboard.ClearError())
sleep(0.5)

# EnableRobot() powers up the motors. Until this is called, the
# robot will reject movement commands.
print("Enabling robot...")
print(dashboard.EnableRobot())
sleep(1)

# RobotMode() returns a number describing what the robot is doing
# right now. Some of the common values you'll see:
#   4 = powered on but NOT enabled
#   5 = enabled and ready
#   6 = in drag/teach mode
#   7 = currently running a motion command
#  10 = paused
# This is useful to check inside loops - e.g. "wait until mode is
# 5 before sending the next command".
print("Current robot mode:", dashboard.RobotMode())

sleep(2)

# DisableRobot() cuts motor power in a controlled way. Always call
# this at the end of a script, rather than just closing the window.
print("Disabling robot...")
print(dashboard.DisableRobot())

print("Done!")
