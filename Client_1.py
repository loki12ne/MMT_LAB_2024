import socket
import os
import struct
import sys
import time
import threading

HOST = "127.0.0.1"
PORT = 65432
_file = "input.txt"

download_path = "D:\HCMUS\HK3\MMT\SOCKET_test\download"
borderline = "---///---/ongquatronroido//--xichlendumtuidi-///=="
borderline_b = borderline.encode('utf-8')

client_live = True

end_list = 0
noti_cnt = 0
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

def gotoxy(x, y):
    print(f"\033[{y};{x}H", end='')

############################################################################################################################

# File List

############################################################################################################################

def sendRequest(client_socket, file_names): 
    for name in file_names:                       
        client_socket.send(name.encode('utf-8'))    
        client_socket.send('\n'.encode('utf-8'))  
    client_socket.send(borderline_b)  

def extractFileList(chunk):  
    lines = chunk.strip().split('\n')
    file_names = []
    
    for line in lines:
        file_name = line.strip()
        if file_name:
            file_names.append(file_name)
    return file_names

def getFileList(file_names):
    file_list = []
    for file_name in file_names:
        name, size = file_name.rsplit(' ', 1)
        file_list.append({"name": name, "size": (size)})
    return file_list

def receiveFileList(client_socket):
    data = ""
    while True:
        chunk = client_socket.recv(1024).decode('utf-8')
        if not chunk: 
            break
        if borderline in chunk:
            data += chunk.split(borderline, 1)[0]
            break
        data += chunk
    file_names = extractFileList(data)
    FileList(file_names)
    if file_names:
        file_list = getFileList(file_names)
    return file_list


############################################################################################################################

# Receive File

############################################################################################################################

def readInput():
    file_names = []
    try:
        with open(_file, 'r') as f:
            for line in f:
                buf = line.strip()
                if buf:
                    file_names.append(buf)
    except FileNotFoundError:
        print(f"File {_file} not found.")
    return file_names

def getSize(file_list, file_name):
    for file in file_list:
        if file["name"] == file_name:
            return file["size"]

def receiveFile(client_socket, file_names, file_list):
    global noti_cnt 
    data_return = []
    noti_cnt = 0
    for file_name in file_names:
        if isValidFile(file_list, file_name): 
            data_return.append(file_name)
    endBorder(end_border)
    file_names = data_return
    
    if not file_names:
        return False

    sendRequest(client_socket, file_names)
    delete(8, end_list - 4, 62, 109)
    count_inter = 0

    for file_name in file_names:
        received_size = 0        
        file_size_bytes = client_socket.recv(4)
        file_size = struct.unpack('!I', file_size_bytes)[0]
        file_path = os.path.join(download_path, file_name)
        with open(file_path, "wb") as f:
            while True:
                if received_size > file_size - 10240:
                    data = client_socket.recv(file_size - received_size)
                else:
                    data = client_socket.recv(10240)

                received_size += len(data)
                if not data:
                    break
                f.write(data)

                if received_size > file_size:
                    received_size = file_size
                progress = round((received_size / file_size) * 100)
                DownloadingBar(count_inter)
                print(f"{outName(file_name)} ... {progress}%")
                if (received_size == file_size):
                    break

        count_inter = count_inter + 1  
    return True

def isSupported(file_list, file):
    for i in file_list:
        if file == i["name"]:
            return True
    return False

def isValidFile(file_list, file): 
    global noti_cnt
    count = end_list + noti_cnt
    if not isSupported(file_list, file):
        gotoxy(1, count)
        print("█░")
        gotoxy(110, count)
        print("░█")
        gotoxy(4, count)
        print(f"{outName(file)} is not supported.")  
        noti_cnt += 1
        return False

    program_path = download_path
    file_path = os.path.join(program_path, file)
    if os.path.exists(file_path):
        gotoxy(1, count)
        print("█░")
        gotoxy(110, count)
        print("░█")
        gotoxy(4, count)
        print(f"{outName(file)} has already been downloaded.") 
        noti_cnt += 1
        return False
 
    return True

############################################################################################################################

# Time To Live 

############################################################################################################################

def checkLive(client_socket):
    global client_live
    try:
        while True:
            client_socket.send(borderline_b)  
            time.sleep(2)
    except (KeyboardInterrupt, socket.error):
        client_live = False
        return
    finally:
        client_live = False

        return
    
############################################################################################################################

# Interface zone

############################################################################################################################

def endBorder(y):
    gotoxy(1, y)
    print("█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█")

def title():
    gotoxy(1, 1)
    print("░█▀▀░█░░░▀█▀░█▀▀░█▀█░▀█▀░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
    gotoxy(1, 2)
    print("░█░░░█░░░░█░░█▀▀░█░█░░█░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
    gotoxy(1, 3)
    print("░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░░▀░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")

    gotoxy(1, 4)
    print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
    print("▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄")


def Lobby():
    title()
    gotoxy(29, 3)
    print(f"Connected from {HOST}:{PORT}")
    gotoxy(1, 6)
    print("█░")
    gotoxy(4, 6)
    print("File List")
    gotoxy(4, 7)
    print("---------")
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
    print("Downloading Progress")
    gotoxy(62, 7)
    print("--------------------")


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


def FileList(file_names):
    global end_list
    cnt = 0
    for i in file_names:
        if (cnt >= 6):
            gotoxy(1, end_list + 8)
            print("█░")
            gotoxy(110, end_list + 8)
            print("░█")
            gotoxy(59, end_list + 8)
            print("█")
            gotoxy(4, end_list + 8)
            print("...")
            end_list += 1
            break
        gotoxy(1, end_list + 8)
        print("█░")
        gotoxy(110, end_list + 8)
        print("░█")
        gotoxy(59, end_list + 8)
        print("█")
        gotoxy(4, end_list + 8)
        print(outName(i))
        end_list += 1
        cnt += 1
    end_list += 8
    gotoxy(1, end_list)
    Noti() 

def countOrder(file_list):
    return len(file_list)

def delete(y_st, y_end, x_st, x_end):
    while (y_st <= y_end):
        space = ' ' * (x_end - x_st)
        gotoxy(x_st, y_st)
        print(space)
        y_st += 1
    gotoxy(x_st, y_st)

def outName(name):
    cal_name = name.split(' ', 1)[0]
    max_length = 12
    if len(cal_name) > (max_length + 3):
        base_name, extension = name.rsplit('.', 1)
        truncated_base = '(' + base_name[:max_length] + '..)'
        return f"{truncated_base}.{extension}"
    else:
        return name

def Noti():
    global end_list
    print("█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█")
    end_list += 1
    gotoxy(1, end_list)
    print("█░")
    gotoxy(110, end_list)
    print("░█")
    gotoxy(4, end_list)
    print("Noti")
    gotoxy(4, end_list + 1)
    print("----")
    gotoxy(1, end_list + 1)
    print("█░")
    gotoxy(110, end_list + 1)
    print("░█")
    end_list += 2

def DownloadingBar(file):
    gotoxy(62, file + 8)

############################################################################################################################

############################################################################################################################

def main():
    hide_cursor()
    gotoxy(14, 5)
    print("ENABLE FULL SCREEN FOR BETTER EXPERIENCE")
    gotoxy(14, 6)
    print("ENTER WHEN YOU ARE READY")
    input()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)
    global client_live
    global end_border
    client_socket.connect(server_address)
    Lobby()

    try:    
        file_list = receiveFileList(client_socket) 
        end_border = (end_list - 12) * 2 + end_list
        for i in range(end_list, end_border):
            gotoxy(1, i)
            print("█░")
            gotoxy(110, i)
            print("░█")
        endBorder(end_border)

        check = threading.Thread(target=checkLive,args=(client_socket,))
        check.start()
        
        while client_live:
            file_names = readInput()
            if not file_names:
                client_socket.close()
                break
            receiveFile(client_socket, file_names, file_list)
              
    except (KeyboardInterrupt, socket.error):
        pass
    finally:
        try:
            client_socket.send("client_close".encode("utf8"))
        except (Exception):
            pass
        client_socket.close()
        disConnect()

if __name__ == "__main__":
    main()