from servo import Servo
from time import sleep
import math

s = Servo(0)

UPDATES = 50            # How many times to udpate the servo per second
TIME_FOR_EACH_MOVE = 2  # The time to travel between each movement
UPDATES_PER_MOVE = TIME_FOR_EACH_MOVE * UPDATES
START_POSITION = 0.9
END_POSITION = 0.4



print(s.pin())
s.enable()

start_value = 0.9
end_value = 0.4

print(f'Start Value: {start_value}, End Value: {end_value}')


update = 0
direction = False
while True or KeyboardInterrupt:
    
    # calculate how far along this movement is to be
    percent_along = update / UPDATES_PER_MOVE
    
    #s.to_percent(math.cos(percentage_along * math.pi), 1.0, -1.0, start_value, end_value)
    calc = percent_along
    s.to_percent(calc)
    
    
    print(f'Value = {round(s.value(),3)}')
    if not direction:
        update += 1
    else:
        update -= 1
    
    if update >= UPDATES_PER_MOVE:
        # reset the counter
        update = 0
        if direction:
            direction = False
            start_value = END_POSITION
            end_value = START_POSITION
        else:
            direction = True
            start_value = START_POSITION
            end_value = END_POSITION
        
    sleep(1.0 / UPDATES)
s.disable()
