#Start by importing all necessary libraries and packages 
import time
from datetime import datetime
import smbus
import asyncio
import os


#create a sensor object
class Sensor:
    def __init__(self , input_address=[0x40, 0x41, 0x42, 0x43], I2c_address=0x48):
        '''
        input_address: List of addresses for ADC inputs
        i2c_address: The address of the adc on the i2c bus
        '''
        self.I2c_address = I2c_address
        self.input_address = input_address
        self.bus = smbus.SMBus(1)
        self.package_count = 0
        self.base_value = self.__get_current_total()
        self.recorded_weights = [self.base_value]
        self.current_state = 0 # 0: no change, 1: increase, -1: decrease

        self.interval = 1
        self.last_time_weight_changed = time.time()

    def __read_one_sensor(self, input_address=0x40):
        '''
        return just one sensor reading
        '''
        #return datetime.now().second #for testing
        self.bus.write_byte(self.I2c_address, input_address)
        return self.bus.read_byte(self.I2c_address)
    
    def __read_all_sensors(self):
        '''
        iterate through input addresses and return average
        '''
        sum = 0
        for current_input_address in self.input_address:
            sum += self.__read_one_sensor(current_input_address)
        return sum / len(self.input_address)
    
    def __get_current_total(self, normalize_delay=6):
        '''
        return the average reading over a period of time (normalize_delay)
        --------------------------------
        normalize_delay: number of seconds used to get average reading
        ''' 
        readings = []
        sleep_time = 0.25
        normalize_delay = int(normalize_delay / sleep_time)
        for i in range(normalize_delay):
            readings.append(self.__read_all_sensors())
            time.sleep(sleep_time)
        return int(sum(readings) / len(readings))

    def __compare_to_last_recorded(self, current_value):
        '''
        compare current value to last recorded value
        '''
        if current_value > sum(self.recorded_weights)+5:
            return 1
        elif current_value < sum(self.recorded_weights)-5:
            return -1
        return 0 #no change

    async def get_package_count(self):
        '''
        used for external access to package count
        '''
        return self.package_count, self.recorded_weights
    
    def __record_weight(self, current_value):
        new_package_weight = current_value - sum(self.recorded_weights)
        if new_package_weight > 0: #avoid package removal errors
            self.recorded_weights.append(new_package_weight)
            self.package_count += 1

    def __remove_weight(self):
        '''
        -Quick and Easy handling-
        If a package is removed, assume all packages are removed
        If weight > base_value, assume it is a single remaining package
        '''
        self.recorded_weights = [self.base_value]
        self.package_count = 0
        current_value = self.__get_current_total()
        if current_value > self.base_value:
            self.recorded_weights.append(current_value - self.base_value)
            self.package_count += 1

    
    async def run(self):

        while True:
            current_total = self.__get_current_total()
            self.current_state = self.__compare_to_last_recorded(current_total)
            if self.current_state == 1:
                self.__record_weight(current_total)
            elif self.current_state == -1:
                self.__remove_weight()

            await asyncio.sleep(self.interval)


#create test if run as main
if __name__ == '__main__':
    #sensor = Sensor()
    #asyncio.run(sensor.run()) #run the sensor
    dot_count = 0
    dots = ['.', '..', '...', '....']
    while True:
        #clear screen
        os.system('cls' if os.name == 'nt' else 'clear')
        dot_count += 1
        print("Reading Weight", end=f"{dots[dot_count]}\n")
        #print(f"Packages: {sensor.package_count} \nRecorded Weights: {sensor.recorded_weights}")
        if dot_count == 4:
            dot_count = 0
        time.sleep(.5)