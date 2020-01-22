import socket
import threading
from threading import Lock
import time

lock = Lock()

localIP,localPort =("127.0.0.1", 1234)

BUFFER_SIZE = 7
buffer_occupied = 0

BUFFER=[' ']*BUFFER_SIZE

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))


def pop_from_bufffer():
    
    global BUFFER,BUFFER_SIZE,buffer_occupied

    time.sleep(2)

    while 1:
            
        lock.acquire()
            
        if buffer_occupied > 0:                     #check for buffer underflow
                
            
            BUFFER.pop(0)                           #pop item at position 0 of buffer
            BUFFER.append(' ')                     #replcae item to be popped with None
            buffer_occupied = buffer_occupied -1    #decrement buffer occupancy
        #else:
        #    print("Buffer Underflow! Speed Up Data Rate.")

        lock.release()

        time.sleep(0.5)
    
ITERATIONS , CLIENT_ADDRESS = UDPServerSocket.recvfrom(1024)

thread1 = threading.Thread(target = pop_from_bufffer)
thread1.start()
parent_data =  0
for i in range(int(ITERATIONS)):
    message = UDPServerSocket.recvfrom(1024)
    data = int(message[0])

   #Parent Node inserts data
    if BUFFER_SIZE > buffer_occupied: #check for buffer overflow
        parent_data = parent_data + 1
        lock.acquire()
        BUFFER[buffer_occupied] = parent_data

        buffer_occupied = buffer_occupied + 1
        lock.release()
        
    else:
        
        UDPServerSocket.sendto(str("Slow down").encode('utf-8'),CLIENT_ADDRESS)    #tell child node to slow down
        
        print("Data Dropped! ",parent_data," Slow Down Data Rate\n")

    #Child Node inserts data
    if BUFFER_SIZE > buffer_occupied:  #check for buffer overflow
        UDPServerSocket.sendto(str("Speed Up").encode('utf-8'),CLIENT_ADDRESS)

        lock.acquire()
        
        BUFFER[buffer_occupied] = data

        buffer_occupied = buffer_occupied + 1

        lock.release()
        
    else:
        
        UDPServerSocket.sendto(str("Slow down").encode('utf-8'),CLIENT_ADDRESS)    #tell child node to slow down
        
        print("Data Dropped! ",data,"\n")
        
        
    print(BUFFER," \t\t Buffer Occupancy Level = ",buffer_occupied,"\n")
