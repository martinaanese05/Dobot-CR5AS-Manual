"""
INVERSE KINEMATICS - converting X/Y/Z into joint angles
==========================================================

Commands covered in this file:
  - InverseKin()  converts a Cartesian target (X/Y/Z/Rx/Ry/Rz)
                  into the joint angles (J1-J6) needed to reach it

WHY THIS MATTERS:
MovL() and MovJ() both accept Cartesian coordinates or joint
angles depending on the mode flag - but sometimes you want to know
in ADVANCE what joint angles a target position corresponds to,
without actually moving there yet. For example:
  - checking whether a target is even reachable before committing
    to the move
  - comparing joint angles across multiple candidate positions

InverseKin() does the maths for you: give it a target position in
space, and it calculates the matching joint angles.
"""

from time import sleep
import re
from dobot_library.dobot_api import DobotApiDashboard

IP = "192.168.201.1"
dashboard = DobotApiDashboard(IP, 29999)


def parse_values(response_string):
    match = re.search(r'\{([-\d.,]+)\}', str(response_string))
    if match:
        return [float(x.strip()) for x in match.group(1).split(',')]
    return None


print("Clearing errors and enabling...")
print(dashboard.ClearError())
sleep(0.5)
print(dashboard.EnableRobot())
sleep(1)

# Read the robot's current position, just so we have a realistic
# target to test with (nearby, reachable positions).
current_pose = parse_values(dashboard.GetPose())
print("Current pose:", current_pose)

if current_pose:
    # Build an example target: same position, but 30mm higher.
    target = current_pose.copy()
    target[2] += 30  # Z axis, move 30mm up

    # InverseKin(X, Y, Z, Rx, Ry, Rz) - ask the robot "if I wanted
    # to be at THIS position, what joint angles would that need?"
    # NOTE: this does NOT move the robot - it only calculates.
    print(f"\nCalculating joint angles for target: {target}")
    result = dashboard.InverseKin(*target)
    print("Result:", result)

    calculated_angles = parse_values(result)
    if calculated_angles:
        print("Joint angles needed to reach this position:")
        joint_names = ["J1", "J2", "J3", "J4", "J5", "J6"]
        for name, angle in zip(joint_names, calculated_angles):
            print(f"  {name}: {angle:.4f} degrees")
else:
    print("Could not read current pose.")

print("\nDisabling robot...")
dashboard.DisableRobot()
print("Done!")
