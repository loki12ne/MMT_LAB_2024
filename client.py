import socket
import os

HOST = "127.0.0.1"
PORT = 65432


# file_names và file_sizes là 2 mảng nhận được sau khi đọc
# danh sách các file từ server
def receiveFile(client_socket, file_names, file_sizes):
    for i in file_names:
        if not isValidFile(file_names, file_names[i]):
            return

        received_size = 0
        with open(file_names[i], "wb") as file:
            while received_size < file_sizes[i]:
                data = client_socket.recv(1024)
                if not data:
                    break
                file.write(data)
                received_size += 1024
            # 
    

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
            # HÀM ĐỌC FILE -> return file_names[], file_sizes[]
            # =====================================================
            file_names = ["File1.zip", "File2.zip"] #ảo
            file_sizes = [15, 25]                   #ảo
            # =====================================================
            receiveFile(client_socket, file_names, file_sizes)
    except KeyboardInterrupt:
        client_socket.close()
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
