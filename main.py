# decreament pb on GPIO23 , D23
# increament pb on GPIO22 , D22
# reset pb on GPIO21 , D21

from machine import Pin, Timer
from time import sleep

DEC_PIN = 23
INC_PIN = 22
RST_PIN = 21

counter_value = 0
pressed_pb = None

def handler(t):
    global pressed_pb
    global counter_value
    if pressed_pb == Pin(RST_PIN):                     # reset
        counter_value = 0
    elif pressed_pb == Pin(DEC_PIN):                   # decreament
        if counter_value == 0:
            counter_value = 9
        else:
            counter_value = counter_value - 1
    else:                                       # increment
        if counter_value == 9:
            counter_value = 0
        else:
            counter_value = counter_value + 1
    print("||", counter_value)

def debounce(pin):
    global pressed_pb
    pressed_pb = pin
    timer.init(mode=Timer.ONE_SHOT, period=200, callback=handler)


timer = Timer(0)
dec_pb = Pin(DEC_PIN, Pin.IN , pull=Pin.PULL_UP)
dec_pb.irq(handler=debounce, trigger=Pin.IRQ_FALLING)
inc_pb = Pin(INC_PIN, Pin.IN , pull=Pin.PULL_UP)
inc_pb.irq(handler=debounce, trigger=Pin.IRQ_FALLING)

# temp auxillary
def reset():
    import machine
    machine.reset()
