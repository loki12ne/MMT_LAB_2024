#sever
import socket 

HOST = "127.0.0.1"
PORT = 65422


def sendFileList(client_socket):
    with open("data.txt", "r") as file:
       while True:
            chunk = file.read()  
            if not chunk:
                break  
            client_socket.send(bytes(chunk, "utf8"))
    client_socket.send(b"File read complete")

#nhan ten file roi gui
def sendMultipleFile(client_socket):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            file_name = data.decode("utf8")
            try:
                with open(file_name, "rb") as file:
                    data = file.read()
                    client_socket.send(data)
            except FileNotFoundError:
                print(f"File {file_name} not found on the server.")
            client_socket.send(b"File read complete")
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
            sendMultipleFile(client_socket)

    except KeyboardInterrupt:
        client_socket.close()
    finally:
        client_socket.close()

   
if __name__ == "__main__":
    main()
