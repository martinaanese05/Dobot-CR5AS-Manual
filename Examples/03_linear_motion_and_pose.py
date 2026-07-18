"""
LINEAR MOTION AND POSE - moving in a straight line, and reading
position in X/Y/Z terms
==================================================================

Commands covered in this file:
  - MovL()     moves the tool in a straight line through space
  - GetPose()  reads the current tool position as X, Y, Z, Rx, Ry, Rz

Unlike MovJ (joint motion), MovL guarantees the tool tip travels
in a straight physical line between where it is now and the target.
This is useful whenever the PATH matters - e.g. moving along a
table surface without dipping down into it.

Coordinates here are in "Cartesian" terms:
  X, Y, Z    = position in millimeters, relative to a reference point
  Rx, Ry, Rz = orientation (rotation) of the tool, in degrees

This is more complex to reason about than joint angles, since you
need to know the robot's coordinate system - but it's essential for
tasks like picking up an object at a specific point in space.
"""

from time import sleep
import re
from dobot_library.dobot_api import DobotApiDashboard

IP = "192.168.201.1"
dashboard = DobotApiDashboard(IP, 29999)


def parse_pose(response_string):
    """Same idea as parse_angles() in the joint motion example,
    but for reading X/Y/Z/Rx/Ry/Rz values instead of joint angles."""
    match = re.search(r'\{([-\d.,]+)\}', str(response_string))
    if match:
        return [float(x.strip()) for x in match.group(1).split(',')]
    return None


print("Clearing errors and enabling...")
print(dashboard.ClearError())
sleep(0.5)
print(dashboard.EnableRobot())
sleep(1)

print("Setting speed to 20%...")
print(dashboard.SpeedFactor(20))
sleep(0.5)

# Read the current tool position before moving.
current_pose = parse_pose(dashboard.GetPose())
print("Current pose (X, Y, Z, Rx, Ry, Rz):", current_pose)

# MovL(X, Y, Z, Rx, Ry, Rz, mode)
# IMPORTANT: the exact numbers below are just an EXAMPLE. Cartesian
# coordinates depend entirely on your robot's mounting position and
# reference frame - copying these numbers directly into your own
# setup could send the robot somewhere unexpected or unreachable.
# Always start from a position you've read with GetPose() and make
# SMALL adjustments from there while testing.
if current_pose:
    target_x = current_pose[0]
    target_y = current_pose[1]
    target_z = current_pose[2] + 50  # move 50mm straight up, as an example
    rx, ry, rz = current_pose[3], current_pose[4], current_pose[5]

    print(f"\nMoving 50mm straight up from current position...")
    result = dashboard.MovL(target_x, target_y, target_z, rx, ry, rz, 1)
    print(result)
    sleep(3)

    new_pose = parse_pose(dashboard.GetPose())
    print("New pose:", new_pose)

    print("\nReturning to original position...")
    dashboard.MovL(*current_pose, 1)
    sleep(3)
else:
    print("Could not read current pose - skipping movement for safety.")

print("Disabling robot...")
dashboard.DisableRobot()
print("Done!")
