import _thread as th
import time
import usocket as socket
import machine
from machine import Pin,SoftI2C
import ssd1306


i2c = SoftI2C(scl=Pin(4), sda=Pin(5))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

z="Client 0:Yes I am coming";
y="Client 0:No, I am not coming";
buzzer = Pin(2,Pin.OUT)
led = Pin(23, Pin.OUT)    # 22 number in is Output
push_button = Pin(18, Pin.IN)# 23 number pin is input
push_button1 = Pin(19,Pin.IN)
buzzer.value(1)

def scroll_screen_in_out(screen):
  for i in reversed(range (0, (oled_width+1)*2, 1)):
    for line in screen:
      oled.text(line[2], -oled_width+i, line[1])
    oled.show()
    if i!= oled_width:
      oled.fill(0)
      
#client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

#Enable broadcasting mode
#client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
def recieve():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
    client.bind(('192.168.61.44',37020)) #Client ESP IP Address , Port Number should be same
    while True:
        data, addr = client.recvfrom(1024)
        print("received message: %s"%data)
        screen1 = [[0, 0 , data]]
        scroll_screen_in_out(screen1)
        break

def send():
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.61.164',2785)) #Server Laptop IP Address , Port Number should be same
    while True:
#         s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         s.connect(('192.168.1.10',2785))
        logic_state = push_button.value()
        logic_state1 = push_button1.value()
        if logic_state == True:     # if pressed the push_button
            led.value(1)             # led will turn ON
            buzzer.value(0)
            print('Button Pressed')
            oled.fill(0)
            oled.text('Yes I am Coming', 0, 0, 1)
            oled.show()
            s.send(z.encode())
            break
        elif logic_state1 == True:
            led.value(1)             # led will turn ON
            buzzer.value(0)
            print('Button Pressed')
            oled.fill(0)
            oled.text('No,I am not Coming', 0, 0, 1)
            oled.show()
            s.send(y.encode())
            break

th.start_new_thread(recieve,())

th.start_new_thread(send,())