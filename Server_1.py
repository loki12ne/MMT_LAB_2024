#sever
import socket 
import os
import time
import struct
import threading
HOST = "127.0.0.1"
PORT = 65432

is_working = True

borderline = "---///---/ongquatronroido//--xichlendumtuidi-///=="
borderline_b = borderline.encode('utf-8')
end_border = 8

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

def sizeFile(file_name):
    with open(file_name, "rb") as file:
        file.seek(0, 2)
        file_size = file.tell()
        file.close()
    return file_size


def sendFile(client_socket, file_name):

    size = sizeFile(file_name)
    # try:
    with open(file_name, "rb") as file:
        file_size_bytes = struct.pack('!I', size)
        client_socket.sendall(file_size_bytes)

        while True:
            data = file.read(10240)
            if not data:
                break
            client_socket.sendall(data)
                            

def sendMultipleFile(client_socket, file_names):
    try:
        for file_name in file_names:
            sendFile(client_socket, file_name)
    except KeyboardInterrupt:
        client_socket.close()

def receiveRequest(client_socket):
    data = ""
    while True:
        chunk = client_socket.recv(1024).decode('utf-8')
        if not chunk: 
            break
        if "client_close" in chunk:
            client_socket.close()
        if borderline in chunk:
            data += chunk.split(borderline, 1)[0]
            break   
        data += chunk
    file_names = extractRequest(data)
    return file_names

def extractRequest(chunk):  
    lines = chunk.strip().split('\n')
    file_names = []
    
    for line in lines:
        name = line.strip()
        if name:
            file_names.append(name)
    
    return file_names

############################################################################################################################


############################################################################################################################

def serveClient(client_socket):
    #global is_working
    global end_border
    try:
        while is_working:
            file_names = receiveRequest(client_socket)
            if not file_names:
                continue
            sendMultipleFile(client_socket, file_names)
    except (KeyboardInterrupt, socket.error, Exception, ConnectionResetError):
        pass
    finally:
        client_socket.close()
        client_socket.close()
        delete(end_border, end_border, 1, 111)
        disClient(end_border)
        end_border += 1
        endBorder(end_border)

############################################################################################################################

# Interface zone

############################################################################################################################

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
    delete(1, 7, 1, 111)
    title()
    gotoxy(29, 3)
    print(f"Server's IP: {HOST}:{PORT}")
    gotoxy(1, 6)
    print("█░")
    gotoxy(4, 6)
    print("Connecting Status")
    gotoxy(4, 7)
    print("-----------------")
    gotoxy(1, 7)
    print("█░")
    gotoxy(110, 7)
    print("░█")
    gotoxy(110, 6)
    print("░█")

def endBorder(y):
    gotoxy(1, y)
    print("█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█")

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
    hide_cursor()
    global is_working
    global end_border
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    os.system('cls' if os.name == 'nt' else 'clear')
    Lobby()
    endBorder(end_border)
    
    try:
        while is_working:
            client_socket, client_address = server_socket.accept()
            Lobby()
            if is_working:
                delete(end_border, end_border, 1, 111)
                clientConnect(end_border, client_address)
                end_border += 1
                endBorder(end_border)
                sendFileList(client_socket) 
                serveClient(client_socket)
    except (KeyboardInterrupt, socket.error, Exception, ConnectionResetError):
        is_working = False
    finally:
        is_working = False
        server_socket.close()
        client_socket.close()
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



