#sever
import socket 

HOST = "127.0.0.1"
PORT = 65422

def sendFileList(client_socket):
    with open("data.txt", "r") as file:
       while True:
            chunk = file.read(1024)  
            if not chunk:
                break  
            client_socket.send(bytes(chunk, "utf8"))
    client_socket.send(b"File read complete")

def sendFile(client_socket, file_name):
    try:
        with open(file_name, "rb") as file:
            data = file.read()
            client_socket.send(data)
    except FileNotFoundError:
        print(f"File {file_name} not found on the server.")
    client_socket.send(b"File read complete")

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
            print("hehe")
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                file_name = data.decode("utf8")
                print(f"Received file name: {file_name}")
                sendFile(client_socket, file_name)
                print(f"Sent file {file_name} successfully!")
                
    except KeyboardInterrupt:
            client_socket.close()
    finally:
            client_socket.close()

   
if __name__ == "__main__":
    main()