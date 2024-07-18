#sever
import socket 
import base64
HOST = "127.0.0.1"
PORT = 65421

def sendFileList(client_socket):
    with open("data.txt", "r") as file:
       while True:
            chunk = file.read(1024)  
            if not chunk:
                break  
            client_socket.send(chunk).encode("utf-8")
    client_socket.send("---///---///---///==").encode("utf-8")

def sizeFile(file_name):
    with open("data.txt", "r") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                filename, size = parts
            if filename == file_name:
                return size
    return -1

def sendMultipleFile(client_socket, file_names):
    try:
        for i in file_names:
            size = sizeFile(i)
            client_socket.send(size).encode("utf-8")

            while True:
                try:
                    with open(i, "rb") as file:
                        while True:
                            data = file.read(1024)
                            if not data:
                                break
                            client_socket.send(data).encode("base64")
                except FileNotFoundError:
                    print(f"File {i} not found on the server.")
                client_socket.send("---///---///---///==")
    except KeyboardInterrupt:
        client_socket.close()
    finally:
        client_socket.close()



def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
  
    try:
        while True: 
            print("Waiting for Client")
            client_socket, client_address = server_socket.accept() 
            print(f"Client connected from {client_address}")
            sendFileList(client_socket)
            file_names = []
            while True:
                file_name = client_socket.recv(1024).decode()  
                if not file_name:  
                    break
            file_names.append(file_name)
            sendMultipleFile(client_socket, file_names)

    except KeyboardInterrupt:
        client_socket.close()
    finally:
        client_socket.close()

   
if __name__ == "__main__":
    main()
