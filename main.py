import imaplib
import email
from email.policy import default
import os
from glob import glob

import openpyxl
from dotenv import load_dotenv
from file_fixer import process_file

load_dotenv()  # take environment variables from .env.

# Code of your application, which uses environment variables (e.g. from `os.environ` or
# `os.getenv`) as if they came from the actual environment.

# Данные для подключения
IMAP_SERVER = os.environ['IMAP_SERVER']
EMAIL_ACCOUNT = os.environ['EMAIL_ACCOUNT']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']

def connect_mail():
    """Подключение к почтовому ящику."""
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    print(f"Подключение к {IMAP_SERVER} как {EMAIL_ACCOUNT}")
    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)  # Тут может быть ошибка
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
            # process_excel(filepath)

'''
def process_excel(filepath):
    """Обработка Excel файла."""
    wb = openpyxl.load_workbook(filepath)
    sheet = wb.active
    for row in sheet.iter_rows(values_only=True):
        print(row)  # Здесь можно делать что-то с данными
'''

if __name__ == "__main__":
    mail = connect_mail()
    email_ids = fetch_unread_emails(mail)

    for e_id in email_ids:
        status, msg_data = mail.fetch(e_id, "(RFC822)")
        if status != "OK":
            continue

        msg = email.message_from_bytes(msg_data[0][1], policy=default)
        download_attachments(msg)

        csv_files = glob("*.csv")

        if not csv_files:
            print("❌ В текущей папке нет CSV-файлов.")
        else:
            for file in csv_files:
                process_file(file)

    mail.logout()