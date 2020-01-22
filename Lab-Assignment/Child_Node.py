import socket
import time
import matplotlib.pyplot as plt

server_address = ("127.0.0.1", 1234)

buffer_size  = 1024     #buffer size
num = 50                #Amount of data to be sent by child node
speed_up_factor = 0.65  #increase data rate by this factor
slow_down_factor = 8   #deacrese data rate by this factor
wait_time = 12          #time to wait

data_list=[]            #list of data to be sent to parent node
speed_list=[]           #list of speed to be sent to parent node

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

UDPClientSocket.sendto(str(num).encode('utf-8'), server_address)


for data in range(num):
    
    UDPClientSocket.sendto(str(data).encode('utf-8'), server_address)

    message = str(UDPClientSocket.recvfrom(1024)[0])

    if "speed" in str(message).lower():
        wait_time = wait_time* speed_up_factor
        print("( ↑ ) Speeding up by \t",wait_time)
        data_list.append(data)
        speed_list.append(1/wait_time)
    elif "slow" in str(message).lower():
        wait_time = wait_time * slow_down_factor
        print("( ↓ ) Slowing down by \t",wait_time)
        data_list.append(data)
        speed_list.append(1/wait_time)

    time.sleep(wait_time)


print("All Data Has Been Sent!")
plt.plot(data_list, speed_list, '.-')
plt.xlabel("Data Generated at Child Node")
plt.ylabel("Speed")
plt.show()


