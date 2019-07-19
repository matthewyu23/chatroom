import socket
import threading

clientList = [] #List that stores all clients (active and inactive)
newThreads = [] #List that stores new (inactive) threads
allActiveThreads = [] #List that stores active threads
messages = [] #List that stores unsent messages (message will be deleted after message is sent)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creating a socket
s.bind((socket.gethostname(), 40000)) #Binding the socket to host's IP and port 40000
print("Server active")
s.listen(10) #Listens for 10 clients

def listenAndStoreClients(): #Function that listens for new clients, stores new clients in a list called clientList
    while True: 
        c, a = s.accept() #Accecpts the client. c is an object that represents the client, a is their address
        clientList.append((c,a))
        print(f"{a[1]} has connected")
        newThreads.append(threading.Thread(target=recieveFromThisClient, args=(c,a,))) #creates new thread that listens to this specific client
        c.send(bytes("ID:" + str(len(clientList)),"UTF-8")) #Sends the client its ID (index on the client list)
    


def recieveFromThisClient(c,a): #Function that recieves and stores incomming messages to the messages list
    while True: 
        incomingMessage = c.recv(2048).decode("utf-8") #Reieves the message in byte string and decodes it
        if incomingMessage != "": 
            messages.append(incomingMessage)
        


def sendMessages(): #Function that sends all messages to all clients
    while True: 
        for x in messages: 
            for y in clientList: 
                y[0].send(bytes(x, "UTF-8"))
            messages.pop(messages.index(x)) #Adds message to the messages list


newThreads.append(threading.Thread(target=listenAndStoreClients)) #Stores thread that listens and stores client in newThreads
newThreads.append(threading.Thread(target=sendMessages)) #Stores thread that sends messages to all clients

while True: 
    for x in newThreads: #Starts any inactive threads stored in newThreads list, moves active threads into allActiveThreads list
        x.start()
        allActiveThreads.append(x)
        newThreads.pop(newThreads.index(x))