"""
RECORD CARTESIAN POINTS - drag, record X/Y/Z positions, and replay
========================================================================

Commands covered in this file:
  - StartDrag() / StopDrag()  hand-guided drag mode
  - GetPose()                 reads X/Y/Z/Rx/Ry/Rz (not joint angles)
  - MovL()                    replays each point in a straight line

HOW THIS DIFFERS FROM 06_drag_record_and_replay.py:
That file recorded and replayed JOINT ANGLES (using GetAngle and
MovJ). This one records and replays CARTESIAN POSITIONS instead
(using GetPose and MovL) - meaning it remembers WHERE something is
in physical space (X/Y/Z coordinates), not which angle each joint
was at.

WHY THIS MATTERS:
If you only care about "put the tool at this exact spot in space",
Cartesian points are usually the more natural way to think about
it - especially for tasks like picking up an object at a specific
location. MovL also travels in a straight line between points,
unlike MovJ.
"""

from time import sleep
import re
from dobot_library.dobot_api import DobotApiDashboard

IP = "192.168.201.1"
dashboard = DobotApiDashboard(IP, 29999)


def parse_pose(response_string):
    """Pulls X, Y, Z, Rx, Ry, Rz out of the robot's reply text."""
    match = re.search(r'\{([-\d.,]+)\}', str(response_string))
    if match:
        return [float(x.strip()) for x in match.group(1).split(',')]
    return None


print("Clearing errors and enabling...")
dashboard.ClearError()
sleep(0.5)
dashboard.EnableRobot()
sleep(1)

print("Setting speed to 40%...")
dashboard.SpeedFactor(40)
sleep(0.5)

recorded_poses = []

confirm = input("Enter drag mode to record Cartesian points? (yes/no): ").strip().lower()

if confirm in ("yes", "y"):
    print("\nEntering drag mode...")
    dashboard.StartDrag()
    sleep(2)

    print("Move the robot to a position, then press ENTER to record it.")
    print("Type 'stop' and press ENTER when you're done.\n")

    while True:
        user_input = input("Press ENTER to record, or type 'stop': ").strip().lower()
        if user_input == "stop":
            break

        pose = parse_pose(dashboard.GetPose())
        if pose:
            recorded_poses.append(pose)
            print(f"Point {len(recorded_poses)} recorded:")
            print(f"  X={pose[0]:.2f}, Y={pose[1]:.2f}, Z={pose[2]:.2f}, "
                  f"Rx={pose[3]:.2f}, Ry={pose[4]:.2f}, Rz={pose[5]:.2f}")
        else:
            print("Could not read a pose - try again.")

    print("\nExiting drag mode...")
    dashboard.StopDrag()
    sleep(2)
else:
    print("Drag mode skipped - no points recorded.")

if recorded_poses:
    print(f"\nReplaying {len(recorded_poses)} recorded points using MovL...")

    dashboard.ClearError()
    sleep(1)
    dashboard.EnableRobot()
    sleep(2)
    dashboard.SpeedFactor(40)
    sleep(0.5)

    for i, pose in enumerate(recorded_poses, start=1):
        print(f"\nMoving to POINT {i}...")
        result = dashboard.MovL(*pose, 1)
        print(result)
        sleep(3)

        actual = parse_pose(dashboard.GetPose())
        if actual:
            print(f"Arrived near: X={actual[0]:.2f}, Y={actual[1]:.2f}, Z={actual[2]:.2f}")

    print(f"\nSequence complete - replayed {len(recorded_poses)} points.")
else:
    print("\nNo points were recorded, nothing to replay.")

print("\nDisabling robot...")
dashboard.DisableRobot()
print("Done!")
