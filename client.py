import socket
import threading
from termcolor import cprint, colored

ID = [0]
newThreads = []
allActiveThreads = []
allColors = ["grey", "red", "green", "yellow", "blue", "magenta", "cyan"]
myColor = ""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("172.19.17.36", 40000))
#s.connect((socket.gethostname(), 40000))
print("Connected to server")


def sendInput(): 
    while True: 
        if len(ID) == 2: 
                s.send(bytes(str(ID[len(ID)-1]) + ": " + input(), "UTF-8"))


def recieveAndPrint(): 
    while True: 
        messageFromServer = s.recv(2048).decode("UTF-8")
        if messageFromServer[0:3] == "ID:": 
                ID.append(messageFromServer[3:8])
                myColor = allColors[int(ID[1])%7]
                output = colored("My color: " + myColor, myColor, attrs=["bold"])
                print(output)
                #cprint("My color: " + myColor, myColor, "on_red")
        else: 
                #add if/else statement here to print message based on color
                if myColor == "": 
                        print(messageFromServer)
                else: 
                        cprint(messageFromServer, allColors[int(messageFromServer[0:1])%7])

newThreads.append(threading.Thread(target=recieveAndPrint))
newThreads.append(threading.Thread(target=sendInput))


while True: 
    for x in newThreads: 
        x.start()
        allActiveThreads.append(x)
        newThreads.pop(newThreads.index(x))