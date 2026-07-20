"""
JOINT MOTION - moving the robot with MovJ()
=============================================

Commands covered in this file:
  - MovJ()      moves using joint-space motion
  - GetAngle()  reads the current angle of every joint
  - SpeedFactor() sets how fast movements happen

JOINT motion means each joint rotates directly towards its target
angle. It does NOT guarantee the tool moves in a straight line
through space - for that, see 03_linear_motion.py (MovL).

Joint motion is the simplest and safest type of movement to start
with, since you're thinking in terms of "rotate this joint to this
angle" rather than 3D coordinates.
"""

from time import sleep
import re
from dobot_library.dobot_api import DobotApiDashboard

IP = "192.168.201.1"
dashboard = DobotApiDashboard(IP, 29999)


def parse_angles(response_string):
    """
    The robot sends its replies back as text, e.g.:
      "0,{30.0000,0.0000,0.0000,0.0000,0.0000,0.0000},GetAngle();"
    This function pulls the six numbers out of that text and
    returns them as a normal Python list of numbers, so we can
    use them in calculations (e.g. current_angles[0] for J1).
    """
    match = re.search(r'\{([-\d.,]+)\}', str(response_string))
    if match:
        return [float(x.strip()) for x in match.group(1).split(',')]
    return None


print("Clearing errors and enabling...")
print(dashboard.ClearError())
sleep(0.5)
print(dashboard.EnableRobot())
sleep(1)

# Always start slow while testing. 100 = full speed, which you
# should only use once you fully trust a script.
print("Setting speed to 20%...")
print(dashboard.SpeedFactor(20))
sleep(0.5)

# Read where the robot currently is before moving anything.
current = parse_angles(dashboard.GetAngle())
print("Current joint angles:", current)

# MovJ(J1, J2, J3, J4, J5, J6, mode)
# The last argument, 1, tells the robot these six numbers are
# JOINT ANGLES in degrees (as opposed to X/Y/Z/Rx/Ry/Rz coordinates,
# which is what MovL uses instead).
print("\nMoving J1 to 30 degrees, all other joints unchanged...")
result = dashboard.MovJ(30, 0, 0, 0, 0, 0, 1)
print(result)
sleep(3)

new_angles = parse_angles(dashboard.GetAngle())
print("New joint angles:", new_angles)

print("\nReturning to all-zero position...")
dashboard.MovJ(0, 0, 0, 0, 0, 0, 1)
sleep(3)

print("Disabling robot...")
dashboard.DisableRobot()
print("Done!")
