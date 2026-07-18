# Dobot CR5AS - Example Scripts

## How to use these examples

1. Download and unzip this whole `Examples` folder - keep the
   `dobot_library` subfolder inside it, in the same place. The
   example scripts import from it directly, so they won't work
   if it's moved elsewhere or deleted.
2. Open any example file and change the `IP` variable near the top
   to match your own robot's IP address.
3. Run the file you're interested in (e.g. `python 00_hello_world.py`).

## Folder contents

| File | What it teaches |
|---|---|
| `00_hello_world.py` | The basic shape of every script: connect, enable, move, disable. Moves all joints to 0, then the base joint to -30°, +30°, +30°. |
| `01_connect_and_status.py` | EnableRobot, DisableRobot, ClearError, RobotMode |
| `02_joint_motion.py` | MovJ, GetAngle, SpeedFactor |
| `03_linear_motion_and_pose.py` | MovL, GetPose |
| `04_drag_mode.py` | StartDrag, StopDrag |
| `05_inverse_kinematics.py` | InverseKin |
| `06_gripper_digital_io.py` | SetToolPower, ToolDOInstant, GetToolDO |
| `07_gripper_modbus.py` | ModbusRTUCreate, ModbusClose (for grippers like the DH Robotics PGC-140-50) |
| `08_gripper_lua_script.py` | Alternative gripper method: running a Lua script stored on the robot controller |

## dobot_library/

This folder contains the official Dobot TCP-IP-Python-V4 library
(`dobot_api.py`), unmodified, from:
https://github.com/Dobot-Arm/TCP-IP-Python-V4

All example scripts import from it like this:
```python
from dobot_library.dobot_api import DobotApiDashboard
```

## A note on safety

Every example here starts slow (20% speed) and expects a clear,
supervised workspace. Always keep the emergency stop within reach
before running any script that moves the robot - see the Safety
Protocols section of this manual.
