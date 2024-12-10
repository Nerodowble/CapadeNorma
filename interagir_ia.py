import imaplib
import email
from email.header import decode_header
import pandas as pd

# Configurações do email
EMAIL = "willian.lima@legalbot.com.br"
PASSWORD = "jjuo udms btbl vozp"
IMAP_SERVER = "imap.gmail.com"

# Conectar ao servidor IMAP
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL, PASSWORD)

# Selecionar a pasta "[Gmail]/Todos os e-mails"
mail.select('"[Gmail]/Todos os e-mails"')

# Critério de busca: Emails enviados pelo remetente com "Bradesco"
search_criteria = '(FROM "bradesco" SINCE "01-Jan-2024" BEFORE "09-Dec-2024")'

# Buscar emails que atendem ao critério
status, messages = mail.search(None, search_criteria)
if status != "OK":
    print("Nenhum email encontrado com os critérios fornecidos.")
    mail.logout()
    exit()

email_ids = messages[0].split()
print(f"Encontrados {len(email_ids)} emails do remetente 'Bradesco' no intervalo de datas.")

# Listas para armazenar os dados
email_titles = []
email_texts = []
email_senders = []
email_recipients = []

for idx, email_id in enumerate(email_ids):
    # Mostrar progresso
    print(f"Processando email {idx + 1} de {len(email_ids)}")

    # Buscar o email pelo ID
    status, msg_data = mail.fetch(email_id, "(RFC822)")
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            
            # Decodificar o título
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8", errors="ignore")
            else:
                subject = subject or "(Sem título)"
            email_titles.append(subject)
            
            # Obter o corpo
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        try:
                            body = part.get_payload(decode=True).decode("utf-8")
                        except UnicodeDecodeError:
                            body = part.get_payload(decode=True).decode("latin1", errors="ignore")
                        break
            else:
                try:
                    body = msg.get_payload(decode=True).decode("utf-8")
                except UnicodeDecodeError:
                    body = msg.get_payload(decode=True).decode("latin1", errors="ignore")
            email_texts.append(body)

            # Obter o remetente (quem enviou)
            sender = msg["From"]
            email_senders.append(sender if sender else "Desconhecido")

            # Obter os destinatários (quem recebeu)
            recipients = msg["To"]
            if recipients:
                recipients = recipients.replace("\r", "").replace("\n", "").replace(", ", ";")
            email_recipients.append(recipients if recipients else "Desconhecido")

# Fechar conexão
mail.logout()

# Criar DataFrame com os dados
df = pd.DataFrame({
    "Título": email_titles,
    "Texto": email_texts,
    "Remetente": email_senders,
    "Destinatários": email_recipients
})

# Salvar em Excel
df.to_excel("emails_bradesco_2024.xlsx", index=False)

print(f"{len(email_titles)} emails encontrados e salvos no arquivo 'emails_bradesco_2024.xlsx'.")
