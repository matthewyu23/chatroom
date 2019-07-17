import socket
import threading
import os

clientList = []
newThreads = []
allActiveThreads = []
messages = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 4000))
print("Binded socket")
s.listen(5)

def listenAndStoreClients(): #listens for new clients, stores new clients in a list called clientList
    while True: 
        print("listening")
        c, a = s.accept()
        clientList.append((c,a))
        print(f"{a} has connected")
        newThreads.append(threading.Thread(target=recieveFromThisClient, args=(c,a,))) #creates new thread for this specific client
    


def recieveFromThisClient(c,a): #recieves and stores incomming messages to the messages list
    while True: 
        incomingMessage = c.recv(2048).decode("utf-8")
        if incomingMessage != "": 
            fullMessage = str(a[1]) + " " + incomingMessage
            messages.append(fullMessage)


def sendMessages(): 
    while True: 
        for x in messages: 
            print(x)


newThreads.append(threading.Thread(target=listenAndStoreClients)) #stores thread that listens and stores client in newThreads
newThreads.append(threading.Thread(target=sendMessages))

while True: 
    for x in newThreads: #starts any inactive threads stored in newThreads, moves active threads into allActiveThreads
        x.start()
        allActiveThreads.append(x)
        newThreads.pop(newThreads.index(x))
    print(messages)
