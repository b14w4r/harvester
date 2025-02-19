import imaplib

IMAP_SERVER = "imap.gmail.com"
EMAIL_ACCOUNT = "zepovj@gmail.com"
EMAIL_PASSWORD = "Gojda2025"

mail = imaplib.IMAP4_SSL(IMAP_SERVER)
try:
    status, response = mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    print(f"Login status: {status}, response: {response}")
except imaplib.IMAP4.error as e:
    print(f"Ошибка IMAP: {e}")
