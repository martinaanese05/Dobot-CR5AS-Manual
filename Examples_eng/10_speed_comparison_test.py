"""
SPEED COMPARISON TEST - seeing SpeedFactor's effect directly
================================================================

Commands covered in this file:
  - SpeedFactor()  sets the global speed percentage
  - MovJ()         moves the robot
  - GetAngle()     confirms where the robot ended up

WHAT THIS SCRIPT DOES:
Runs the exact same move - joint 1 (the base) from 0° to 180° -
at five different speed settings in a row: 10%, 25%, 50%, 75%, and
100%. Between each one, it returns to 0° first, so every test
starts from the same place.

WHY THIS IS USEFUL:
SpeedFactor is easy to read about but hard to understand until you
SEE it - this script lets you directly watch (and time, if you
add a stopwatch) how the same move feels at different speeds. This
is also a good script to use when tuning a new script's speed
before deciding what value to hardcode elsewhere.

SAFETY NOTE: 100% speed is included here for comparison, but running
unfamiliar motions at full speed is not recommended in general. Make
sure the workspace is completely clear before running this file.
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

speeds_to_test = [10, 25, 50, 75, 100]

for speed in speeds_to_test:
    print(f"\n{'='*50}")
    print(f"Testing speed: {speed}%")
    print(f"{'='*50}")

    dashboard.SpeedFactor(speed)
    sleep(1)

    # Always start each test from the same position (0 degrees),
    # so the comparison between speeds is fair.
    print("Moving J1 to 0°...")
    dashboard.MovJ(0, 0, 0, 0, 0, 0, 1)
    sleep(3)

    start_angles = parse_angles(dashboard.GetAngle())
    print(f"Start position: J1 = {start_angles[0]:.4f}°")

    print(f"Moving J1 to 180° at {speed}% speed...")
    dashboard.MovJ(180, 0, 0, 0, 0, 0, 1)
    sleep(5)  # generous wait, since slower speeds take longer

    end_angles = parse_angles(dashboard.GetAngle())
    print(f"End position: J1 = {end_angles[0]:.4f}°")
    print(f"Speed {speed}% complete.")

# Return to a safe, known position when finished.
print("\nReturning J1 to 0°...")
dashboard.SpeedFactor(50)
sleep(0.5)
dashboard.MovJ(0, 0, 0, 0, 0, 0, 1)
sleep(3)

print("\nDisabling robot...")
dashboard.DisableRobot()
print("Done!")
