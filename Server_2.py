import socket
import os
import threading
import struct
import time
import sys

HOST = "127.0.0.1"
PORT = 65432

download_path = "D:\HCMUS\HK3\MMT\SOCKET_test\download"
borderline = "---///---/ongquatronroido//--xichlendumtuidi-///=="
borderline_b = borderline.encode('utf-8')

is_working = True
limit = 8
connected_clients = []

############################################################################################################################

# System 

############################################################################################################################

if os.name == 'nt':
    import msvcrt
    import ctypes

    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int),
                    ("visible", ctypes.c_byte)]

def hide_cursor():
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

def gotoxy(x,y):
    print ("%c[%d;%df" % (0x1B, y, x), end='')

############################################################################################################################

# File List

############################################################################################################################

def sendFileList(client_socket):
    with open("data.txt", "r") as file:
       while True:
            chunk = file.read(1024)  
            if not chunk:
                break  
            client_socket.sendall(chunk.encode('utf-8'))
    client_socket.sendall(borderline.encode('utf-8'))
    file.close()

############################################################################################################################

# Send File

############################################################################################################################

def sendChunk(client_socket, filename, cursor, size_next_chunk):
    try:
        with open(filename, "rb") as f:
            f.seek(cursor)
            data = f.read(size_next_chunk)
            if not data: 
                pass # làm j ở đây bh
            
            client_socket.sendall(data)
    except FileNotFoundError:
        print(f"File {filename} not found.")

def sizeFile(file_name):
    with open(file_name, "rb") as file:
        file.seek(0, 2)
        file_size = file.tell()
        file.close()
    return file_size


def handleClient(client_socket, client_address):
    global limit
    global connected_clients
    sendFileList(client_socket)
    connected_clients.append(client_address)
    connectedClients()
    try:
        while True:
            data = (client_socket.recv(1024).decode('utf-8')).strip('\x00')
            if not data:
                continue

            if data == "stop_client":
                break

            filename, cursor_str, size_next_chunk_str = data.split(' ', 2)
            cursor = int(cursor_str)
            size_next_chunk = int(size_next_chunk_str)

            if cursor == 0:
                size = sizeFile(filename)
                size_bytes = struct.pack('!I', size)
                client_socket.sendall(size_bytes)
                        
                data = (client_socket.recv(1024).decode('utf-8')).strip('\x00')

                if not data:
                    break

                try:
                    filename, cursor_str, size_next_chunk_str = data.split(' ', 2)
                    cursor = int(cursor_str)
                    size_next_chunk = int(size_next_chunk_str)
                except ValueError:
                    break
                
            sendChunk(client_socket, filename, cursor, size_next_chunk)
    except (KeyboardInterrupt, socket.error, Exception, ConnectionResetError):
        client_socket.close()
    finally:
        delete(limit, limit, 1, 111)
        disClient(limit)
        limit += 1
        endBorder(limit)
        connected_clients.remove(client_address)
        connectedClients()
        client_socket.close()

############################################################################################################################

# Interface Zone

############################################################################################################################

def connectedClients():
    cnt = 8
    delete(8, limit - 1, 62, 109)
    for client in connected_clients:
        gotoxy(62, cnt)
        print(f"Client: {client}")
        cnt += 1

def title():
    gotoxy(1, 1)
    print("░█▀▀░█▀▀░█▀▄░█░█░█▀▀░█▀▄░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
    gotoxy(1, 2)
    print("░▀▀█░█▀▀░█▀▄░▀▄▀░█▀▀░█▀▄░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
    gotoxy(1, 3)
    print("░▀▀▀░▀▀▀░▀░▀░░▀░░▀▀▀░▀░▀░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")

    gotoxy(1, 4)
    print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
    print("▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄")

def Lobby():
    #(1,1) -> (23, 3)
    title()
    gotoxy(29, 3)
    print(f"Server's IP: {HOST}:{PORT}")
    gotoxy(1, 6)
    print("█░")
    gotoxy(4, 6)
    print("Noti")
    gotoxy(4, 7)
    print("----") 
    gotoxy(1, 7)
    print("█░")
    gotoxy(110, 7)
    print("░█")
    gotoxy(59, 6)
    print("█")
    gotoxy(59, 7)
    print("█")
    gotoxy(110, 6)
    print("░█")
    gotoxy(62, 6)
    print("Connecting Status")
    gotoxy(62, 7)
    print("-----------------")

def endBorder(y):
    gotoxy(59, y - 1)
    print("█")
    gotoxy(1, y)
    print("█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█")

def clientConnect(y, client_address):
    gotoxy(1, y)
    print("█░")
    gotoxy(110, y)
    print("░█")
    gotoxy(4, y)
    print(f"Client connected from {client_address}")

def disClient(y):
    gotoxy(1, y)
    print("█░")
    gotoxy(110, y)
    print("░█")
    gotoxy(4, y)
    print("Client disconnected.")

def disConnect():
    os.system('cls' if os.name == 'nt' else 'clear')
    title()
    gotoxy(10, 10)
    print("░█▀▄░▀█▀░█▀▀░█▀▀░█▀█░█▀█░█▀█░█▀▀░█▀▀░▀█▀░▀█▀░█▀█░█▀▀░░░░░░░░░")
    gotoxy(10, 11)
    print("░█░█░░█░░▀▀█░█░░░█░█░█░█░█░█░█▀▀░█░░░░█░░░█░░█░█░█░█░░░░░░░░░")
    gotoxy(10, 12)
    print("░▀▀░░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀░▀░▀▀▀░▀▀▀░░▀░░▀▀▀░▀░▀░▀▀▀░▀░░▀░░▀░")
    time.sleep(0.5)
    delete(10, 13, 10, 75)

    gotoxy(10, 10)
    print("░█▀▄░▀█▀░█▀▀░█▀▀░█▀█░█▀█░█▀█░█▀▀░█▀▀░▀█▀░▀█▀░█▀█░█▀▀░░░░░░")
    gotoxy(10, 11)
    print("░█░█░░█░░▀▀█░█░░░█░█░█░█░█░█░█▀▀░█░░░░█░░░█░░█░█░█░█░░░░░░")
    gotoxy(10, 12)
    print("░▀▀░░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀░▀░▀▀▀░▀▀▀░░▀░░▀▀▀░▀░▀░▀▀▀░▀░░▀░")
    time.sleep(0.5)
    delete(10, 13, 10, 75)

    gotoxy(10, 10)
    print("░█▀▄░▀█▀░█▀▀░█▀▀░█▀█░█▀█░█▀█░█▀▀░█▀▀░▀█▀░▀█▀░█▀█░█▀▀░░░")
    gotoxy(10, 11)
    print("░█░█░░█░░▀▀█░█░░░█░█░█░█░█░█░█▀▀░█░░░░█░░░█░░█░█░█░█░░░")
    gotoxy(10, 12)
    print("░▀▀░░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀░▀░▀▀▀░▀▀▀░░▀░░▀▀▀░▀░▀░▀▀▀░▀░")
    time.sleep(0.5)
    delete(10, 13, 10, 75)

    gotoxy(10, 10)
    print("░█▀▄░▀█▀░█▀▀░█▀▀░█▀█░█▀█░█▀█░█▀▀░█▀▀░▀█▀░▀█▀░█▀█░█▀▀░░░░░░")
    gotoxy(10, 11)
    print("░█░█░░█░░▀▀█░█░░░█░█░█░█░█░█░█▀▀░█░░░░█░░░█░░█░█░█░█░░░░░░")
    gotoxy(10, 12)
    print("░▀▀░░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀░▀░▀▀▀░▀▀▀░░▀░░▀▀▀░▀░▀░▀▀▀░▀░░▀░")
    time.sleep(0.5)
    delete(10, 13, 10, 75)

    gotoxy(10, 10)
    print("░█▀▄░▀█▀░█▀▀░█▀▀░█▀█░█▀█░█▀█░█▀▀░█▀▀░▀█▀░▀█▀░█▀█░█▀▀░░░░░░░░░")
    gotoxy(10, 11)
    print("░█░█░░█░░▀▀█░█░░░█░█░█░█░█░█░█▀▀░█░░░░█░░░█░░█░█░█░█░░░░░░░░░")
    gotoxy(10, 12)
    print("░▀▀░░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀░▀░▀▀▀░▀▀▀░░▀░░▀▀▀░▀░▀░▀▀▀░▀░░▀░░▀░")
    time.sleep(0.5)
    delete(10, 13, 10, 75)

    gotoxy(10, 10)
    print("░█▀▄░▀█▀░█▀▀░█▀▀░█▀█░█▀█░█▀█░█▀▀░█▀▀░▀█▀░█▀▀░█▀▄░░░")
    gotoxy(10, 11)
    print("░█░█░░█░░▀▀█░█░░░█░█░█░█░█░█░█▀▀░█░░░░█░░█▀▀░█░█░░░")
    gotoxy(10, 12)
    print("░▀▀░░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀░▀░▀▀▀░▀▀▀░░▀░░▀▀▀░▀▀░░▀░")
    time.sleep(0.5)

def delete(y_st, y_end, x_st, x_end):
    y = y_st
    while (y <= y_end):
        space = ' ' * (x_end - x_st)
        gotoxy(x_st, y)
        print(space)
        y += 1
    gotoxy(x_st, y_st)

############################################################################################################################


############################################################################################################################

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    hide_cursor()
    global is_working
    global limit
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    Lobby()
    endBorder(limit)
    clients = []
    try:
        while is_working:
            client_socket, client_address = server_socket.accept()
            clients.append(client_socket)
            Lobby()
            delete(limit, limit, 1, 111)
            clientConnect(limit, client_address)
            limit += 1
            endBorder(limit) 
            if is_working:
                client_thread = threading.Thread(target=handleClient, args=(client_socket,client_address,))
                client_thread.start()       
    finally:
        for client in clients:
            client.close()
        server_socket.close()
        disConnect()


if __name__ == "__main__":
    try:
        start_server = threading.Thread(target=main)
        start_server.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        is_working = False
    finally:
        is_working = False
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        client_socket.close()

