import imaplib
import email
from email.policy import default
import os
from glob import glob

import openpyxl
from dotenv import load_dotenv
from file_fixer import process_file
from injector import injection

load_dotenv()

# Данные для подключения
IMAP_SERVER = os.environ['IMAP_SERVER']
EMAIL_ACCOUNT = os.environ['EMAIL_ACCOUNT']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']

def connect_mail():
    """Подключение к почтовому ящику."""
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    print(f"Подключение к {IMAP_SERVER} как {EMAIL_ACCOUNT}")
    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    mail.select("inbox")
    return mail


def fetch_unread_emails(mail):
    """Получение непрочитанных писем."""
    status, messages = mail.search(None, 'UNSEEN')
    if status != "OK":
        return []
    return messages[0].split()


def download_attachments(msg):
    """Скачивание вложений из письма и проверка на Excel."""
    for part in msg.iter_attachments():
        filename = part.get_filename()
        if filename and filename.endswith((".xls", ".xlsx", ".csv")):
            filepath = os.path.join(filename)
            with open(filepath, "wb") as f:
                f.write(part.get_payload(decode=True))
            print(f"Сохранен файл: {filename}")

def filing():
    data_files = glob("*.csv") + glob("*.xlsx")
    if not data_files:
        print("❌ В текущей папке нет CSV или XLSEADDMEов.")
    else:
        for file in data_files:
            injection(process_file(file))

if __name__ == "__main__":
    mail = connect_mail()
    email_ids = fetch_unread_emails(mail)

    for e_id in email_ids:
        status, msg_data = mail.fetch(e_id, "(RFC822)")
        if status != "OK":
            continue

        msg = email.message_from_bytes(msg_data[0][1], policy=default)
        print("here works")
        download_attachments(msg)
        filing()


    mail.logout()