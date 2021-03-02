import socket
import select
import msvcrt

IP = '127.0.0.1'
PORT = 5555

""" the name length and message will be 3 digit numbers (which means they are limited to a max length of 999) and 2 will be 002"""

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect((IP, PORT))
print("Connected to localhost on port {}".format(PORT))

sock_list = [my_socket]
messages = []
text = []

print("Enter message to the chat whenever you want, enter exit to disconnect")

while True:
    rlist, wlist, xlist = select.select(sock_list, sock_list, [])

    if rlist:
        # print('hola')
        message = my_socket.recv(2048).decode()
        print(message)
        if message == "Kicked":
            break

    if msvcrt.kbhit():
        data = msvcrt.getch().decode()
        # print(data)
        # if data == "":
        # break
        print(data, end='', flush=True)
        # print(data)
        # print("hola")
        if data == '\r':
            if ''.join(text) == 'exit':
                break
            elif ''.join(text) == 'quit':
                if wlist:
                    my_socket.send(''.join(text).encode())
                    break
            messages.append(''.join(text) + '\n')
            text = []
            # print("$$", messages, "$$")
        else:
            text.append(data)

    if wlist:
        for m in messages:
            my_socket.send(m.encode())
            messages.remove(m)

print("closing")
my_socket.close()
