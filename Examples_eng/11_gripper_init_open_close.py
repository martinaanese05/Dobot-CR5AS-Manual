"""
GRIPPER: INITIALIZE, OPEN, CLOSE - based on the Robot Barman project
=========================================================================

This example mirrors exactly how the gripper is controlled in the
Robot Barman project - three named Lua scripts stored on the robot
controller ("gripper_init", "gripper_open", "gripper_close"), each
triggered the same way: close the Dashboard, send the script over a
raw socket, wait, then reconnect the Dashboard.

WHY "INITIALIZE" IS A SEPARATE STEP:
Some grippers need a one-time initialization/homing routine before
they'll respond reliably to open/close commands - similar to how a
3D printer homes its axes before printing. In Robot Barman, this is
run once at the start of a session (`gripper_init`), before any
open/close commands are sent.

IMPORTANT LESSON FROM ROBOT BARMAN (the trickiest part of this):
Every time a gripper script runs, the Dashboard connection gets
closed and reopened behind the scenes. This can silently leave the
robot in a state where MovJ/MovL commands are IGNORED, even though
nothing looks wrong. The fix used throughout Robot Barman is to
always call ClearError() + EnableRobot() again immediately after
any gripper action, before trying to move the arm. This example
follows that same safety pattern.

REQUIREMENT: this assumes "gripper_init", "gripper_open", and
"gripper_close" scripts already exist on your robot controller.
This script only triggers them, it does not create them.
"""

import socket
from time import sleep
from dobot_library.dobot_api import DobotApiDashboard

IP = "192.168.201.1"
PORT = 29999


def run_gripper_script(dashboard, script_name):
    """
    Runs a named Lua script stored on the robot controller.
    Returns a (possibly new) dashboard object, since the connection
    gets closed and recreated as part of this process.
    """
    print(f"Running gripper script: {script_name}")

    # Step 1: close the current Dashboard connection to free the port
    if dashboard:
        try:
            dashboard.close()
        except Exception:
            pass
        sleep(1.0)

    # Step 2: open a raw socket and send the RunScript command directly
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(5)
        sock.connect((IP, PORT))

        sock.sendall((f"RunScript({script_name})\n").encode())
        sleep(1.0)

        try:
            response = sock.recv(1024)
            print("Gripper response:", response.decode().strip())
        except socket.timeout:
            print("No response from gripper (timed out)")
    except Exception as e:
        print(f"Error running gripper script: {e}")
    finally:
        try:
            sock.close()
        except Exception:
            pass

    # Step 3: reconnect the Dashboard
    new_dashboard = DobotApiDashboard(IP, PORT)
    sleep(0.5)
    return new_dashboard


def ensure_motion_ready(dashboard):
    """
    Re-arms the robot for movement after a gripper script has run.
    This is the critical step Robot Barman relies on - without it,
    the gripper appears to work, but the arm silently ignores any
    MovJ/MovL commands sent afterwards.
    """
    try:
        dashboard.ClearError()
        sleep(0.5)
        dashboard.EnableRobot()
        sleep(1)
        print("Arm re-armed for motion (errors cleared, robot enabled)")
    except Exception as e:
        print(f"Warning: could not re-arm robot for motion: {e}")


# ---- Main script ----

dashboard = DobotApiDashboard(IP, PORT)

print("Clearing errors and enabling...")
dashboard.ClearError()
sleep(0.5)
dashboard.EnableRobot()
sleep(1)

# PHASE 1: Initialize the gripper (one-time, at the start of a session)
print("\nInitializing gripper...")
dashboard = run_gripper_script(dashboard, "gripper_init")
sleep(5)  # gripper_init needs time to fully complete before anything else

# The gripper scripts close/reopen the Dashboard - always re-arm the
# robot for motion afterwards, even if you're not moving yet.
ensure_motion_ready(dashboard)

# PHASE 2: Close the gripper
print("\nClosing gripper...")
dashboard = run_gripper_script(dashboard, "gripper_close")
ensure_motion_ready(dashboard)

sleep(3)

# PHASE 3: Opem the gripper
print("\nOpening gripper...")
dashboard = run_gripper_script(dashboard, "gripper_open")
ensure_motion_ready(dashboard)

print("\nDisabling robot...")
dashboard.DisableRobot()
print("Done!")
