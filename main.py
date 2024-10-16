import imaplib
import email 
from email.header import decode_header

import time

def check_email(username, password, sender_filter):
    imap = imaplib.IMAP4_SSL("imap-mail.outlook.com")  # Porta padrão para IMAP


    try:
        imap.login(username, password)
    except Exception as e:
        print(f"Erro ao logar: {e}")
        return False
    
    imap.select("inbox")

    imap.select("inbox")
    status, messages = imap.search(None, 'Unseen')

    if not messages[0]:
        print("Nenhum e-mail não lido encontrado.")
        return False
    
    email_ids = messages[0].split()

    for email_id in email_ids:

        res, msg = imap.fetch(email_id, "(RFC822)")
        for response in msg:

            if isinstance(response, tuple):

                msg = email.message_from_bytes(response[1])
                subject, encoding = decode_header(msg["Subject"])[0]

                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                
                from_ = msg.get("From")

                if sender_filter.lower() in from_.lower():
                    print(f"Novo e-mail de {sender_filter} encontrado!")
                    print(f"Assunto: {subject}")
                    print(f"De: {from_}")

                    return True

    imap.close()
    imap.logout()
    return False

def email_sniffer(username, password, sender_filter, check_interval=60):
    while True:
        # Verificar novos e-mails do remetente específico
        found = check_email(username, password, sender_filter)
        
        if found:
            print("E-mail processado com sucesso!")
        
        # Esperar pelo intervalo antes de verificar novamente
        time.sleep(check_interval)

# Informações de login 
username = 'henriquefherrmann1@hotmail.com'
password = 'iyqnlqfwaoituzru'

# Remetente que você deseja monitorar
sender_filter = 'todomundo@nubank.com.br'

# Intervalo de checagem (em segundos)
check_interval = 15 # Verifica a cada 15 segundos

# Executar o sniffer
email_sniffer(username, password, sender_filter, check_interval)