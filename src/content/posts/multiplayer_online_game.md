---
title: "Trying to make an online multiplayer minigame"
summary: "A simple article to explain how we made a multiplayer online game using python and what we learnt while doing it, from the very basic use of sockets, to the different communication protocols and a bit of optimization."
date: 2024-03-11T16:39:09-02:00
lastUpdate: 2023-03-26T20:18:09-02:00
tags: ["iscsc","python","network"]
author: Zyno
draft: false
---

## Table of Contents
- [A little introduction](#a-little-introduction)
- [First Step : Successfully sending a simple message to another computer in our LAN](#first-step--successfully-sending-a-simple-message-to-another-computer-in-our-lan)
  - [The server-side](#the-server-side-will-look-like-this-)
  - [The client-side](#on-the-client-side-it-will-be-this-)
- [Simple online implementation to play a basic game](#simple-online-implementation-to-play-a-basic-game)
- [First improvement of the connection](#first-improvement-of-the-connection)
  - [Client-side improvements](#client-side-improvements)
  - [Server-side improvements](#server-side-improvements)
- [But, how to reduce ping?](#but-how-to-reduce-ping)
- [The road to UDP connection](#the-road-to-udp-connection)
  - [What is UDP and why would we want to use that?](#what-is-udp-and-why-would-we-want-to-use-that)
  - [Using UDP sockets instead of TCP sockets](#using-udp-sockets-instead-of-tcp-sockets-)
- [Now : A quite stable game to play](#now--a-quite-stable-game-to-play)
  - [The UDP client-side](#the-udp-client-side-now-looks-like-this-)
  - [The UDP server-side](#on-the-server-side-the-code-for-udp-is-now-designed-like-this-)
- [Future Improvements to do...](#future-improvements-to-do)

## A little introduction

This project, called Haunted Chronicles, started when we wanted to introduce ourselves to online multiplayer games and the code behind it.

Naturally, we decided to code using python because it was simpler to begin with - everyone knew how to code in Python - and because we just wanted to discover the notion, not to code an AAA game.

So, we began with a little documentation and we discovered the magic of **sockets**!

For those who don't know anything about them, it is basically a glass bottle in which you put your message, and that you then throw away in the approximate direction of your friend, hoping for them to receive it. (Here is the very looong documentation of python : https://docs.python.org/3/library/socket.html)

## First Step : Successfully sending a simple message to another computer in our LAN
The first step here to understand how all this socket-stuff works is to try to make a simple 'email' system. The goal here is to make a python script able to send a predefined message to another computer.

To do so, we need to define a server script and a client script.
The server will initialize a socket which will listen to incoming messages, while the client will initialize a socket to send messages to the server.
We wrote this code thanks to the [python documentation's example](https://docs.python.org/3/library/socketserver.html#socketserver-tcpserver-example)

### The server-side will look like this :
```py
import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        
        in_ip = self.client_address[0]
        
        print("{} wrote:".format(in_ip))
        in_data = str(self.data,'utf-16')
        print(in_data)
        
        out = "Hello client, you correctly sent your message : '" + in_data + "' to the server."

        print(">>> ",out,"\n")
        self.request.sendall(bytes(out,'utf-16'))



# ----------------------- Main -----------------------

if __name__ == "__main__":
    HOST, PORT = str(IP), 9998
    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, bound to the given IP on port 9998
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        print("HOST = ",IP,"\nPORT = ",PORT,"\n")
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
```

Ok so it may seem a big difficult to understand, but not everything here is important to really understand, and you will see further that what we did was in fact easier to understand in the end.

But to give some explanation, sockets are 'objects' in Python, so they are custom classes. Here, the class we define (`MyTCPHandler`) is the way the socket must react to incoming messages, not the socket itself which is already coded. It is defined in the `handle(self)` method. What it does here is that it reads the incoming message with `self.data = self.request.recv(1024).strip()`. The data is stored in bytes here. The client address is automatically stored in `self.client_address` as the name is explicit enough. We then just print the client ip and data in the server terminal to be able to check that we correctly received the message (after converting the bytes to str with the `utf-16` convention).

And then, we just send it back to the client with a little confirmation message after converting it back to bytes with the lines :
```py
out = "Hello client, you correctly sent your message : '" + in_data + "' to the server."
self.request.sendall(bytes(out,'utf-16'))
```

So, now that we defined the way we want our socket to react to messages, we just need to initialize it! To do so, we use a [context manager](https://realpython.com/python-with-statement/), which is for example the `open folder` form in Python `with open(...) as f:`.

Here, it is the initialization of our socket :
```py
with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
    print("HOST = ",IP,"\nPORT = ",PORT,"\n")
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
```
What happens here is we initialize a new socket with the given address `(HOST, PORT)` where HOST is the IP of our server (it is the IP of the computer that will run this program). To obtain it, you can either use some websites, your terminal, or use the next Python lines :
```py
import socket

def extractingIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return(ip)

IP = extractingIP()
```

Once the socket is initialized, we verify that it has the correct address `(IP, PORT)` by printing it, and then we use the `serve_forever()` method which makes the server wait for new messages indefinitely and, when he receives one, executes the code we defined in the `handle(self)` method under the `MyTCPHandler` class. Once a message has been processed, it waits for another one to arrive.

The only way to make it stop **for now** is to use ctrl+C in the terminal to shut down the process, but we can obviously implement a better way to shut down the server through the `handle(self)` method for instance (example : if the server receives `"STOP"`, the socket closes itself and the server code terminates).

Don't mind the 
`socketserver.TCPServer.allow_reuse_address = True`, this line is not mandatory but it allows the server to be closed and reopened with the exact same `(IP, PORT)`. If you don't write this line, the only thing that will change is the fact that when closing your server, you will have to wait about 30 seconds to be able to open a new server with the same address.

### On the client-side, it will be this :

```py
from socket import *

SERVER_IP = "localhost"
SERVER_PORT = 9998

def send(msg="Hello server!"):
    """Sends the given message to the server.
    """
    
    with socket(AF_INET, SOCK_STREAM) as sock:        
        # send data
        sock.connect((SERVER_IP, SERVER_PORT))
        sock.sendall(bytes(msg, "utf-16"))
        
        # receive answer
        answer = str(sock.recv(1024*2), "utf-16")
        
        return answer

while True:
    msg = input("What message do you want to send?")
    print(send(msg))
```

As you can see, we use the same kind of code to initialize a client socket. This time, we just don't need to define our own handler as it was the case for the server, and we can simply use the basic `socket` library instead of the `socketserver`. Just be aware that the socket object is `socket.socket` and that its parameters are `socket.AF_INET` and `socket.SOCK_STREAM`, but you can avoid mistakes by importing everything from socket as we did here with `from socket import *`.

Then, we simply collect a message from the user in the terminal, and we send it to the server through the `sock.sendall()` method in our `send()` function. We then wait for the server to answer with `sock.recv()` and we print it.

In this code, we first defined the server ip and port. Here, `"localhost"` is the best way to send the message to yourself without searching for your own ip. This way, you can just execute the server code in an instance of your terminal, and this code in another and try to send yourself some messages!

Then, you can setup the server on another computer and try to communicate with it by changing this IP to the correct one.

## Simple online implementation to play a basic game
Well, to make a simple game, you must implement a visual interface and rules in order to make this a bit more interactive, but the online part is in fact almost done!
We used pygame in order to make a small map where squares - which are players - will be able to move.

The only 'new' thing we need to do is to formalize these messages to make the server understand client's actions.
To do so, we decided that the clients would only send their inputs to the server, and that the server would compute the players' new positions and send them back to the clients. This will implement a semi anti-cheat as players won't be able to directly send their positions to the server, and thus try to teleport. However, it will increase the amount of calculations required by the server and may cause some more lags in case of huge computations due to some game rules later.

We thus decided to implement some basic formalized messages to communicate with the server which are also defined in the [README.md](https://github.com/iScsc/Haunted-Chronicles) on the github page of the project (There are more messages than the ones described here since the game evolved, but here are the first one we used) :

* **Connection** : The client sends `CONNECT <Username> END` to the server, which sends back `CONNECTED <Username> END` if the connection succeeded.
* **Clients' inputs** : The client sends `INPUT <Input> END` to the server where `<Input>` can be either `L` for left, `R` for right, `U` for up, `D` for down or `.` if there are no inputs. The server computes the new position and sends back the new state of the game with `STATE <PlayerList> END` where `<PlayerList>` is the list of player structures, which store the player's name, color and position.
* **Disconnection** : The clients sends `DISCONNECT <Username> END` and receives `DISCONNECTED <Username> END` if the server has correctly destroyed the client's player structure. The client then closes.

The `<Parameter>` fields are to replace with the correct values. For instance, for the connection : `CONNECT Zyno END`. The `END` field allows the server to easily recognize the end of a formatted message, and the conformity of it. The formatted messages begin with a `<TYPE>` field which allows the server to recognize the rule that must be applied on this kind of incoming message.

## First improvement of the connection
Yet, this is not optimized at all. In fact, what we do here is we create a new socket, send a message, then automatically destroy this socket (when exiting the `with` indent), and then start all over from the beginning.
Obviously, this is not the way it should be, and we can improve this by creating a socket at first, and then keeping it open as long as the client is connected.

### Client-side improvements

Instead of this :
```py
def send(input="INPUT " + USERNAME + " . END"):
    """Send a normalized request to the server and listen for the normalized answer.

    Args:
        input (str): Normalized request to send to the server. Defaults to "INPUT <Username> . END".

    Returns:
        str: the normalized answer from the server.
    """
    
    global PING
    
    with socket(AF_INET, SOCK_STREAM) as sock:
        t = time.time()
        
        # send data
        sock.connect((SERVER_IP, SERVER_PORT))
        sock.sendall(bytes(input, "utf-16"))
        
        
        # receive answer
        answer = str(sock.recv(1024*2), "utf-16")
        
        PING = int((time.time() - t) * 1000)
        
        return answer
```
We now write this :
```py
SOCKET = None

PING = None # To display the approximate ping with the server

#
#
# More code for display and things like that...
#
#

def send(input="INPUT " + USERNAME + " . END"):
    """Send a normalized request to the server and listen for the normalized answer.

    Args:
        input (str): Normalized request to send to the server. Defaults to "INPUT <Username> . END".

    Returns:
        str: the normalized answer from the server.
    """
    
    global PING
    global SOCKET
    
    # Initialization, when the socket has not been created yet
    if (SOCKET == None and input[0:7] == "CONNECT"):
        SOCKET = socket(AF_INET, SOCK_STREAM)
        SOCKET.settimeout(SOCKET_TIMEOUT)
        SOCKET.connect((SERVER_IP, SERVER_PORT))
    
    
    # Usual behavior
    if SOCKET != None:
        t = time.time()

        # send data
        try:
            SOCKET.sendall(bytes(input, "utf-16"))
            
            # receive answer
            answer = str(SOCKET.recv(1024*2), "utf-16")
            
            PING = int((time.time() - t) * 1000)
            
            return answer
        except:
            exitError("Loss connection with the remote server.")
```

So, as you can see, we stopped using the `with` magic formula and we now initialize our socket in a GLOBAL variable named `SOCKET`. In fact, we detect the first need of defining our socket when the formalized `CONNECT` message is used, and that's why we don't initialize it before, in case the message would be wrong, but also to be able in some peculiar cases to disconnect and reconnect with a new socket.

The rest of the code is really the same function as we used before. We send a formalized message to the server and then wait for the answer. This answer is interpreted to display the correct players at the correct positions, and even the approximate ping with the server which we simply compute with the time the answer took to come back, starting just before we sent our own message.

It is in another function but we detect the disconnection when the client presses the escape button or closes the window, and we then executes this important code :
```py
    SOCKET.close()
    SOCKET = None
```
It is only two lines but it is really important to not forget to close the initialized sockets when they are not needed anymore. And putting SOCKET to None allows us to reconnect to another server if wanted.

Obviously, we also improved the server-side on the exact same basis.
Another key library we had to use was the threading library which allows to emulate threads in python. It was mandatory to display images with pygame while keeping sending messages to the server and receiving answers from it.

### Server-side improvements

For the server-side, our main became this :
```py
from socket import *
from threading import *

def main():
    global MAINSOCKET
    global LOCK
    
    # Initialization
    if MAINSOCKET == None:
        MAINSOCKET = socket(AF_INET, SOCK_STREAM)
        MAINSOCKET.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        MAINSOCKET.bind((IP, PORT))
        MAINSOCKET.listen(BACKLOG)
    
    if LOCK == None:
        LOCK = Lock()
    
    print("Server opened with :\n    - ip = " + str(IP) + "\n    - port = " + str(PORT))
    
    listener_new = Thread(target=listen_new)
    manager_server = Thread(target=manage_server)
    listener_old = Thread(target=listen_old)
    
    listener_new.start()
    manager_server.start()
    listener_old.start()

if __name__ == "__main__":
    main()
```
Here we initialize the `MAINSOCKET` which is a socket from the basic `socket` library, and which will only be responsible for the connection attempts. We use the `socket.bind(address)` method to make it listens for incoming messages at the given `(IP, PORT)`. We then configure the maximum number of connection attempts the socket can queue with the `socket.listen(BACKLOG)` method. In our case, we used `BACKLOG = 1` and it is good to know that this parameter should usually be between 1 and 5 (usually 5 is the system-dependant maximum possible value). So our server will only accept a single connection each time we use the further explained `socket.accept()` method.

We can see that we also defined our threads and started them.

I won't show the complete code of these threads but to resume, the `listen_new` thread is the one that use the `MAINSOCKET` to accept new connections. The `listen_old` is the one that uses the newly created sockets to listen for already connected users. And the `manage_server` thread is a thread that allows the server to take commands from its terminal in order to change some parameters or close the server.

So, let's start with the new way to accept connections. In the `listen_new` function, we wrote :
```py
sock, addr = MAINSOCKET.accept()
in_ip = addr[0]

data = sock.recv(1024).strip()

print("{} wrote:".format(in_ip))
in_data = str(data,'utf-16')
print(in_data)

out = processRequest(in_ip ,in_data)
message = out.split(' ')

if message[0]=="CONNECTED":
    LOCK.acquire()
    username = message[1]
    dicoSocket[username] = (sock, addr)
    LOCK.release()

print(">>> ",out,"\n")
try:
    sock.sendall(bytes(out,'utf-16'))
```

Ok so, the `MAINSOCKET.accept()` method listens for new connections that use the `SOCKET.connect((SERVER_IP, SERVER_PORT))` we saw on the client-side. When a connection succeeds, this method creates another socket, binds it to the client's socket and returns both the newly created socket and the address of the client. After this, when the client uses the `SOCKET.sendall()` method, the client will in fact send the data to this newly created socket.

Then, we receive the connection data from the client and try to connect it to the server through our `processRequest(ip, data)` function. If it succeeds, we will send back a message of the type `CONNECTED <Username> END`. If it the case, we use our `LOCK` object (class from the `threading` library) which will temporary block the other threads with `LOCK.acquire()` while we store the newly created socket in a global list. Then, the `LOCK.release()` function will resume the threads.


Then, to process the data sent to the already connected clients, we use our `listen_old` function, in which we wrote :
```py
for elt in waitingDisconnectionList:
    username, sock, addr = elt[0], elt[1], elt[2]
    dicoSocket.pop(username)
    
    # deco remaining player with same ip if needed.
    for username in dicoJoueur:
        if dicoJoueur[username].ip == addr[0]:
            dicoJoueur.pop(username)
            break
    
    sock.close()
waitingDisconnectionList = []


LOCK.acquire()
for username in dicoSocket:
    sock = dicoSocket[username][0]
    addr = dicoSocket[username][1]

    data = sock.recv(1024).strip()
    
    in_ip = addr[0]
    
    print("{} wrote:".format(in_ip))
    in_data = str(data,'utf-16')
    print(in_data)
    
    out = processRequest(in_ip ,in_data)
    message = out.split(" ")
            
    if message[0]=="DISCONNECTED":
        username = message[1]
        waitingDisconnectionList.append((username, sock, addr))
    
    print(">>> ",out,"\n")
    try:
        sock.sendall(bytes(out,'utf-16'))
    except:
        waitingDisconnectionList.append((username, sock, addr))
LOCK.release()
```

The first loop is made to disconnect clients that sent the `DISCONNECT <Username> END` message. The second loop which is in the `LOCK.acquire()` state process data from the already connected clients, thanks to the socket dictionary we used to store the newly created sockets. This code would crash if new clients connected and if the dictionary changed during the for loop, so that's why we lock the other threads.

Yet, the code is very similar to the client side here, but we first listen for data, and then send our answer back.

## But, how to reduce ping?
Yet, when several players connect (more than 3 in average), clients start to suffer from increasing ping, which end up creating seconds of latency for players' movements. But how does this happen?
It seems the server is overcrowded! In fact, we assume that we were DDOSing our own server by sending way too many messages at the same time...

A first thing we could do is to reduce the frequency of communications with the server to reduce the ping. Indeed it works, but it also make movements less smooth, and ask to change the way we designed the game. Whatever the solution we develop next, this is a good thing to do when possible, because it will greatly help the server and reduce its charge.

But we will now look into another issue we had with this code, and that I didn't talk much about when explaining sockets : its communicating protocol.

## The road to UDP connection
### What is UDP and why would we want to use that?
The thing is, from the very beginning of this project, we learnt how to use sockets with Python, but only using the TCP protocol, which is very **NOT** optimal for video games.

For those who don't know, the TCP protocol means that your communications look like this :
- You establish a communication with an IP sending something like : "I want to talk with you."
- You wait for an answer that says : "Ok, let's talk."
- You send the message you first wanted to send : "Hello I am Zyno and happy to meet you!"
- You wait for the receiver to send back to you : "I have correctly received your message."

And this is a very simplified vision of it, because the TCP Protocol also runs several tests to assure there has been no loss during the communication. And it even make the frequency of communication vary if it thinks that the server is overwhelmed by many messages.
To resume, when you want to make a game, in which losing a single frame of a 60-FPS game is not a problem at all, and you use a way of communicating with the server that may make your client wait before it is allowed to send messages, you are definitely not using the good communication protocol.

On the other hand, let me introduce you to the UDP protocol. This amazing communication protocol basically makes your communications look like this :
- You send the only message you wanted to send : "Hello I am Zyno and happy to meet you!"

And that's it! So, obviously, you may lose some messages in the process, and you won't know it. You don't have TCP's errors detection and correction algorithms either. But as I said earlier, we do not really suffer from a lack of a message every 5 ms in a video game.

### Using UDP sockets instead of TCP sockets :

Now, let's go back to our code. Using UDP sockets in Python isn't really that big of a deal. In fact, it's almost the same!

Look at this :
- This is TCP :
```py
sock = socket(AF_INET, SOCK_STREAM)
```
- And this is UDP :
```py
sock = socket(AF_INET, SOCK_DGRAM)
```
`SOCK_STREAM` means TCP, and `SOCK_DGRAM` UDP and *voilà*!

Ok, it is not **that** simple. The way you previously used this socket has changed a bit as well. Let's see which are the affected functions :

Previously, we were using `server_sock.listen(BACKLOG)` to make a previously bound socket listen to connections, and then `sock, addr = server_sock.accept()` to make it accept connections. On the client side, we used `client_sock.connect((SERVER_IP, SERVER_PORT))` in order to connect our client socket to the listening socket. The server then generated a new socket - named sock here - and the client was now communicating with the server through its dedicated and newly created socket, using the `sock.sendall()` and `sock.recv()` functions.

With UDP sockets, these functions have changed a little :

There is no `sock.listen()`, `sock.accept()` nor `sock.connect()` anymore. However, the `sock.bind((IP, PORT))` function still exists and shall be used to make a socket work as a server which listen at a given IP and PORT.

However, everything else now works with only two functions :
```py
sock.sendto(bytes(message_to_send, "utf-8"), (SERVER_IP, SERVER_PORT))
```
And :
```py
data, addr = sock.recvfrom(MESSAGES_LENGTH)

message_received = str(data.strip(), "utf-8") # Converting the received bytes into an str
```
Where `message_to_send`, which is here a string, is the data to send. It is firstly converted into bytes with the utf-8 encoding. You can also send any kind of data as long as you send it using bytes. The address you send the data to is given by the second parameter : `(SERVER_IP, SERVER_PORT)`.
To receive data, the `recvfrom()` function takes the maximum length of the message you want to receive (in bytes). It returns both the `data` in bytes, and the address `addr = (IP, PORT)` from which the data has been sent. In our case, we convert it back into a string using the utf-8 decoding. (We did change our encoding because as our formatted messages gained new keywords, and thus length, we wanted to reduce their sizes and we decided to lose the utf-16 characters to do so.)

And that's it! Now, it's time for you to think about how you will use these two simple functions in order to make what you want!

## Now : A quite stable game to play
### The UDP client-side now looks like this :

Here is the initialization of the socket on the client-side :
```py
SOCKET = socket(AF_INET, SOCK_DGRAM)
SOCKET.settimeout(SOCKET_TIMEOUT)
```
`SOCKET_TIMEOUT` being 0.5s in our case.

The data is sent to the server using :
```py
SOCKET.sendto(bytes(input, "utf-8"), (SERVER_IP, SERVER_PORT))
```

The data is received using :
```py
data, addr = SOCKET.recvfrom(MESSAGES_LENGTH)
```

When we exit the game, the client finishes by closing the socket using the usual :
```py
SOCKET.close()
```

### On the server-side, the code for UDP is now designed like this :

The initialization is :
```py
MAINSOCKET = socket(AF_INET, SOCK_DGRAM)
MAINSOCKET.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Allows for the server to be reopened with the same ip immediately after being closed.
MAINSOCKET.settimeout(TIMEOUT)
MAINSOCKET.bind((HOST, PORT))
```

The server receives the data from clients with :
```py
data, addr = MAINSOCKET.recvfrom(MESSAGES_LENGTH)
```

and send back data with :
```py
MAINSOCKET.sendto(bytes(out,'utf-8'), addr)
```

However, we give each client a dedicated socket (linked to a given port) to talk to :
```py
if message[0]=="CONNECTED":  # Detect connection
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.settimeout(TIMEOUT)
    
    # port attribution    
    port = availablePorts[0]  # use a free port for this new client
    out = message[0] + " " + str(port)
    for s in message[1:]:
        out += (" " + s)
    # Add the information of the new port in the connection message
    # out = CONNECTED <port> <username> <size> WALLS <wallstring> STATE <statestring> END

    sock.bind((HOST, port))
    availablePorts.remove(port)

    username = message[1]
    dicoSocket[addr] = (sock, username)  # Keep the information of the link between sockets and players
```

When a client has its own dedicated socket, it receives the information of the new port in the connection confirmation, and changes the port it sends messages to using the command :
```py
SERVER_PORT = int(portStr)
```
With `portStr` being the extract of the connection message (the second word of the answer).

After that, clients sends their messages to their own dedicated socket. We detect on the server side which sockets have received data using the lines :
```py
sockets = [MAINSOCKET] + [dicoSocket[addr][0] for addr in dicoSocket]

if sockets != []:
    inSockets, _, _ = select.select(sockets, [], [], TIMEOUT)
```
Because the select module allows to efficiently (low level) keep only sockets that have received data.

Once sockets that have received data has been selected, a for loop on them to apply the usual reception and answering code allows for each client to send their inputs and receive the new state of the game.

Finally, don't forget to close every socket before completely closing the server, including the MAINSOCKET.
When a client disconnects, its socket can be closed as well and its port can be add back in the available ports list:
```py
availablePorts.append(port)
sock.close()
```

## Future Improvements to do...
To keep on improving the performances of the online system, we worked on a thread based system in which both clients and the server would have one thread to listen for messages, and one thread to send their messages. In this scenario, the server sends automatically every few milliseconds the current state of the game to every clients connected to the server, while each client sends their input continuously.

Another way to improve the ping that we did not implement yet is to make clients stop sending permanently all their inputs. Instead, clients would only send their new inputs when the player changes input. This way, the server would receive way less messages and it would instead store the last input made by each player, and assume it is their current input as long as they do not send another one.
This would work by sending a rack of several messages when changing input to be sure the server has correctly received it, and by asking for a confirmation.
In this case, the server would make the state of the game update every X ms, with the stored inputs of every player, and automatically send back to everyone the new state of the game.

Finally, another way to make the game look a lot smoother would be to let clients assume and compute the next frames of the game without waiting for the actual computations of the server. This could help make the game look smoother even when the connection is not stable, and it is what is done in most online games nowadays.
