# decreament pb on GPIO23 , 36 , D23
#
#
#

from machine import Pin, Timer
from time import sleep

def dec_handle(pin):
    print("|| PRESSED")

def debounce(pin):
    timer.init(mode=Timer.ONE_SHOT, period=200, callback=lambda pin: dec_handle(pin))

timer = Timer(0)
dec_pb = Pin(23, Pin.IN , pull=Pin.PULL_UP)
dec_pb.irq(handler=debounce, trigger=Pin.IRQ_FALLING)
dec_pb.value()
