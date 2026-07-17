from stepper import Stepper
import time
import machine
from machine import Pin
from random import randint
import micropython
from servo import Servo
from math import sin, cos
import random
import sys
from collections import deque 
from time import ticks_us, ticks_diff

def deinit(pin=1):
    pen_up()
    
    x_axis.stop()
    y_axis.stop()

    en.value(1)
    time.sleep_ms(300)
    machine.soft_reset()


def irq_handler(pin=1):
    print("STOP")

    micropython.schedule(deinit, None)


# Allocate buffer in case of crash - doesn't seem to help but there's no harm
micropython.alloc_emergency_exception_buf(100)

# Kill switch - force reboots
e_stop = Pin(13, Pin.IN, Pin.PULL_UP)

e_stop.irq(trigger=machine.Pin.IRQ_RISING, handler=irq_handler)

y_axis = Stepper(
    18, 19, steps_per_rev=3200, speed_sps=5000, timer_id=1, invert_dir=True
)
x_axis = Stepper(
    16, 21, steps_per_rev=3200, speed_sps=5000, timer_id=0, invert_dir=True
)

# Down: 0
# Up: 30

srv = Servo(pin_id=25)

# Enable low = on, enable high = off
en = Pin(17, Pin.OUT)

end_swy = Pin(15, Pin.IN, Pin.PULL_UP)
end_swx = Pin(4, Pin.IN, Pin.PULL_UP)

def pen_up():
    srv.write(40)
    time.sleep_ms(100)

def pen_down():
    srv.write(0)
    time.sleep_ms(100)

x_pos = 0
y_pos = 0
speed = 5000

def home():
    en.value(0)
    pen_up()
    # X axis
    x_axis.speed(500) #use low speed for the calibration
    x_axis.free_run(-1)
    while end_swx.value(): #wait till the switch is triggered
        time.sleep_ms(1)
    x_axis.stop() #stop as soon as the switch is triggered
    
    y_axis.speed(500) #use low speed for the calibration
    y_axis.free_run(-1)
    while end_swy.value(): #wait till the switch is triggered
        time.sleep_ms(1)
    y_axis.stop() #stop as soon as the switch is triggered
    
    move (100, 100)
    x_pos = 100
    y_pos = 100



@micropython.native
def move(t_x, t_y):
    # Increase speed in hundredths of the original speed
    speed_add_amount = speed // 25
    cur_speed = speed_add_amount
    
    global x_pos
    global y_pos
    
    # Steps needed 
    sn_x = abs(t_x - x_pos)
    sn_y = abs(t_y - y_pos)
    # More steps needed in x (or the same, but that doesn't change anything
    if sn_x >= sn_y:
        sn = sn_x
    else:
        sn = sn_y
        
    # Short line - set to full speed
    if sn < 100:
        cur_speed = speed
    sn = 1000
        
    # Steps taken
    st = 0
    
    if t_x > 15000 or t_y > 16000 or t_x < 0 or t_y < 0:
        return
    # XY0 = Old
    # XY1 = New
    # Draw point from xy0 to xy1
    
    # Distance from x0 to x1
    dx = abs(x_pos - t_x)
    # Sign value
    if x_pos < t_x:
        sx = 1
    else:
        sx = -1
        
    # Distance from y0 to y1    
    dy = -abs(y_pos - t_y)
    # Sign value
    if y_pos < t_y:
        sy = 1
    else:
        sy = -1
    error = dx + dy
    
    next_step_time = ticks_us()
    
    while True:
        # At the target
        if x_pos == t_x and y_pos == t_y:
            break
        e2 = 2 * error
        step_x = 0
        step_y = 0
        
        if e2 >= dy:
            if x_pos == t_x:
                break
            error += dy
            x_pos += sx
            step_x += sx
        
        if e2 <= dx:
            if y_pos == t_y:
                break
            error += dx
            y_pos += sy
            step_y += sy
        
        # Wait 200us - we have to do this as the instructions may take a few us, which would make things slower
        while ticks_diff(next_step_time, ticks_us()) > 0:
            pass
        
        # Still at the start
        if cur_speed < speed:
            cur_speed += speed_add_amount
        # We're approaching the end - 25 steps to go
        elif sn - st <= 25:
            cur_speed -= speed_add_amount
            
            
        next_step_time += (1_000_000 // cur_speed)
        
        st += 1
        
        
        if step_x != 0:
            x_axis.step(step_x)
        if step_y != 0:
            y_axis.step(step_y)
        

def main():
    global speed

    cur_x = 0
    cur_y = 0
    pen_up()
    en.value(0)
    home()
    print("NEXT")
    while True:
        command = sys.stdin.readline()

        if not command:  # EOF
            break
    
        print("NEXT")
      
       
        
        # Remove trailing newcommand
        command = command.strip().upper()
        if not command:
            print("NEXT")
            continue
        command = command.split(" ")
        
        if command[0] == "MOVE":
            new_x = int(command[1])
            new_y = int(command[2])
            move(new_x, new_y)
            
        elif command[0] == "PEN":
            if command[1] == "DOWN":
                pen_down()
            elif command[1] == "UP":
                pen_up()
            else:
                print("INVALID COMMAND: " + line)

        elif command[0] == "SPEED":
            # Min speed 100
            if speed >= 100:
                speed = int(command[1])
        elif command[0] == "HOME":
            x_pos = 0
            y_pos = 0
            home()
        elif command[0] == "RST":
            deinit()
    
    pen_up()
    home()

try:
    main()
except KeyboardInterrupt:
    deinit()

