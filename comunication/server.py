import socket
import zipfile
import os

def compactar_diretorio(diretorio, arquivo_saida):
    with zipfile.ZipFile(arquivo_saida, 'w') as zipf:
        for raiz, _, arquivos in os.walk(diretorio):
            for arquivo in arquivos:
                caminho_completo = os.path.join(raiz, arquivo)
                relativo = os.path.relpath(caminho_completo, diretorio)
                zipf.write(caminho_completo, relativo)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# server ip address and port 

server.bind(('192.168.1.118', 8080))
server.listen(1)

print('Waiting for a connection...')
connection, address = server.accept()
print(f'Connection from {address}')

# Receives the name of the directory to be zipped
diretorio_cliente = connection.recv(1024).decode()

# Check if the directory exists
if not os.path.exists(diretorio_cliente) or not os.path.isdir(diretorio_cliente):
    print(f"Directory '{diretorio_cliente}' does not exist or is not a directory.")
    connection.close()
    server.close()
    exit()

# Name of the output ZIP file
arquivo_zip_saida = 'arquivo_enviado.zip'

# Compact the client's directory
compactar_diretorio(diretorio_cliente, arquivo_zip_saida)

# Check if the ZIP file was created successfully
if os.path.getsize(arquivo_zip_saida) == 0:
    print(f"Failed to create ZIP file for directory '{diretorio_cliente}'.")
    connection.close()
    server.close()
    exit()

# Send the ZIP file
with open(arquivo_zip_saida, 'rb') as file:
    while True:
        data = file.read(4096)  # Read in chunks
        if not data:
            break
        connection.sendall(data)  # Send data in chunks

print('ZIP file sent.')
server.close()
