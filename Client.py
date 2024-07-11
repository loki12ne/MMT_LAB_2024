#client
import socket

HOST = "127.0.0.1"
PORT = 65422

def receiveFile(client_socket, file_name):
    with open(file_name, "wb") as file:
        data = client_socket.recv(1024)
        while data:
            file.write(data)
            if not data:
                break
            data = client_socket.recv(1024)
            
        print(f"Downloading {file_name}...")
    

def main():
    server_address = (HOST, PORT)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Client connect to server with port: " + str(PORT))
    client_socket.connect(server_address)

#connece to server

    data = client_socket.recv(1024)
    while data:
        print(data.decode("utf8"))
        data = client_socket.recv(1024)
        if not data:
            break



    try:
        while True:
            file_name = input('Client: ')
            client_socket.send(bytes(file_name, "utf8"))
            receiveFile(client_socket,file_name)
            print(f"Nhận tệp {file_name} thành công!")
    except KeyboardInterrupt:
        pass
    finally:
        client_socket.close()

    # file_name = "hahacaiqqjztr.txt"
    # receiveFile(client_socket, file_name)
    # client_socket.close()

if __name__ == "__main__":
    main()
