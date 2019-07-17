import socket
import threading

clientList = []
newThreads = []
allActiveThreads = []
messages = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 4000))
print("Binded socket")
s.listen(5)

def listenAndStoreClients(): 
    while True: 
        print("listening")
        c, a = s.accept()
        clientList.append((c,a))
        print(f"{a} has connected")
    
def storeMessages(): 
    while True: 
        print("storing")

def sendMessages(): 
    while True: 
        for x in messages: 
            print("x")


newThreads.append(threading.Thread(target=listenAndStoreClients)) #stores thread that listens and stores client in newThreads
newThreads.append(threading.Thread(target=storeMessages))
newThreads.append(threading.Thread(target=sendMessages))

while True: 
    for x in newThreads: #starts any inactive threads stored in newThreads, moves active threads into allActiveThreads
        x.start()
        allActiveThreads.append(x)
        newThreads.pop(newThreads.index(x))
