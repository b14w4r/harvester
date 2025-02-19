import imaplib
import os
from dotenv import load_dotenv
load_dotenv()

IMAP_SERVER = os.environ['IMAP_SERVER']
EMAIL_ACCOUNT = os.environ['EMAIL_ACCOUNT']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']

mail = imaplib.IMAP4_SSL(IMAP_SERVER)
try:
    status, response = mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    print(f"Login status: {status}, response: {response}")
except imaplib.IMAP4.error as e:
    print(f"Ошибка IMAP: {e}")
