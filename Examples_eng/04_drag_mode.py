"""
DRAG MODE - manually hand-guiding the robot
==============================================

Commands covered in this file:
  - StartDrag()  puts the robot into drag/teach mode
  - StopDrag()   takes the robot back out of drag mode

Drag mode lets you physically grab the robot's arm and move it by
hand - the motors go "loose" enough to be pushed, while the robot
still tracks its own position. This is commonly used to:
  - manually guide the robot to a position, then read that
    position with GetAngle() / GetPose() to reuse in a script
  - quickly test reachability of a point without programming it

SAFETY NOTE: even in drag mode, the robot is still powered on.
Standard safety protocols still apply (clear space, stay aware,
e-stop within reach).
"""

from time import sleep
from dobot_library.dobot_api import DobotApiDashboard

IP = "192.168.201.1"
dashboard = DobotApiDashboard(IP, 29999)

print("Clearing errors and enabling...")
print(dashboard.ClearError())
sleep(0.5)
print(dashboard.EnableRobot())
sleep(1)

# StartDrag() puts the robot into a "loose", hand-guidable state.
print("\nStarting drag mode - you can now move the arm by hand.")
print(dashboard.StartDrag())

# In a real script, you'd normally pause here and let a person
# physically move the robot, then read its position. We simulate
# that pause with input() so the script waits for you.
input("Move the robot by hand, then press Enter here to continue...")

# GetAngle() lets you read wherever the robot ended up after being
# dragged - useful for recording a taught position.
print("Position after dragging:", dashboard.GetAngle())

# StopDrag() exits drag mode and returns to normal operation -
# the robot will hold its position rigidly again.
print("\nStopping drag mode...")
print(dashboard.StopDrag())

sleep(1)
print("Disabling robot...")
dashboard.DisableRobot()
print("Done!")
