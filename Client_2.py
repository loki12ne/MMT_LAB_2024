import socket 
import os 
import sys
import threading 
import time
import struct

HOST = "127.0.0.1"
PORT = 65432
_file = "input.txt"

download_path = "D:\HCMUS\HK3\MMT\SOCKET_test\download"
borderline = "---///---/ongquatronroido//--xichlendumtuidi-///=="
borderline_b = borderline.encode('utf-8')

downloading_file = []
files_to_download = []

stop_thread = False

end_list = 0
noti_cnt = 0
end_border  = 0

priority_spd = {
    'CRITICAL': 10,
    'HIGH': 4,
    'NORMAL': 1,
}

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
    global stop_thread
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

    if file_names:
        file_list = getFileList(file_names)
    FileList(file_names)
    return file_list

def readInput():
    try:
        with open(_file, "r") as f:
            lines = f.readlines()
        files_to_download = []
        for line in lines:
            filename, priority = line.strip().split()
            files_to_download.append((filename, priority))
    except FileNotFoundError:
        print(f"File {outName(_file)} not found.")
    return files_to_download

def sendRequest(client_socket, files_to_download): 
    for (filename, priority) in files_to_download:                       
        client_socket.send(filename.encode('utf-8'))    
        client_socket.send('\n'.encode('utf-8'))  
    client_socket.send(borderline_b)  

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

# Receive File

############################################################################################################################


def getCursor(filename):
    try:
        file_path = os.path.join(download_path, filename)
        with open(file_path, "rb") as f:
            f.seek(0, os.SEEK_END)
            cursor = f.tell()
            f.close()
            return cursor
    except FileNotFoundError:
        return 0

def writeFile(client_socket, filename, size_next_chunk):
    program_path = download_path
    file_path = os.path.join(program_path, filename)
    with open (file_path, "ab") as f:
        while size_next_chunk > 0:
            data = client_socket.recv(size_next_chunk)
            if not data:
                return
            f.write(data)
            size_next_chunk -= len(data)
    f.close()

def receiveFile(client_socket):
    global files_to_download
    global stop_thread
    downloading_file ={}
    cnt = 0
    try:
        while not stop_thread:
            if files_to_download:
                for (filename, priority) in files_to_download:
                    download_spd = int(priority_spd.get(priority, 1))
                    downloading_file[filename] = (download_spd, 0, 0, cnt, 0)
                    cnt += 1
                files_to_download = []

            recheck = {}

            temp = cnt
            cnt = 0
            for filename, (download_spd, file_size,percent, y, status) in downloading_file.items(): 
                if status == 0:
                    recheck[filename] = download_spd, file_size,percent, cnt, status
                    cnt += 1
            downloading_file = recheck
            
            if not downloading_file:
                time.sleep(1)
                client_socket.sendall(b'\x00' * 1024)

            if cnt < temp:
                delete(8, end_list - 4, 62, 109)

            for filename, (download_spd, file_size,percent, y, status) in downloading_file.items(): 
                if status == 1:
                    DownloadingBar(y)
                    print(f"{outName(filename)} ... {percent}%")
                    downloading_file.pop(filename, None)
                    continue
                cursor = getCursor(filename) 
                if cursor == 0:
                        sending_data = filename + ' ' + str(cursor) + ' ' + str(1)
                        client_socket.send((sending_data.encode("utf-8").ljust(1024, b'\x00')))
                        file_size_bytes = client_socket.recv(4)
                        file_size = struct.unpack('!I', file_size_bytes)[0]
                        downloading_file[filename] = (download_spd, file_size, 0, y, 0)

                for _ in range ((download_spd)):  
                    
                    cursor = getCursor(filename)
                    if cursor >= file_size:
                        downloading_file[filename] = (download_spd, file_size, 100, y, 1)
                        break
                    
                    if cursor + 102400 > file_size:
                        size_next_chunk = (file_size - cursor )
                    else:
                        size_next_chunk = 102400

                    sending_data = filename + ' ' + str(cursor) + ' ' + str(size_next_chunk)
                    client_socket.send((sending_data.encode("utf-8").ljust(1024, b'\x00')))
                    percent = round(cursor/file_size*100)

                    DownloadingBar(y)
                    print(f"{outName(filename)} ... {percent}%")
                    writeFile(client_socket, filename, size_next_chunk)
    except (KeyboardInterrupt, socket.error, Exception, ConnectionResetError):
        stop_thread = True
    finally:
        stop_thread = True
        client_socket.send((("stop_client").encode("utf-8").ljust(1024, b'\x00')))
        client_socket.close()

############################################################################################################################

# Update Receive File

############################################################################################################################

def checkUpdate(file_list):
    global files_to_download
    global stop_thread
    global noti_cnt
    while not stop_thread:
        files = readInput()
        data_return = []
        for (filename, priority) in files:
            if isValidFile(file_list, filename):
                data_return.append((filename, priority))
        if data_return: 
            files_to_download = data_return
            delete(noti_cnt, len(data_return) + noti_cnt, 1, max(len(s) for s in data_return))

        endBorder(noti_cnt + end_list)
        
        time.sleep(2)

        delete(end_list, noti_cnt + end_list, 1, 120)
        noti_cnt = 0


############################################################################################################################

# Interface zone

############################################################################################################################

def endBorder(y):
    gotoxy(1, y)
    print("█░")
    gotoxy(110, y)
    print("░█")
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
    os.system('cls' if os.name == 'nt' else 'clear')
    #(1,1) -> (23, 3)
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
    for i in file_names:
        gotoxy(1, end_list + 8)
        print("█░")
        gotoxy(110, end_list + 8)
        print("░█")
        gotoxy(59, end_list + 8)
        print("█")
        gotoxy(4, end_list + 8)
        print(outName(i))
        end_list += 1
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
    max_length = 12
    if len(name) > (max_length + 3):
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
    global files_to_download
    global stop_thread
    global noti_cnt

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)
    client_socket.connect(server_address)
    Lobby()

    try:
        file_list = receiveFileList(client_socket) 
        threads = threading.Thread(target=checkUpdate, args=(file_list,))
        threads.start()
        receiveFile(client_socket)
    except (Exception, ConnectionResetError, BrokenPipeError, KeyboardInterrupt):
        stop_thread = True
    finally:
        stop_thread = True
        client_socket.close()
        disConnect()

if __name__ == "__main__":
    main()
