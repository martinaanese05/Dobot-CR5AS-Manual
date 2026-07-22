from time import sleep
from dobot_api import DobotApiDashboard
from dobot_pgc140_modbus import PGC140Gripper

IP = "192.168.201.1"
dashboard = DobotApiDashboard(IP, 29999)

print("Connecting...")
print(dashboard.ClearError())
sleep(0.5)

print("Enabling robot...")
print(dashboard.EnableRobot())
sleep(1)

print("Enabling tool power...")
print(dashboard.SetToolPower(1))
sleep(1)

# Create gripper controller
gripper = PGC140Gripper(dashboard)

print("\n" + "="*40)
print("PGC-140 CONTROL TEST")
print("="*40 + "\n")

# Initialize
gripper.initialize()

print("\nTest sequence:")
print("1. Opening...")
gripper.open()
sleep(2)

print("\n2. Closing...")
gripper.close()
sleep(2)

print("\n3. Half position...")
gripper.set_position(500)
sleep(2)

print("\nTest complete!")

print("\nShutting down...")
dashboard.SetToolPower(0)
dashboard.DisableRobot()
print("Done!")
