"""
HELLO WORLD - Your first Dobot CR5AS script
=============================================

What this script does, step by step:
  1. Connects to the robot over the network (Dashboard port 29999)
  2. Clears any leftover errors and enables (powers up) the robot
  3. Moves ALL joints to their 0 degree position
  4. Moves joint 0 (the base, J1) to -30 degrees
  5. Moves joint 0 back to +30 degrees
  6. Moves joint 0 to +30 degrees again (kept as a repeated step -
     if you only need two moves, feel free to delete this last one)
  7. Prints out what it's doing at every step, and disables the
     robot when finished

This does NOT require you to understand robotics - it's meant to
show you the basic "shape" every Dobot script will have:
  connect -> enable -> move -> disable
"""

from time import sleep
from dobot_library.dobot_api import DobotApiDashboard

# ---------------------------------------------------------------
# STEP 1: Connection settings
# ---------------------------------------------------------------
# Replace this with YOUR robot's actual IP address.
# You can find it in DobotStudio Pro's connection screen, or by
# checking the Passwords and Connectivity section of this manual.
IP = "192.168.201.1"
DASHBOARD_PORT = 29999

# This line opens the connection. From this point on, "dashboard"
# is our remote control for the robot - every command below is
# sent through it.
dashboard = DobotApiDashboard(IP, DASHBOARD_PORT)


# ---------------------------------------------------------------
# STEP 2: Clear errors and enable the robot
# ---------------------------------------------------------------
# ClearError() resets any alarm left over from a previous session.
# It's good practice to always call this before enabling.
print("Clearing any previous errors...")
print(dashboard.ClearError())
sleep(0.5)  # A short pause gives the robot time to process the command

# EnableRobot() powers up the motors. The robot won't move at all
# until this succeeds - if this fails, check that:
#   - the IP address above is correct
#   - the robot is switched into TCP mode (see the TCP mode section)
print("Enabling the robot...")
print(dashboard.EnableRobot())
sleep(1)


# ---------------------------------------------------------------
# STEP 3: Set a safe speed before moving
# ---------------------------------------------------------------
# SpeedFactor takes a percentage (1-100). Starting slow (e.g. 20%)
# is strongly recommended while testing new scripts.
print("Setting speed to 20%...")
print(dashboard.SpeedFactor(20))
sleep(0.5)


# ---------------------------------------------------------------
# STEP 4: Move all joints to 0 degrees
# ---------------------------------------------------------------
# MovJ() moves the robot using joint-space motion (each joint
# rotates directly to its target angle - this is NOT a straight
# line in space, just the simplest way to move).
#
# The six numbers are the target angle for joints J1 through J6,
# in degrees. The final "1" tells the robot "these are joint
# angles" (as opposed to X/Y/Z coordinates).
print("\nMoving all joints to 0 degrees...")
result = dashboard.MovJ(0, 0, 0, 0, 0, 0, 1)
print(result)
sleep(3)  # Give the robot time to finish moving before continuing


# ---------------------------------------------------------------
# STEP 5: Move the base joint (J1) to -30, then +30, then +30 again
# ---------------------------------------------------------------
# Only the FIRST number changes here - that's J1, the base joint,
# the one that rotates the whole arm left/right. The other five
# stay at 0.

print("\nMoving base joint (J1) to -30 degrees...")
result = dashboard.MovJ(-30, 0, 0, 0, 0, 0, 1)
print(result)
sleep(3)

print("\nMoving base joint (J1) to +30 degrees...")
result = dashboard.MovJ(30, 0, 0, 0, 0, 0, 1)
print(result)
sleep(3)

print("\nMoving base joint (J1) to +30 degrees again...")
result = dashboard.MovJ(30, 0, 0, 0, 0, 0, 1)
print(result)
sleep(3)

print("\nMoving all joints to 0 degrees...")
result = dashboard.MovJ(0, 0, 0, 0, 0, 0, 1)
print(result)
sleep(3)


# ---------------------------------------------------------------
# STEP 6: Disable the robot when finished
# ---------------------------------------------------------------
# Always disable the robot at the end of a script. This cuts motor
# power in a controlled way, rather than leaving it enabled.
print("\nDisabling the robot...")
dashboard.DisableRobot()

print("Done! Hello, Dobot.")
