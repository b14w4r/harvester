import imaplib
import email
from email.policy import default
import os
import openpyxl

# Данные для подключения
IMAP_SERVER = "imap.gmail.com"  # для Gmail, для других сервисов будет свой
EMAIL_ACCOUNT = "zepovj@gmail.com"
EMAIL_PASSWORD = "edwp wkpt slsx tjub"

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
        if filename and filename.endswith((".xls", ".xlsx")):
            filepath = os.path.join(filename)
            with open(filepath, "wb") as f:
                f.write(part.get_payload(decode=True))
            print(f"Сохранен файл: {filename}")
            process_excel(filepath)


def process_excel(filepath):
    """Обработка Excel файла."""
    wb = openpyxl.load_workbook(filepath)
    sheet = wb.active
    for row in sheet.iter_rows(values_only=True):
        print(row)  # Здесь можно делать что-то с данными


if __name__ == "__main__":
    mail = connect_mail()
    email_ids = fetch_unread_emails(mail)

    for e_id in email_ids:
        status, msg_data = mail.fetch(e_id, "(RFC822)")
        if status != "OK":
            continue

        msg = email.message_from_bytes(msg_data[0][1], policy=default)
        download_attachments(msg)

    mail.logout()