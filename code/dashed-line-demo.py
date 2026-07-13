from stepper import Stepper
import time
import machine
from machine import Pin
from random import randint
import micropython
import asyncio
import network
from servo import Servo

# Allocate buffer in case of crash - doesn't seem to help but there's no harm
micropython.alloc_emergency_exception_buf(100)

# Kill switch - force reboots
ksw = Pin(12, Pin.IN, Pin.PULL_UP)

s1 = Stepper(18,19,steps_per_rev=3200,speed_sps=5000, timer_id=0, invert_dir=True)
s2 = Stepper(16,21,steps_per_rev=3200,speed_sps=5000, timer_id=1, invert_dir=True)

# Down: 0
# Up: 30

srv = Servo(pin_id=25)

# Enable low = on, enable high = off
en = Pin(17, Pin.OUT)


async def run():
    toggle = False

    en.value(0)
    target = 0
    while True:
        while target < 1000:
            toggle = not toggle
            target += 100
            s1.target_deg(target)
            srv.write(30 * toggle)
            time.sleep_ms(300)
        while target > -1000:
            toggle = not toggle
            target -= 100
            s1.target_deg(target)
            srv.write(30 * toggle)
            time.sleep_ms(300)


async def kill_switch():
    while True:
        if ksw.value() == 0:
            print("Kill switch pressed")
            deinit()
        await asyncio.sleep_ms(20)


def deinit():
    print("Stopping program")
    

    s1.stop()
    s2.stop()
    
    en.value(1)
    machine.soft_reset()

def main():
    await asyncio.gather(run(), kill_switch())

try:
    asyncio.run(main())
except KeyboardInterrupt:
    deinit()

    

