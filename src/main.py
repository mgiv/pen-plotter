from stepper import Stepper
import time
import machine
from machine import Pin
from random import randint
import micropython
import asyncio

micropython.alloc_emergency_exception_buf(100)

ksw = Pin(12, Pin.IN, Pin.PULL_UP)

s1 = Stepper(18,19,steps_per_rev=3200,speed_sps=5000, timer_id=0)
s2 = Stepper(16,21,steps_per_rev=3200,speed_sps=5000, timer_id=1, invert_dir=True)

en = Pin(17, Pin.OUT)

async def run_steppers():
    en.value(0)

    while True:
        target = randint(0,900)
        print("Moving to target: %s" % target)
        
        s1.target_deg(target)
        s2.target_deg(target)
        
        await asyncio.sleep_ms(1000)

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
    await asyncio.gather(run_steppers(), kill_switch())

try:
    asyncio.run(main())
except KeyboardInterrupt:
    deinit()
    

