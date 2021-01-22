import network
import usocket
from time import sleep
from machine import Pin

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

# Pin Numbers
DEC_PIN = 23
INC_PIN = 22
RST_PIN = 21
DCDR_A = 5
DCDR_B = 17
DCDR_C = 16
DCDR_D = 4

# wifi access point parameters
AP_NAME = "ESP-Said"
AP_PASS = "123456798"

# Global Variables
counter_value = 0
pressed_pb = None

# Functions
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

# wait for wifi clients
print("waiting for wifi clients")
while wifi_ap.isconnected() == False:
    sleep(2)

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
        conn.sendall(str(counter_value))
    elif request == WEB_1:
        counter_value = 1
        conn.sendall(str(counter_value))
    elif request == WEB_2:
        counter_value = 2
        conn.sendall(str(counter_value))
    elif request == WEB_3:
        counter_value = 3
        conn.sendall(str(counter_value))
    elif request == WEB_4:
        counter_value = 4
        conn.sendall(str(counter_value))
    elif request == WEB_5:
        counter_value = 5
        conn.sendall(str(counter_value))
    elif request == WEB_6:
        counter_value = 6
        conn.sendall(str(counter_value))
    elif request == WEB_7:
        counter_value = 7
        conn.sendall(str(counter_value))
    elif request == WEB_8:
        counter_value = 8
        conn.sendall(str(counter_value))
    elif request == WEB_9:
        counter_value = 9
        conn.sendall(str(counter_value))
    else:
        conn.sendall("-1")
    conn.close()
    print("[LOOP] Counter Value = %d" %counter_value)
    print("[LOOP] ------------------------------------------")
#*************************************************#
