"""
DRAG, RECORD, AND REPLAY - teaching the robot a sequence of points
======================================================================

Commands covered in this file:
  - StartDrag() / StopDrag()  enter and exit hand-guided drag mode
  - GetAngle()                reads joint angles at each recorded point
  - MovJ()                    replays each recorded point in order

WHAT THIS SCRIPT DOES:
  1. Moves to the home position (all joints at 0)
  2. Puts the robot into drag mode, so you can move it by hand
  3. Each time you press ENTER, it records the CURRENT joint
     angles as a "point" in a list
  4. When you type "stop", it exits drag mode
  5. It then replays every recorded point, in order, automatically
  6. Finally, it returns to home

WHY THIS IS USEFUL:
This is how you "teach" the robot a sequence of positions without
writing down coordinates yourself - you physically show it where
to go, and the script remembers. This is the same technique used
to build things like pick-and-place routines: drag to each
position once, then let the script repeat it forever.

SAFETY NOTE: even in drag mode, the robot is powered on. Keep the
workspace clear and the e-stop within reach while dragging it by
hand.
"""

from time import sleep
import re
from dobot_library.dobot_api import DobotApiDashboard

IP = "192.168.201.1"
dashboard = DobotApiDashboard(IP, 29999)


def parse_angles(response_string):
    """Pulls the six joint angle numbers out of the robot's reply text."""
    match = re.search(r'\{([-\d.,]+)\}', str(response_string))
    if match:
        return [float(x.strip()) for x in match.group(1).split(',')]
    return None


def move_to_angles(angles, label="position"):
    """Sends a MovJ command to the given joint angles, waits for it
    to finish, then prints where the robot actually ended up."""
    print(f"\nMoving to {label}...")
    result = dashboard.MovJ(*angles, 1)
    print(result)
    sleep(3)  # crude wait - good enough for teaching purposes

    current = parse_angles(dashboard.GetAngle())
    if current:
        print(f"Arrived at {label}:")
        for i in range(6):
            print(f"  J{i+1}: {current[i]:.4f}°")


# ---------------------------------------------------------------
# STEP 1: Start from a known position
# ---------------------------------------------------------------
print("Clearing errors and enabling...")
dashboard.ClearError()
sleep(0.5)
dashboard.EnableRobot()
sleep(1)

print("Setting speed to 50%...")
dashboard.SpeedFactor(50)
sleep(0.5)

move_to_angles([0, 0, 0, 0, 0, 0], label="HOME position")


# ---------------------------------------------------------------
# STEP 2: Enter drag mode and record points
# ---------------------------------------------------------------
recorded_points = []

confirm = input("\nEnter drag mode to record points? (yes/no): ").strip().lower()

if confirm in ("yes", "y"):
    print("\nEntering drag mode - the robot will go loose and can be moved by hand.")
    print(dashboard.StartDrag())
    sleep(2)

    print("\nMove the robot to a position, then press ENTER to record it.")
    print("Type 'stop' and press ENTER when you're done recording.\n")

    while True:
        user_input = input("Press ENTER to record, or type 'stop': ").strip().lower()

        if user_input == "stop":
            break

        angles = parse_angles(dashboard.GetAngle())
        if angles:
            recorded_points.append(angles)
            print(f"Point {len(recorded_points)} recorded:")
            for i in range(6):
                print(f"  J{i+1}: {angles[i]:.4f}°")
        else:
            print("Could not read a position - try again.")

    print("\nExiting drag mode...")
    print(dashboard.StopDrag())
    sleep(2)
else:
    print("Drag mode skipped - no points recorded.")


# ---------------------------------------------------------------
# STEP 3: Replay the recorded sequence
# ---------------------------------------------------------------
if recorded_points:
    print(f"\nReplaying {len(recorded_points)} recorded points...")

    # After drag mode, the robot sometimes needs to be re-enabled
    # before it will accept movement commands again.
    dashboard.ClearError()
    sleep(1)
    dashboard.EnableRobot()
    sleep(2)
    dashboard.SpeedFactor(50)
    sleep(0.5)

    move_to_angles([0, 0, 0, 0, 0, 0], label="HOME position")

    for i, point in enumerate(recorded_points, start=1):
        move_to_angles(point, label=f"POINT {i}")

    move_to_angles([0, 0, 0, 0, 0, 0], label="HOME position")

    print(f"\nSequence complete - replayed {len(recorded_points)} points.")
else:
    print("\nNo points were recorded, nothing to replay.")

print("\nDisabling robot...")
dashboard.DisableRobot()
print("Done!")