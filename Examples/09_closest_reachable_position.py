"""
MOVE TO CLOSEST REACHABLE POSITION - handling unreachable targets
======================================================================

Commands covered in this file:
  - MovL()    attempts a straight-line move to a Cartesian target
  - GetPose() reads the current X/Y/Z/Rx/Ry/Rz position

THE PROBLEM THIS SOLVES:
Not every X/Y/Z coordinate you can type is actually reachable - the
robot has a limited working radius, and some positions are outside
it, or awkward angles the arm physically can't achieve. If you send
an unreachable target with MovL(), the robot will simply reject the
command and stay where it is.

THIS SCRIPT'S APPROACH:
Rather than giving up on the first failure, it tries the target,
and if that fails, backs off step by step - first lowering Z
(height), then Y, then X - retrying each time, until it either
finds a position the robot CAN reach, or gives up after a set
number of attempts.

This is a simple, "good enough" strategy - it does not guarantee
the absolute closest reachable point, just a nearby one found by
trial and error. For applications where "closest" needs to be
mathematically precise, you'd want proper kinematics-based
reachability checking instead.
"""

from time import sleep
import re
from dobot_library.dobot_api import DobotApiDashboard

IP = "192.168.201.1"
dashboard = DobotApiDashboard(IP, 29999)


def parse_pose(response_string):
    match = re.search(r'\{([-\d.,]+)\}', str(response_string))
    if match:
        return [float(x.strip()) for x in match.group(1).split(',')]
    return None


def try_position(x, y, z, rx, ry, rz, step_size=10, max_attempts=20):
    """
    Attempts to move to (x, y, z). If the move fails, backs off in
    Z, then Y, then X, in small steps, and tries again - up to
    max_attempts times.

    Returns (success, final_x, final_y, final_z) - the position it
    actually ended up trying, whether or not it succeeded.
    """
    current_x, current_y, current_z = x, y, z

    for attempt in range(max_attempts):
        result = dashboard.MovL(current_x, current_y, current_z, rx, ry, rz, 1)
        result_str = str(result)

        # A result starting with "0," generally means success.
        # Anything else usually indicates the move was rejected.
        if result_str.startswith("0,"):
            print(f"  Success at X={current_x:.1f}, Y={current_y:.1f}, Z={current_z:.1f}")
            sleep(3)
            return True, current_x, current_y, current_z

        print(f"  Unreachable at X={current_x:.1f}, Y={current_y:.1f}, Z={current_z:.1f}, backing off...")

        # Try lowering Z first (usually the most flexible axis),
        # then Y, then X, until we run out of room to back off.
        if current_z > 50:
            current_z -= step_size
        elif current_y > 0:
            current_y -= step_size
        elif current_x > 100:
            current_x -= step_size
        else:
            print("  Ran out of room to back off - giving up.")
            break

        sleep(0.5)

    return False, current_x, current_y, current_z


print("Clearing errors and enabling...")
dashboard.ClearError()
sleep(0.5)
dashboard.EnableRobot()
sleep(1)

print("Setting speed to 40%...")
dashboard.SpeedFactor(40)
sleep(0.5)

print("\nMoving to HOME position...")
dashboard.MovJ(0, 0, 0, 0, 0, 0, 1)
sleep(3)

current_pose = parse_pose(dashboard.GetPose())
if current_pose:
    print(f"Current position: X={current_pose[0]:.2f}, Y={current_pose[1]:.2f}, Z={current_pose[2]:.2f}")

print("\nEnter target X Y Z coordinates, 'home' to return home, or 'quit' to exit.\n")

while True:
    user_input = input("Target (X Y Z), or command: ").strip().lower()

    if user_input in ("quit", "exit"):
        break

    if user_input == "home":
        print("Moving to HOME...")
        dashboard.MovJ(0, 0, 0, 0, 0, 0, 1)
        sleep(3)
        continue

    coords = user_input.split()
    if len(coords) != 3:
        print("Please enter exactly 3 values: X Y Z")
        continue

    try:
        target_x, target_y, target_z = (float(c) for c in coords)
    except ValueError:
        print("Please enter valid numbers.")
        continue

    print(f"\nAttempting to reach X={target_x:.1f}, Y={target_y:.1f}, Z={target_z:.1f}...")
    success, final_x, final_y, final_z = try_position(target_x, target_y, target_z, 0, 0, 0)

    if success:
        print(f"Reached target (or exact match): X={final_x:.1f}, Y={final_y:.1f}, Z={final_z:.1f}")
    else:
        print(f"Could not reach target. Best attempt was: X={final_x:.1f}, Y={final_y:.1f}, Z={final_z:.1f}")

print("\nMoving to HOME...")
dashboard.MovJ(0, 0, 0, 0, 0, 0, 1)
sleep(3)

print("Disabling robot...")
dashboard.DisableRobot()
print("Done!")
