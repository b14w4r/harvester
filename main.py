import imaplib
import email
from email.policy import default
import os
from glob import glob

import sqlalchemy as db
from dotenv import load_dotenv
from file_fixer import process_file
from injector import injection
from weather_requester import weather_table_inject

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

def cleanup(extensions: tuple = (".xlsx", ".csv")):
    directory = os.path.dirname(os.path.abspath(__file__))
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename.endswith(extensions):
            try:
                os.remove(file_path)
                print(f"Удалён: {file_path}")
            except Exception as e:
                print(f"Ошибка удаления {file_path}: {e}")

    print("Лишние файлы удалены")


def find_missing_dates():
    engine = db.create_engine(
        "postgresql://neondb_owner:npg_FBvTi18ySpoY@ep-yellow-salad-a9lbdmij-pooler.gwc.azure.neon.tech/neondb?sslmode=require")

    with engine.connect() as connection:
        query = db.text("""
            SELECT DISTINCT p.date 
            FROM prices p
            LEFT JOIN weather w ON p.date = w.date
            WHERE w.date IS NULL;
        """)
        result = connection.execute(query)

        for row in result:
            weather_table_inject(row[0])


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
    cleanup()
    find_missing_dates()

    mail.logout()
