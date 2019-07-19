import socket
import threading


clientList = []  # List that stores all clients (active and inactive)
newThreads = []  # List that stores new (inactive) threads
allActiveThreads = []  # List that stores active threads
messages = [] # List that stores unsent messages (message will be deleted after message is sent)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creating a socket


# Binding the socket to host's IP and port 40000
s.bind((socket.gethostname(), 40000))
print("Server active")

# Listens for 6 clients
s.listen(6)


# Function that listens for new clients, stores new clients in a list called clientList
def listenAndStoreClients():
    while True:
        # Accecpts the client. c is an object that represents the client, a is their address
        c, a = s.accept()
        clientList.append((c, a))
        print(f"{a[1]} has connected")
        # creates new thread that listens to this specific client
        newThreads.append(threading.Thread(target=recieveFromThisClient, args=(c, a,)))
        # Sends the client its ID (index on the client list)
        c.send(bytes("ID:" + str(len(clientList)), "UTF-8"))


# Function that recieves and stores incomming messages to the messages list
def recieveFromThisClient(c, a):
    while True:
        # Reieves the message in byte string and decodes it
        incomingMessage = c.recv(2048).decode("utf-8")
        if incomingMessage != "":
            messages.append(incomingMessage)


# Function that sends all messages to all clients
def sendMessages():
    while True:
        for x in messages:
            for y in clientList:
                y[0].send(bytes(x, "UTF-8"))
            # Adds message to the messages list
            messages.pop(messages.index(x))


# Stores thread that listens and stores client in newThreads
newThreads.append(threading.Thread(target=listenAndStoreClients))
# Stores thread that sends messages to all clients
newThreads.append(threading.Thread(target=sendMessages))


while True:
    # Starts any inactive threads stored in newThreads list, moves active threads into allActiveThreads list
    for x in newThreads:
        x.start()
        allActiveThreads.append(x)
        newThreads.pop(newThreads.index(x))