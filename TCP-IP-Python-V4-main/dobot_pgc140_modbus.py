from time import sleep
import struct

class PGC140Gripper:
    """
    PGC-140 Gripper Modbus RTU Control
    Slave Address: 1 (default)
    Baud Rate: 115200
    """
    
    def __init__(self, dashboard):
        self.dashboard = dashboard
        self.slave_id = 1
        
    def _calculate_crc(self, data):
        """Calculate CRC16 for Modbus RTU"""
        crc = 0xFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 1:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc = crc >> 1
        return struct.pack('<H', crc)
    
    def _build_command(self, function_code, register, value=None):
        """Build a Modbus RTU command"""
        if function_code == 0x06:  # Write Single Register
            data = bytes([self.slave_id, function_code])
            data += struct.pack('>HH', register, value)
        else:
            return None
        
        crc = self._calculate_crc(data)
        return data + crc
    
    def initialize(self):
        """Initialize the gripper (0x0100)"""
        print("Initializing gripper...")
        cmd = self._build_command(0x06, 0x0100, 0x0001)
        if cmd:
            result = self.dashboard.SendCmd(cmd)
            print(f"Init result: {result}")
            sleep(3)  # Wait for initialization
            return True
        return False
    
    def set_position(self, position):
        """
        Set gripper position (0-1000 = 0-100%)
        Register: 0x0103
        """
        if not (0 <= position <= 1000):
            print(f"Position must be 0-1000, got {position}")
            return False
        
        print(f"Setting position to {position}...")
        cmd = self._build_command(0x06, 0x0103, position)
        if cmd:
            result = self.dashboard.SendCmd(cmd)
            print(f"Position result: {result}")
            sleep(2)
            return True
        return False
    
    def set_force(self, force):
        """
        Set gripper force (20-100%)
        Register: 0x0101
        """
        if not (20 <= force <= 100):
            print(f"Force must be 20-100, got {force}")
            return False
        
        print(f"Setting force to {force}%...")
        cmd = self._build_command(0x06, 0x0101, force)
        if cmd:
            result = self.dashboard.SendCmd(cmd)
            print(f"Force result: {result}")
            sleep(1)
            return True
        return False
    
    def set_speed(self, speed):
        """
        Set gripper speed (1-100%)
        Register: 0x0104
        """
        if not (1 <= speed <= 100):
            print(f"Speed must be 1-100, got {speed}")
            return False
        
        print(f"Setting speed to {speed}%...")
        cmd = self._build_command(0x06, 0x0104, speed)
        if cmd:
            result = self.dashboard.SendCmd(cmd)
            print(f"Speed result: {result}")
            sleep(1)
            return True
        return False
    
    def open(self):
        """Open gripper to maximum position (1000 = 100%)"""
        print("Opening gripper...")
        self.set_position(1000)
        sleep(2)
    
    def close(self):
        """Close gripper to minimum position (0 = 0%)"""
        print("Closing gripper...")
        self.set_position(0)
        sleep(2)
    
    def grip(self, position=500, force=80, speed=100):
        """Grip with custom parameters"""
        self.set_force(force)
        self.set_speed(speed)
        self.set_position(position)
