import socket
import threading

newThreads = []
allActiveThreads = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 40000))
print("Connected to server")


def sendInput(): 
    while True: 
        s.send(bytes(input(), "UTF-8"))


def recieveAndPrint(): 
    while True: 
        messageFromServer = s.recv(2048).decode("UTF-8")
        print(messageFromServer)

newThreads.append(threading.Thread(target=sendInput))
newThreads.append(threading.Thread(target=recieveAndPrint))


while True: 
    for x in newThreads: 
        x.start()
        allActiveThreads.append(x)
        newThreads.pop(newThreads.index(x))