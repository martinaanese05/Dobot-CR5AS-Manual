"""
GRIPPER CONTROL - via Lua script (advanced / alternative method)
====================================================================

This example is based on the real approach used in the
"Robot Barman" project. It's more complex than the digital I/O or
Modbus methods, so read the comments carefully.

WHY THIS METHOD EXISTS:
Some grippers are controlled by running a small Lua script that's
stored ON the robot's own controller (not on your PC). To trigger
that script, the robot needs a command sent to it - but there's a
catch: while the Dashboard connection (port 29999) is open in the
normal way, gripper scripts often need to be triggered over a raw
socket connection instead. This means you have to:

  1. CLOSE the existing Dashboard connection (to free up the port)
  2. Open a plain, raw socket connection of your own
  3. Send the command "RunScript(script_name)" directly
  4. Wait for the gripper to physically finish moving
     (its own internal "state machine" needs settling time)
  5. RE-OPEN the Dashboard connection
  6. Re-enable the robot (closing/reopening the dashboard can
     leave the robot refusing to move until you clear errors
     and enable it again)

This looks complicated, but it's really just: "step out of the way,
tell the gripper to do its thing directly, then step back in."

REQUIREMENT: this assumes gripper scripts named "gripper_open" and
"gripper_close" already exist and are saved on the robot controller
itself - this script does NOT create them, only triggers them.
"""

import socket
from time import sleep
from dobot_library.dobot_api import DobotApiDashboard

IP = "192.168.201.1"
PORT = 29999


def run_gripper_script(dashboard, script_name):
    """
    Runs a named Lua script (e.g. "gripper_open") that lives on the
    robot controller, using the close -> raw socket -> reconnect
    pattern described above. Returns the (possibly new) dashboard
    object, since the old connection gets closed and replaced.
    """
    print(f"Running gripper script: {script_name}")

    # Step 1: close the existing Dashboard connection to free the port
    if dashboard:
        try:
            dashboard.close()
        except Exception:
            pass
        sleep(1.0)  # give the OS time to fully release the port

    # Step 2 + 3: open our own raw socket and send the RunScript command
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(5)
        sock.connect((IP, PORT))

        command = f"RunScript({script_name})"
        sock.sendall((command + "\n").encode())
        sleep(1.0)

        try:
            response = sock.recv(1024)
            print("Gripper response:", response.decode().strip())
        except socket.timeout:
            print("No response from gripper (timed out)")

    except Exception as e:
        print(f"Error while running gripper script: {e}")
    finally:
        try:
            sock.close()
        except Exception:
            pass

    # Step 4: give the gripper time to physically finish moving.
    # This delay matters - sending the next command too soon can
    # catch the gripper mid-motion.
    sleep(1.5)

    # Step 5: reconnect the Dashboard
    new_dashboard = DobotApiDashboard(IP, PORT)
    sleep(0.5)

    # Step 6: re-arm the robot for motion. Closing/reopening the
    # dashboard can silently leave MovJ/MovL commands ignored
    # unless you clear errors and re-enable first.
    try:
        new_dashboard.ClearError()
        sleep(0.3)
        new_dashboard.EnableRobot()
        sleep(0.8)
        print("Robot re-enabled after gripper script.")
    except Exception as e:
        print(f"Warning: could not re-enable robot: {e}")

    return new_dashboard


# ---- Main script ----

dashboard = DobotApiDashboard(IP, PORT)

print("Clearing errors and enabling...")
dashboard.ClearError()
sleep(0.5)
dashboard.EnableRobot()
sleep(1)

dashboard = run_gripper_script(dashboard, "gripper_open")
sleep(1)
dashboard = run_gripper_script(dashboard, "gripper_close")

print("\nDisabling robot...")
dashboard.DisableRobot()
print("Done!")
