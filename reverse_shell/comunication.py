import socket
import zipfile
import os
import sys
import subprocess
import platform

class Setup:
    def compactar_diretorio(self, diretorio, arquivo_saida):
        with zipfile.ZipFile(arquivo_saida, 'w') as zipf:
            for raiz, _, arquivos in os.walk(diretorio):
                for arquivo in arquivos:
                    caminho_completo = os.path.join(raiz, arquivo)
                    relativo = os.path.relpath(caminho_completo, diretorio)
                    zipf.write(caminho_completo, relativo)

    def clear_zip(self):
        zip_file = "received_file.zip"
        if os.path.isfile(zip_file):
            os.remove(zip_file)

    def server(self):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(('127.0.0.1', 8887))
            server.listen(1)

            print('\nWaiting for a connection...\n')
            connection, address = server.accept()
            print(f'\nConnection from {address}\n')

            diretorio_cliente = connection.recv(1024).decode()

            if not os.path.exists(diretorio_cliente) or not os.path.isdir(diretorio_cliente):
                print(f"\nDirectory '{diretorio_cliente}' does not exist or is not a directory.\n")
                connection.close()
                server.close()
                exit()

            arquivo_zip_saida = 'received_file.zip'
            self.compactar_diretorio(diretorio_cliente, arquivo_zip_saida)

            if os.path.getsize(arquivo_zip_saida) == 0:
                print(f"\nFailed to create ZIP file for directory '{diretorio_cliente}'.\n")
                connection.close()
                server.close()
                exit()

            with open(arquivo_zip_saida, 'rb') as file:
                while True:
                    data = file.read(4096)
                    if not data:
                        break
                    connection.sendall(data)

            print('\n[+] ZIP file sent.\n')
            server.close()
            self.clear_zip()

        except Exception as e:
            print("ERROR: ", e)

    def client(self):
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
                            print(f"There is no directory {directory_name} found.")
                            break
                        if data:
                            file.write(data)
                            print(f'File received as received_file.zip [ok]')
                            client.close()
                            break
        except Exception as e:
            print("Closing connection with the server: ", e)
        except FileNotFoundError:
            print(f"There is no directory {directory_name} found.")
        
    def netcat_installation(self):
        try:
            os_name = platform.system()
            os_version = platform.version()
            print(f"""\n##########
                  
Netcat installation process started on OS: {os_name} version: {os_version}.

##########\n""")

            if os_name == 'Linux':
                print(f"\n[!] Starting Ncat installation on {os_name}...\n")
                subprocess.run("sudo apt install netcat -y", shell=True)
                print("\n[!] Netcat installation completed.")

            elif os_name == 'Windows':
                print(f"\n[!] Starting Netcat installation on {os_name}...\n")
                subprocess.run("winget install Insecure.Nmap", shell=True)
                print("\n[!] Netcat installation completed.")


        except Exception as e:
            print("\n[ERROR] Installation error: ", e)


class Menu:
    def __init__(self):
        self.system = Setup()

    def exit(self):
        sys.exit()

    def show_panel(self):
        try:
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')

                panel = [
                    """\n###############

MENU PANEL USAGE:

1. Activate Server on 8887 port;
2. Activate Client on 8889 port;
3. Netcat installation;
4. Exit

###############

Choose: """
                ]
                try:
                    result = int(input(panel[0]))
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue

                if result == 1:
                    self.system.server()
                elif result == 2:
                    self.system.client()
                elif result == 3:
                    self.system.netcat_installation()
                elif result == 4:
                    self.exit()

        except Exception as e:
            print("\nProgram failed", e)
        except KeyboardInterrupt:
            print("\nFinishing the program...")

menu_run = Menu()
menu_run.show_panel()
