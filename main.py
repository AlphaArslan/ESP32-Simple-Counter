# decreament pb on GPIO23 , D23
# increament pb on GPIO22 , D22
# reset pb on GPIO21 , D21
# BCD-SSD decoder A on GPIO5
# BCD-SSD decoder B on GPIO17
# BCD-SSD decoder C on GPIO16
# BCD-SSD decoder D on GPIO4

from machine import Pin, Timer
from time import sleep
import network
import usocket

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

# supported web requests
WEB_DEC = "dec"                     # decrement
WEB_INC = "inc"                     # increment
WEB_RST = "rst"                     # reset
WEB_RES = "res"                     # result
WEB_0 = "zer"
WEB_1 = "one"
WEB_2 = "two"
WEB_3 = "thr"
WEB_4 = "fou"
WEB_5 = "fiv"
WEB_6 = "six"
WEB_7 = "sev"
WEB_8 = "eig"
WEB_9 = "nin"

# wifi access point parameters
AP_NAME = "ESP-Said"
AP_PASS = "123456798"

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

#******************* Functions *******************#
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
    if t != None:
        print("[PBTN] A button is pressed")
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
    if t != None:
        print("[PBTN] Counter Value = %d" %counter_value)

def debounce(pin):
    global pressed_pb
    pressed_pb = pin
    timer.init(mode=Timer.ONE_SHOT, period=400, callback=handler)

# temp auxillary Functions
def reset():
    import machine
    machine.reset()

def check_ssd():
    while 1:
        for i in range(0,10):
            update_display(i)
            sleep(1)
#*************************************************#

#********************* Setup *********************#
# global setup
import esp
esp.osdebug(None)

# setting up pins
timer = Timer(0)
dec_pb = Pin(DEC_PIN, Pin.IN , pull=Pin.PULL_UP)
dec_pb.irq(handler=debounce, trigger=Pin.IRQ_FALLING)
inc_pb = Pin(INC_PIN, Pin.IN , pull=Pin.PULL_UP)
inc_pb.irq(handler=debounce, trigger=Pin.IRQ_FALLING)
rst_pb = Pin(RST_PIN, Pin.IN , pull=Pin.PULL_UP)
rst_pb.irq(handler=debounce, trigger=Pin.IRQ_FALLING)
A_pin = Pin(DCDR_A, Pin.OUT)
B_pin = Pin(DCDR_B, Pin.OUT)
C_pin = Pin(DCDR_C, Pin.OUT)
D_pin = Pin(DCDR_D, Pin.OUT)
update_display(0)

# setting up the wifi network
wifi_ap = network.WLAN(network.AP_IF)
wifi_ap.config(essid=AP_NAME, authmode=3 ,password=AP_PASS)
wifi_ap.config(max_clients=2)
wifi_ap.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '8.8.8.8'))
wifi_ap.active(True)

# setting up web sockets
s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
s.bind(('192.168.4.1', 80))
s.listen(0)
#*************************************************#

#********************** loop *********************#
while True:
    # wait for someone to connect to the wifi
    while wifi_ap.isconnected() == False:
        print("[LOOP] Waiting for wifi clients")
        sleep(2)
    # wait for HTTP requests
    print("[LOOP] Waiting for HTTP requests")
    conn, addr = s.accept()
    print('[HTTP] Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    # print(request)
    request = str(request)[7:10]
    print('[HTTP] Got < %s > request' % request)
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('\n')
    if request == WEB_DEC:
        pressed_pb = Pin(DEC_PIN)
        handler(None)
        conn.sendall(str(counter_value))
    elif request == WEB_INC:
        pressed_pb = Pin(INC_PIN)
        handler(None)
        conn.sendall(str(counter_value))
    elif request == WEB_RST:
        pressed_pb = Pin(RST_PIN)
        handler(None)
        conn.sendall(str(counter_value))
    elif request == WEB_RES:
        conn.sendall(str(counter_value))
    elif request == WEB_0:
        counter_value = 0
        update_display(counter_value)
        conn.sendall(str(counter_value))
    elif request == WEB_1:
        counter_value = 1
        update_display(counter_value)
        conn.sendall(str(counter_value))
    elif request == WEB_2:
        counter_value = 2
        update_display(counter_value)
        conn.sendall(str(counter_value))
    elif request == WEB_3:
        counter_value = 3
        update_display(counter_value)
        conn.sendall(str(counter_value))
    elif request == WEB_4:
        counter_value = 4
        update_display(counter_value)
        conn.sendall(str(counter_value))
    elif request == WEB_5:
        counter_value = 5
        update_display(counter_value)
        conn.sendall(str(counter_value))
    elif request == WEB_6:
        counter_value = 6
        update_display(counter_value)
        conn.sendall(str(counter_value))
    elif request == WEB_7:
        counter_value = 7
        update_display(counter_value)
        conn.sendall(str(counter_value))
    elif request == WEB_8:
        counter_value = 8
        update_display(counter_value)
        conn.sendall(str(counter_value))
    elif request == WEB_9:
        counter_value = 9
        update_display(counter_value)
        conn.sendall(str(counter_value))
    else:
        conn.sendall("-1")
    conn.close()
    print("[LOOP] Counter Value = %d" %counter_value)
    print("[LOOP] ------------------------------------------")
#*************************************************#
