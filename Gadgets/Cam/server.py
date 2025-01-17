import subprocess

# Script a ser executado
SCRIPT = """
import cv2
import numpy as np
from http.server import BaseHTTPRequestHandler, HTTPServer

# Classe para manipular as requisições HTTP
class WebcamHandler(BaseHTTPRequestHandler):
    
    # Método para lidar com as requisições GET
    def do_GET(self):
        # Verifica se a URL acessada é "/shot.jpg"
        if self.path == '/shot.jpg':
            # Captura o frame da câmera
            ret, frame = cap.read()
            if ret:
                # Codifica o frame para JPEG
                ret, jpeg = cv2.imencode('.jpg', frame)
                # Define o cabeçalho da resposta HTTP
                self.send_response(200)
                self.send_header('Content-type', 'image/jpeg')
                self.end_headers()
                # Envia o conteúdo do frame como resposta
                self.wfile.write(jpeg.tobytes())
            else:
                self.send_error(500, 'Erro ao capturar o frame da câmera')
        else:
            self.send_error(404, 'Recurso não encontrado')

# Inicia a captura da câmera
cap = cv2.VideoCapture(0)

# Define o endereço IP e a porta do servidor
server_address = ('', 7272)

# Cria uma instância do servidor HTTP
httpd = HTTPServer(server_address, WebcamHandler)

# Inicia o servidor e o mantém em execução
httpd.serve_forever()
"""

# Inicia o servidor assim que o script é iniciado
subprocess.Popen(['python3', '-c', SCRIPT])
