# Trying to make an online multiplayer minigame
This project, called Haunted Chronicles, started when we wanted to introduce ourselves to online multiplyaer games and the code behind it.

Naturally, we decided to code using python because it was simpler to begin with - everyone knew how to code in Python - and because we just wanted to discover the notion, not to code a AAA game.

So, we began with a little documentation and we discovered the magic of **sockets** !

For those who don't know anything about them, it is basically a glass bottle in which you put your message, and that you then throw away in the vague direction of your friend, hoping for them to receive it. (Here is the very looong documentation of python : https://docs.python.org/3/library/socket.html)

## First Step : Successfully sending a simple message to another computer in our LAN
blabla

## Simple online implementation to play a basic game
blabla

## First improvement of the connection
blabla

## But, how to reduce ping ?
blabla

## The road to UDP connection
### What is UDP and why would we want to use that ?
The thing is, from the very beginning of this project, we learned how to use sockets with Python, but only using the TCP protocol, which is very **NOT** optimal for video games.

For those who don't know, the TCP protocol means that your communications look like this :
- You establish a communication with an IP sending something like : "I want to talk with you."
- You wait for an answer that says : "Ok, let's talk."
- You send the message you first wanted to send : "Hello I am Zyno and happy to meet you !"
- You wait for the receiver to send back to you : "I have correctly received your message."

And this is a very simplified vision of it, because the TCP Protocol also runs several tests to assure there has been no loss during the communication. And it even make the frequency of communication vary if it thinks that the server is overwhelmed by many messages.
To resume, when you want to make a game, in which losing a single frame of a 60-FPS game is not a problem at all, and you use a way of communicating with the server that may make your client wait before it is allowed to send messages, you are definitely not using the good communication protocol.

On the other hand, let me introduce you to the UDP protocol. This amazing communication protocol basically makes your communications look like this :
- You send the only message you wanted to send : "Hello I am Zyno and happy to meet you !"

And that's it ! So, obviously, you may lose some messages in the process, and you won't know it. You don't have TCP's errors detection and correction algorithms either. But as I said earlier, we do not really suffer from a lack of a message every 5 ms in a video game.

### Using UDP sockets instead of TCP sockets :

Now, let's go back to our code. Using UDP sockets in Python isn't really that big of a deal. In fact, it's almost the same !

Look at this :
- This is TCP :
```
sock = socket(AF_INET, SOCK_STREAM)
```
- And this is UDP :
```
sock = socket(AF_INET, SOCK_DGRAM)
```
`SOCK_STREAM` means TCP, and `SOCK_DGRAM` UDP and voilà !

Ok, it is not **that** simple. The way you previously used this socket has changed a bit as well. Let's see which are the affected functions :

Previously, we were using `server_sock.listen(BACKLOG)` to make a previously bound socket listen to connections, and then `sock, addr = server_sock.accept()` to make it accept connections. On the client side, we used `client_sock.connect((SERVER_IP, SERVER_PORT))` in order to connect our client socket to the listening socket. The server then generated a new socket - named sock here - and the client was now communicating with the server through its dedicated and newly created socket, using the `sock.sendall()` and `sock.recv()` functions.

With UDP sockets, these functions have changed a little :

There is no `sock.listen()`, `sock.accept()` nor `sock.connect()` anymore. However, the `sock.bind((IP, PORT))` function still exists and shall be used to make a socket work as a server which listen at a given IP and PORT.

However, everything else now works with only two functions :
```
sock.sendto(bytes(message_to_send, "utf-8"), (SERVER_IP, SERVER_PORT))
```
And :
```
data, addr = sock.recvfrom(MESSAGES_LENGTH)

message_received = str(data.strip(), "utf-8") # Converting the received bytes into an str
```
Where `message_to_send`, which is here a string, is the data to send. It is firstly converted into bytes with the utf-8 encoding. You can also send any kind of data as long as you send it using bytes. The address you send the data to is given by the second parameter : `(SERVER_IP, SERVER_PORT)`.
To receive data, the `recvfrom()` function takes the maximum length of the message you want to receive (in bytes). It returns both the `data` in bytes, and the address `addr = (IP, PORT)` from which the data has been sent. In our case, we convert it back into a string using the utf-8 decoding.

And that's it ! Now, it's time for you to think about how you will use these two simple functions in order to make what you want !

## Now : A quite stable game to play
### The UDP client-side now looks like this :

Here is the initialization of the socket on the client-side :
```
SOCKET = socket(AF_INET, SOCK_DGRAM)
SOCKET.settimeout(SOCKET_TIMEOUT)
```
`SOCKET_TIMEOUT` being 0.5s in our case.

The data is sent to the server using :
```
SOCKET.sendto(bytes(input, "utf-8"), (SERVER_IP, SERVER_PORT))
```

The data is received using :
```
data, addr = SOCKET.recvfrom(MESSAGES_LENGTH)
```

When we exit the game, the client finishes by closing the socket using the usual :
```
SOCKET.close()
```

### On the server-side, the code for UDP is now designed like this :

The initialization is :
```
MAINSOCKET = socket(AF_INET, SOCK_DGRAM)
MAINSOCKET.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Allows for the server to be reopened with the same ip immediately after being closed.
MAINSOCKET.settimeout(TIMEOUT)
MAINSOCKET.bind((HOST, PORT))
```

The server receives the data from clients with :
```
data, addr = MAINSOCKET.recvfrom(MESSAGES_LENGTH)
```

and send back data with :
```
MAINSOCKET.sendto(bytes(out,'utf-8'), addr)
```

However, we give each client a dedicated socket (linked to a given port) to talk to :
```
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
```
SERVER_PORT = int(portStr)
```
With `portStr` being the extract of the connection message (the second word of the answer).

After that, clients sends their messages to their own dedicated socket. We detect on the server side which sockets have received data using the lines :
```
sockets = [MAINSOCKET] + [dicoSocket[addr][0] for addr in dicoSocket]

if sockets != []:
    inSockets, _, _ = select.select(sockets, [], [], TIMEOUT)
```
Because the select module allows to efficiently (low level) keep only sockets that have received data.

Once sockets that have received data has been selected, a for loop on them to apply the usual reception and answering code allows for each client to send their inputs and receive the new state of the game.

Finally, don't forget to close every sockets before completely closing the server, including the MAINSOCKET.
When a client disconnect, its socket can be closed as well and its port can be add back in the available ports list:
```
availablePorts.append(port)
sock.close()
```

## Future Improvements to do...
To keep on improving the performances of the online system, we worked on a thread based system in which both clients and the server would have one thread to listen for messages, and one thread to send their messages. In this scenario, the server sends automatically every few milliseconds the current state of the game to every client connected to the server, while each client sends their input continuously.

Another way to improve the ping that we did not implement yet is to make clients stop sending permanently all their inputs. Instead, clients would only send their new inputs when the player changes input. This way, the server would receive way less messages and it would instead store the last input made by each player, and assume it is their current input as long as they do not send any other input.
This would work by sending a rack of several messages when changing input to be sure the server has correctly received it, and by asking for a confirmation.
In this case, the server would make the state of the game update every X ms, with the stored inputs of every player, and automatically send back to everyone the new state of the game.

Finally, another way to make the game look a lot smoother would be to let clients assume and compute the next frames of the game without waiting for the actual computations of the server. This could help make the game look smoother even when the connection is not stable.