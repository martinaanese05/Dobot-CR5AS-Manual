"""
INTERACTIVE JOINT JOG - a simple menu to move one joint at a time
=====================================================================

Commands covered in this file:
  - GetAngle()  reads all six joint angles
  - MovJ()      moves the robot (used here for a single joint)

WHAT THIS SCRIPT DOES:
Instead of hardcoding a sequence of moves, this script asks YOU,
in a loop, which joint to move and where. It's a small building
block for anything you want to make interactive later - e.g. a
custom jog panel, a manual positioning tool, or a way to explore
the robot's range of motion safely, one joint at a time.

Each time through the loop it:
  1. Reads and displays the current position of all six joints
  2. Asks which joint (1-6) you want to move
  3. Asks what angle to move it to
  4. Asks for confirmation before actually moving
  5. Moves only that joint, leaving the other five untouched
Type 'quit' at the joint prompt to exit.
"""

from time import sleep
import re
from dobot_library.dobot_api import DobotApiDashboard

IP = "192.168.201.1"
dashboard = DobotApiDashboard(IP, 29999)


def parse_angles(response_string):
    match = re.search(r'\{([-\d.,]+)\}', str(response_string))
    if match:
        return [float(x.strip()) for x in match.group(1).split(',')]
    return None


print("Clearing errors and enabling...")
dashboard.ClearError()
sleep(0.5)
dashboard.EnableRobot()
sleep(1)

print("Setting speed to 50%...")
dashboard.SpeedFactor(50)
sleep(0.5)

print("\nInteractive Joint Jog")
print("Enter a joint number (1-6) to move it, or 'quit' to exit.\n")

while True:
    # Always re-read the current position each loop, since the
    # robot may have moved since we last checked.
    current_angles = parse_angles(dashboard.GetAngle())
    if current_angles is None:
        print("Could not read joint angles - stopping.")
        break

    print("\nCurrent joint positions:")
    for i in range(6):
        print(f"  J{i+1}: {current_angles[i]:.4f}°")

    user_input = input("\nWhich joint do you want to move? (1-6, or 'quit'): ").strip().lower()

    if user_input in ("quit", "exit"):
        break

    # Validate the joint number
    try:
        joint_num = int(user_input)
        if joint_num < 1 or joint_num > 6:
            print("Please enter a number between 1 and 6.")
            continue
    except ValueError:
        print("Please enter a number between 1 and 6.")
        continue

    # Ask for the target angle
    target_input = input(f"Move J{joint_num} to what angle (degrees)? ").strip()
    try:
        target_angle = float(target_input)
    except ValueError:
        print("Please enter a valid number.")
        continue

    # Confirm before moving - always good practice for anything
    # driven by live user input rather than a fixed script.
    confirm = input(f"Move J{joint_num} to {target_angle}°? (yes/no): ").strip().lower()
    if confirm not in ("yes", "y"):
        print("Movement cancelled.")
        continue

    # Build the full six-angle command, changing only the one
    # joint the user picked and leaving the rest at their current
    # positions.
    move_angles = current_angles.copy()
    move_angles[joint_num - 1] = target_angle

    print(f"\nMoving J{joint_num}...")
    result = dashboard.MovJ(*[float(a) for a in move_angles], 1)
    print(result)
    sleep(3)

print("\nDisabling robot...")
dashboard.DisableRobot()
print("Done!")
