from servo import Servo
from time import sleep

class Arms:
    closed_value = 0.9
    open_value = 0.4
    __percent = 0.4
    
    def __init__(self, pin):
        self.s = Servo(pin)
        
    def enable(self):
        self.s.enable()
    
    def disable(self):
        self.s.disable()
    
    def open_arms(self):
        self.__percent = self.open_value
        self.s.to_percent(self.open_value)
        
    def close_arms(self):
        self.__percent = self.closed_value
        self.s.to_percent(self.closed_value)
        
    def to_percent(self, percent):
        self.__percent = percent
        self.s.to_percent(percent)
        
    def swoop_arms(self, duration, start, finish):
            
        for i in range(int(start*1000), int(finish*1000),1):
            self.s.to_percent(i/1000)
            sleep(duration/1000)
        
    @property
    def percent(self):
        return self.__percent
    