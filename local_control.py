# decreament pb on GPIO23 , D23
# increament pb on GPIO22 , D22
# reset pb on GPIO21 , D21
# BCD-SSD decoder A on GPIO5
# BCD-SSD decoder B on GPIO17
# BCD-SSD decoder C on GPIO16
# BCD-SSD decoder D on GPIO4

from machine import Pin, Timer
from time import sleep

# Look-up Table for BCD-SSD decoder (D C B A)
decoder_table = [   (0, 0, 0, 0),
                    (0, 0, 0, 1),
                    (0, 0, 1, 0),
                    (0, 0, 1, 1),
                    (0, 1, 0, 0),
                    (0, 1, 0, 1),
                    (0, 1, 1, 0),
                    (0, 1, 1, 1),
                    (1, 0, 0, 0),
                    (1, 0, 0, 1),
                    ]
# Pin Numbers
DEC_PIN = 23
INC_PIN = 22
RST_PIN = 21
DCDR_A = 5
DCDR_B = 17
DCDR_C = 16
DCDR_D = 4

# Global Variables
counter_value = 0
pressed_pb = None

# Functions
def update_display(value):
    global A_pin
    global B_pin
    global C_pin
    global D_pin
    A_pin.value(decoder_table[value][3])
    B_pin.value(decoder_table[value][2])
    C_pin.value(decoder_table[value][1])
    D_pin.value(decoder_table[value][0])

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
    update_display(counter_value)

def debounce(pin):
    global pressed_pb
    pressed_pb = pin
    timer.init(mode=Timer.ONE_SHOT, period=400, callback=handler)

# main
timer = Timer(0)
dec_pb = Pin(DEC_PIN, Pin.IN , pull=Pin.PULL_UP)
dec_pb.irq(handler=debounce, trigger=Pin.IRQ_FALLING)
inc_pb = Pin(INC_PIN, Pin.IN , pull=Pin.PULL_UP)
inc_pb.irq(handler=debounce, trigger=Pin.IRQ_FALLING)

A_pin = Pin(DCDR_A, Pin.OUT)
B_pin = Pin(DCDR_B, Pin.OUT)
C_pin = Pin(DCDR_C, Pin.OUT)
D_pin = Pin(DCDR_D, Pin.OUT)
update_display(0)

# temp auxillary
def reset():
    import machine
    machine.reset()

def check_ssd():
    while 1:
        for i in range(0,10):
            update_display(i)
            sleep(1)
