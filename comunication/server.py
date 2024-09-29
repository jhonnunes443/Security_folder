import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(('192.168.1.118', 8080))
print('Connected [!]\n')

# Prompt for a valid directory to zip
directory_name = input('Enter the directory to zip> ')
client.send(directory_name.encode())

# Receive the ZIP file
with open('received_file.zip', 'wb') as file:
    while True:
        data = client.recv(4096)
        if not data:
            break
        file.write(data)

print(f'File received as received_file.zip [ok]')
client.close()
