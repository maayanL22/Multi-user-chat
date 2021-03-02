import socket
import select
import datetime

MAX_MSG_LENGTH = 5000
SERVER_PORT = 5555
SERVER_IP = '0.0.0.0'
MANAGERS = ['Maayan']
CLIENTS = []
SILENCED = []

""" the name length and message will be 3 digit numbers (which means they are limited to a max length of 999) """

def print_client_sockets(clients_sockets):
    for c in clients_sockets:
        print("\t", c.getpeername())


def get_socket_by_name(n):
    for client in CLIENTS:
        cname, csocket = client
        print("name", cname, "socket", csocket)
        if cname == n:
            return csocket
    return ""


print("Setting up server...")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()
print("Listening for clients...")

client_sockets = []
messages_to_send = []

while True:
    rlist, wlist, xlist = select.select([server_socket] + client_sockets, client_sockets, [])
    for current_socket in rlist:
        if current_socket is server_socket:
            connection, client_address = current_socket.accept()
            print("New client joined!", client_address)
            client_sockets.append(connection)
            print_client_sockets(client_sockets)
        else:
            data = current_socket.recv(MAX_MSG_LENGTH).decode()
            if data == "" or data == "quit" or data == "\n" or data == "quit\n":
                print("Connection closed", )
                client_sockets.remove(current_socket)
                current_socket.close()
                print_client_sockets(client_sockets)
            elif not data[:3].isnumeric():
                if current_socket in wlist:
                    current_socket.send("invalid message".encode())
            else:
                if len(data) < 3:
                    if current_socket in wlist:
                        current_socket.send("Invalid message".encode())
                name_length = int(data[:3])
                name1 = data[3:3 + name_length]
                print(type(name1))
                print(name1)
                if name1 in MANAGERS:
                    name = '@' + name1
                else:
                    name = name1
                if (name1, current_socket) not in CLIENTS:
                    CLIENTS.append((name1, current_socket))
                if len(data) <= 4 + name_length:
                    if current_socket in wlist:
                        current_socket.send("Invalid message".encode())
                    continue
                ordernum = int(data[3 + name_length])
                if name1 in SILENCED:
                    if current_socket in wlist:
                        current_socket.send("You were silenced by a manager".encode())
                elif ordernum == 1:
                    if name in SILENCED:
                        if current_socket in wlist:
                            current_socket.send("you are silenced".encode())
                    else:
                        messagedata = data[4 + name_length:]
                        meslength = messagedata[:3]
                        msg = messagedata[3:]
                        now = datetime.datetime.now()
                        hour = str(now.hour)
                        minute = str(now.minute)
                        if len(hour) == 1:
                            hour = "0" + hour
                        if len(minute) == 1:
                            minute = "0" + minute
                        timetoshow = hour + ':' + minute
                        finalmsg = timetoshow + " " + name + ": " + msg
                        messages_to_send.append((current_socket, finalmsg))
                elif ordernum == 2:
                    if name1 not in MANAGERS:
                        if current_socket in wlist:
                            current_socket.send("You are not a manager and therefore cannot promote".encode())
                    else:
                        messagedata = data[4 + name_length:]
                        meslength = messagedata[:3]
                        lng = len(messagedata)
                        msg = messagedata[3:lng - 1]
                        now = datetime.datetime.now()
                        if get_socket_by_name(msg) == "":
                            if current_socket in wlist:
                                current_socket.send("Invalid order".encode())
                        else:
                            timetoshow = str(now.hour) + ':' + str(now.minute)
                            finalmsg = timetoshow + " " + msg + " has been promoted and is now a manager"
                            MANAGERS.append(msg)
                            messages_to_send.append((current_socket, finalmsg))
                elif ordernum == 3:
                    if name1 not in MANAGERS:
                        if current_socket in wlist:
                            current_socket.send("You are not a manager and therefore cannot kick anyone".encode())
                    else:
                        messagedata = data[4 + name_length:]
                        meslength = messagedata[:3]
                        lng = len(messagedata)
                        msg = messagedata[3:lng - 1]  # name of member to kick
                        print(msg)
                        if get_socket_by_name(msg) == "":
                            if current_socket in wlist:
                                current_socket.send("Invalid order".encode())
                        else:
                            now = datetime.datetime.now()
                            timetoshow = str(now.hour) + ':' + str(now.minute)
                            sock = get_socket_by_name(msg)
                            messages_to_send.append((current_socket, timetoshow + " " + msg + " has been kicked from "
                                                                                              "the chat!"))
                            if sock in wlist:
                                sock.send("Kicked".encode())
                            if msg in MANAGERS:
                                MANAGERS.remove(msg)
                            CLIENTS.remove((msg, sock))
                            client_sockets.remove(sock)
                            rlist, wlist, xlist = select.select([server_socket] + client_sockets, client_sockets, [])
                            sock.close()
                elif ordernum == 4:
                    if name1 not in MANAGERS:
                        if current_socket in wlist:
                            current_socket.send("You are not a manager and therefore cannot silence anyone".encode())
                    else:
                        messagedata = data[4 + name_length:]
                        meslength = messagedata[:3]
                        lng = len(messagedata)
                        msg = messagedata[3:lng - 1]  # name of member to silence
                        if get_socket_by_name(msg) == "":
                            messages_to_send.append((current_socket, "Invalid order"))
                        else:
                            SILENCED.append(msg)
                            now = datetime.datetime.now()
                            timetoshow = str(now.hour) + ':' + str(now.minute)
                            messages_to_send.append((current_socket, timetoshow + " " + msg + " has been silenced"
                                                                      ))
                elif ordernum == 5:
                    messagedata = data[4 + name_length:]
                    if not messagedata[:3].isnumeric():
                        if current_socket in wlist:
                            current_socket.send("Invalid message".encode())
                        continue
                    nlength = int(messagedata[:3])
                    gettername = messagedata[3:3 + nlength]
                    print(gettername)
                    if get_socket_by_name(gettername) == "":
                        messages_to_send.append((current_socket, "Invalid order"))
                    else:
                        mdata = data[4 + name_length + 3 + nlength:]
                        mlength = mdata[:3]
                        lng = len(messagedata)
                        msg1 = mdata[3:lng - 1]
                        sock = get_socket_by_name(gettername)
                        now = datetime.datetime.now()
                        timetoshow = str(now.hour) + ':' + str(now.minute)
                        if sock in wlist:
                            sock.send((timetoshow + " !" + name1 + ": " + msg1).encode())
                else:
                    if current_socket in wlist:
                        current_socket.send("Invalid order")

    for message in messages_to_send:
        current_socket, data = message
        for c_socket in wlist:
            c_socket.send(data.encode())
        messages_to_send.remove(message)


