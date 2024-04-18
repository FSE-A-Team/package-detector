import random
import time

class SMBus:
    def __init__(self, bus):
        # Simulate bus number, not used in mock
        self._bus = bus
        self._last_time = time.time()
        self._current_pressure = self._generate_initial_pressure()

    def _generate_initial_pressure(self):
        # Initialize with a random pressure value
        return random.randint(0, 255)

    def write_byte(self, addr, value):
        # Simulate writing a byte to a device at addr
        #print(f"Mock write to {addr}: {value}")
        pass

    def read_byte(self, addr):
        # Simulate reading a byte from a device at addr and reg
        current_time = time.time()
        if current_time - self._last_time > 10:
            self._current_pressure = self._generate_pressure_change()
            self._last_time = current_time
        return self._current_pressure

    def _generate_pressure_change(self):
        # Change pressure randomly to simulate sensor output
        return random.randint(0, 255)