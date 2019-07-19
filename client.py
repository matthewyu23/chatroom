import socket
import threading
# termcolor module makes it easy to print text with color and style (makes text bold)
from termcolor import cprint, colored


ID = [0]  # Creates a place holder ID, new ID will be appended to the 1st element
newThreads = []  # List that stores any threads yet to be activacted
allActiveThreads = []  # List that stores any activacted threads
allColors = ["red", "green", "yellow", "blue", "magenta", "cyan"]
myColor = ""  # Place holder color, will be assigned later
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creates socket


# Connect to socket with the host's IP and 40000
s.connect(("172.19.17.36", 40000))
print("Connected to server")


# Function that recieves message from server and prints it
def recieveAndPrint():  
    while True:
        messageFromServer = s.recv(2048).decode("UTF-8")  # Recieve and decode
        # Takes welcome message from server and stores ID
        if messageFromServer[0:3] == "ID:":
            ID.append(messageFromServer[3:8])
            # Assigns myColor, which is calculated based on the ID and the index of allColors list
            myColor = allColors[int(ID[1]) % 6]
            output = colored("My ID: " + str(ID[1] + "\nMy color: " + myColor), myColor, attrs=["bold"])
            print(output)
        else:
            if myColor == "":
                print(messageFromServer)
            else:
                cprint(messageFromServer,
                       allColors[int(messageFromServer[0:1]) % 6])


# Function that sends user input after ID has been assigned (length of ID list is 2)
def sendInput():  
    while True:
        if len(ID) == 2:
            s.send(bytes(str(ID[len(ID)-1]) + ": " + input(), "UTF-8"))

# Creates and stores new thread
newThreads.append(threading.Thread(target=recieveAndPrint))  
# Creates and stores new thread
newThreads.append(threading.Thread(target=sendInput))  


while True:
    # Starts inactive threads
    for x in newThreads:  
        x.start()
        allActiveThreads.append(x)
        newThreads.pop(newThreads.index(x))