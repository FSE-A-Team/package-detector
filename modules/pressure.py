#Start by importing all necessary libraries and packages 
import time
from datetime import datetime
try:
    from modules import mock_smbus
except:
    import mock_smbus
import smbus
import asyncio
import os


#create a sensor object
class Sensor:
    def __init__(self , sms, input_address=[0x40, 0x41, 0x42, 0x43], I2c_address=0x48, test=False):
        '''
        input_address: List of addresses for ADC inputs
        i2c_address: The address of the adc on the i2c bus
        '''
        self.sms = sms
        self.I2c_address = I2c_address
        self.input_address = input_address
        if test:
            self.bus = mock_smbus.SMBus(1)
        else:
            self.bus = smbus.SMBus(1)
        self.package_count = 0
        self.base_value = 0
        self.recorded_weights = [self.base_value]
        self.current_state = 0 # 0: no change, 1: increase, -1: decrease

        self.sleep_interval = 1
        self.new_box_added = False

    def __read_one_sensor(self, input_address=0x40):
        '''
        return just one sensor reading
        '''
        self.bus.write_byte(self.I2c_address, input_address)
        temp = self.bus.read_byte(self.I2c_address)
        return temp
    
    async def __read_all_sensors(self):
        '''
        iterate through input addresses and return average
        '''
        sum = 0
        #os.system('cls' if os.name == 'nt' else 'clear')
        loop = asyncio.get_running_loop()
        for current_input_address in self.input_address:
            if current_input_address == self.input_address[1]: #This is a workaround for only sensor 1 working
              sum += await loop.run_in_executor(None, self.__read_one_sensor, current_input_address)
        return sum #/ len(self.input_address)
    
    async def __get_current_total(self, normalize_delay=6):
        '''
        return the average reading over a period of time (normalize_delay)
        --------------------------------
        normalize_delay: number of seconds used to get average reading
        ''' 
        readings = []
        sleep_time = 0.5
        normalize_delay = int(normalize_delay / sleep_time)
        for i in range(normalize_delay):
            readings.append(await self.__read_all_sensors())
            await asyncio.sleep(sleep_time)
        return int(sum(readings) / len(readings))

    async def __compare_to_last_recorded(self, current_value):
        '''
        compare current value to last recorded value
        '''
        if current_value > sum(self.recorded_weights)+5:
            return 1
        elif current_value < sum(self.recorded_weights)-5:
            return -1
        return 0 #no change

    async def set_added_new_box(self):
        '''
        used to tell the sensor that a new box has been added
        a new box can only be recorded if this is set to True
        '''
        self.new_box_added = True

    async def get_package_count(self):
        '''
        used for external access to package count
        '''
        return self.package_count, self.recorded_weights
    
    async def __record_weight(self, current_value):
        new_package_weight = current_value - sum(self.recorded_weights)
        if new_package_weight > 0: #avoid package removal errors
            self.recorded_weights.append(new_package_weight)
            self.package_count += 1

    async def __remove_weight(self):
        '''
        -Quick and Easy handling-
        If a package is removed, assume all packages are removed
        If weight > base_value, assume it is a single remaining package
        '''
        self.recorded_weights = [self.base_value]
        self.package_count = 0
        current_value = await self.__get_current_total()
        if current_value > self.base_value:
            self.recorded_weights.append(current_value - self.base_value)
            self.package_count += 1

    
    async def run(self):
        
        self.base_value = await self.__get_current_total()
        if self.base_value > 150: self.base_value = 75
        self.recorded_weights = [self.base_value]
        
        while True:
            current_total = await self.__get_current_total()
            self.current_state = await self.__compare_to_last_recorded(current_total)

            if self.new_box_added:
                print(f"current total: {self.package_count} package(s)")
                print(f"current weight: {current_total}")
                print()
            if self.current_state == 1 and self.new_box_added:
                await self.__record_weight(current_total)
                self.new_box_added = False
                print(f"New package weighs: {current_total}!")
                print(f"Total packages: {self.package_count}")
                await self.sms.send_sms_via_email(f'You have {self.package_count} package(s)!')
                print()
            elif self.current_state == -1 and self.package_count > 0:
                await self.__remove_weight()
                if self.package_count == 1:
                    print("Package removed! But there is still at least one package remaining!")
                    await self.sms.send_sms_via_email('You removed a package but there is still at least one package remaining!')
                    print()
                else:
                    print("All packages removed!")
                    await self.sms.send_sms_via_email('All of your packages have been removed!')
                    print()

            await asyncio.sleep(self.sleep_interval)


async def system_test():
    sensor = Sensor()
    pressure_task = asyncio.create_task(sensor.run()) #run the sensor
    dot_count = 0
    dots = ['', '.', '..', '...']
    while True:
        #clear screen
        try:
          os.system('cls' if os.name == 'nt' else 'clear')
          dot_count += 1
          print("Reading Weight", end=f"{dots[dot_count]}\n")
          package_count, recorded_weights = await sensor.get_package_count()
          print(f"Packages: {package_count} \nRecorded Weights: {recorded_weights}")
          if dot_count == 3:
              dot_count = 0
          await asyncio.sleep(.5)
        except KeyboardInterrupt:
          pressure_task.cancel()

#create test if run as main
if __name__ == '__main__':
    asyncio.run(system_test())