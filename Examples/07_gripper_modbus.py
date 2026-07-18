"""
GRIPPER CONTROL - via Modbus RTU (e.g. DH Robotics PGC-140-50)
=================================================================

Commands covered in this file:
  - ModbusRTUCreate()  opens a Modbus RTU connection to the gripper
  - ModbusClose()      closes that Modbus connection
  - SetToolPower()     powers the tool connector
  - ToolDOInstant()    still used here to trigger open/close, on
                       top of the Modbus connection

WHY MODBUS INSTEAD OF SIMPLE DIGITAL I/O:
Some "smarter" grippers (like the DH Robotics PGC-140-50 used here)
communicate over Modbus RTU, a common industrial serial protocol.
This lets the robot exchange more detailed information with the
gripper (e.g. current grip force, position feedback) rather than
just a simple on/off signal.

Reminder from the Connectivity section: in Modbus, the robot is
always the SLAVE - here, we're using the robot to bridge a Modbus
connection specifically to talk to the gripper, which is a
slightly different relationship than the robot's main TCP/IP
control connection.
"""

from time import sleep
from dobot_library.dobot_api import DobotApiDashboard

IP = "192.168.201.1"
dashboard = DobotApiDashboard(IP, 29999)
GRIPPER_OUTPUT = 1

print("Clearing errors and enabling...")
print(dashboard.ClearError())
sleep(0.5)
print(dashboard.EnableRobot())
sleep(1)

print("Turning on tool power...")
dashboard.SetToolPower(1)
sleep(1)

# ModbusRTUCreate(slave_id, baud_rate, parity, data_bits, stop_bits)
# These settings need to match whatever your specific gripper
# expects - check its manual. The values below (slave ID 1, 9600
# baud, no parity, 8 data bits, 1 stop bit) are common defaults for
# the DH Robotics PGC-140-50.
print("\nSetting up Modbus RTU connection to the gripper...")
try:
    result = dashboard.ModbusRTUCreate(1, 9600, 'N', 8, 1)
    print("Modbus connection result:", result)
except Exception as e:
    print(f"Error creating Modbus connection: {e}")


def open_gripper():
    print("Opening gripper...")
    dashboard.ToolDOInstant(GRIPPER_OUTPUT, 1)
    sleep(1.5)  # Grippers often need a moment to physically move


def close_gripper():
    print("Closing gripper...")
    dashboard.ToolDOInstant(GRIPPER_OUTPUT, 0)
    sleep(1.5)


open_gripper()
sleep(1)
close_gripper()

# Always close the Modbus connection when finished with it.
print("\nClosing Modbus connection...")
dashboard.ModbusClose(0)

print("Turning off tool power...")
dashboard.SetToolPower(0)

print("Disabling robot...")
dashboard.DisableRobot()
print("Done!")
