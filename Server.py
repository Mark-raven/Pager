import threading
import socket
import time


def send():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) 
    udp.settimeout(0.2)
    while True:
        message = b"4pm Meeting at the office"
        udp.sendto(message,('192.168.203.16',37020)) #Client ESP IP Address , Port Number should be same
        #udp.sendto(message,('192.168.61.169',37020))
        #udp.sendto(message,('192.168.61.225',37020))
        time.sleep(1)
def recieve():
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('192.168.203.36',2785)) #Server Laptop IP Address , Port Number should be same 
    s.listen(5)
    while True:
        #port number can be anything between 0-65535(we usually specify non-previleged ports which are > 1023)
        clt,adr=s.accept() 
        print(clt.recv(1024))

if __name__ == "__main__":
    # creating thread
    t1 = threading.Thread(target=send)
    t2 = threading.Thread(target=recieve)

    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()
