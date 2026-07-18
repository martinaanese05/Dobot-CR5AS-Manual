"""
GRIPPER CONTROL - via Tool Digital Output (ToolDOInstant)
============================================================

Commands covered in this file:
  - SetToolPower()   turns power to the tool (gripper) on/off
  - ToolDOInstant()  instantly toggles a tool digital output
  - GetToolDO()      reads the current state of a tool digital output

Many pneumatic/electric grippers are controlled the simplest way
possible: by turning a digital output ON or OFF, which physically
triggers the gripper to open or close. This is the most common and
straightforward gripper control method - if your gripper doesn't
need Modbus or Lua scripting, this is probably the approach to use.

NOTE: the exact digital output NUMBER (we use "1" below) depends
on how your gripper is physically wired to the robot's tool
connector - check your gripper's own documentation or wiring
diagram to confirm which output number controls it.
"""

from time import sleep
from dobot_library.dobot_api import DobotApiDashboard

IP = "192.168.201.1"
dashboard = DobotApiDashboard(IP, 29999)
GRIPPER_OUTPUT = 1  # change this to match your gripper's wiring

print("Clearing errors and enabling...")
print(dashboard.ClearError())
sleep(0.5)
print(dashboard.EnableRobot())
sleep(1)

print("Setting speed to 20%...")
print(dashboard.SpeedFactor(20))
sleep(0.5)

# SetToolPower(1) turns ON power to the tool connector - most
# grippers need this before they'll respond to any commands at all.
print("\nTurning on tool power...")
result = dashboard.SetToolPower(1)
print(result)
sleep(1)


def open_gripper():
    print("Opening gripper (setting output to 1)...")
    dashboard.ToolDOInstant(GRIPPER_OUTPUT, 1)
    sleep(1)
    print("Gripper output state:", dashboard.GetToolDO(GRIPPER_OUTPUT))


def close_gripper():
    print("Closing gripper (setting output to 0)...")
    dashboard.ToolDOInstant(GRIPPER_OUTPUT, 0)
    sleep(1)
    print("Gripper output state:", dashboard.GetToolDO(GRIPPER_OUTPUT))


open_gripper()
sleep(1)
close_gripper()

# Always turn tool power back off and disable the robot when done.
print("\nTurning off tool power...")
dashboard.SetToolPower(0)

print("Disabling robot...")
dashboard.DisableRobot()
print("Done!")
