import socket
import os

HOST = "127.0.0.1"
PORT = 65432
_file = "input.txt"
# _file      là *.txt tên các file cần tải
# file_names là [] nhận được sau khi đọc


def sendFileRequire(client_socket, _file): #nghe đá đá -> ai đó hãy sửa lại
    with open(_file, "r") as f:
        while True:
            file_datas = f.read()
            if not file_datas:
                break
            client_socket.send(file_datas.encode('utf-8'))


def readInput(_file):
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


def receiveFile(client_socket, file_names):
    for i in file_names:
        if not isValidFile(file_names, file_names[i]):
            continue

        received_size = 0
        file_size = client_socket.recv(1024)
        with open(file_names[i], "wb") as f:
            while received_size < file_size:
                data = client_socket.recv(1024)
                if not data:
                    break
                f.write(data)
                received_size += 1024

                # Progressing bar
                progress = (received_size / file_size) * 100
                print(f'Downloading {file_names[i]} .... {progress:.2f}%')
        
        # Receive EOF
        data = client_socket.recv(1024) # thấy insecure chỗ này s s
        buf = data.decode('utf-8')
        if buf == "---///---///---///==":
            pass


def isValidFile(file_names, file):
    # Check whether the file exists in the file list
    if file not in file_names:
        return False

    # Check whether the file has been downloaded
    program_path = os.getcwd()
    file_path = os.path.join(program_path, file)
    if os.path.exists(file_path):
        return False
    
    # File is valid to download
    return True


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)
    client_socket.connect(server_address)

    try:
        while True:
            file_names = readInput(_file) #lỡ đặt biến cục bộ r, nếu fix thì báo lại nhé
            receiveFile(client_socket, file_names)
    except KeyboardInterrupt:
        client_socket.close()
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
