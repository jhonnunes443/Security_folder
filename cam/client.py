import tkinter as tk
import requests
import numpy as np 
import cv2

# Função para capturar o vídeo do servidor
def capture_video():
    # Obtém o endereço IP e a porta inseridos pelo usuário
    ip_address = ip_entry.get()
    port = port_entry.get()
    
    # Monta a URL do feed de vídeo
    url = f"http://{ip_address}:{port}/shot.jpg"
    
    # Loop para capturar e exibir o vídeo
    while True:
        try:
            # Requisição ao servidor para obter o próximo frame
            response = requests.get(url)
            
            # Converte o conteúdo da resposta em uma imagem
            video = np.array(bytearray(response.content), dtype=np.uint8)
            render = cv2.imdecode(video, -1)
            
            # Exibe o frame na janela
            cv2.imshow('frame', render)
            
            # Verifica se o usuário pressionou 'q' para sair
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except Exception as e:
            print("Erro:", e)
            break

# Cria a janela principal
root = tk.Tk()
root.title("Cliente de Webcam")

# Cria e posiciona os elementos na janela
ip_label = tk.Label(root, text="Endereço IP:")
ip_label.grid(row=0, column=0, padx=5, pady=5)
ip_entry = tk.Entry(root)
ip_entry.grid(row=0, column=1, padx=5, pady=5)

port_label = tk.Label(root, text="Porta:")
port_label.grid(row=1, column=0, padx=5, pady=5)
port_entry = tk.Entry(root)
port_entry.grid(row=1, column=1, padx=5, pady=5)

start_button = tk.Button(root, text="Iniciar", command=capture_video)
start_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Inicia o loop de eventos da janela
root.mainloop()
