import os
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

BASE = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(BASE, 'gmail_token.json')
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
]

def get_service():
    if not os.path.exists(TOKEN_FILE):
        raise RuntimeError('gmail_token.json not found — run gmail_auth.py first.')
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def fetch_emails(max_results=20):
    service = get_service()
    result = service.users().messages().list(
        userId='me', labelIds=['INBOX'], maxResults=max_results
    ).execute()

    emails = []
    for msg in result.get('messages', []):
        full = service.users().messages().get(
            userId='me', id=msg['id'], format='full'
        ).execute()
        headers = {h['name']: h['value'] for h in full['payload'].get('headers', [])}
        body = _extract_body(full['payload'])
        emails.append({
            'id': full['id'],
            'thread_id': full['threadId'],
            'from': headers.get('From', ''),
            'to': headers.get('To', ''),
            'subject': headers.get('Subject', '(No Subject)'),
            'date': headers.get('Date', ''),
            'message_id': headers.get('Message-ID', ''),
            'snippet': full.get('snippet', ''),
            'body': body,
            'unread': 'UNREAD' in full.get('labelIds', []),
        })
    return emails

def _extract_body(payload):
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data', '')
                if data:
                    return base64.urlsafe_b64decode(data).decode('utf-8', errors='replace')
        for part in payload['parts']:
            result = _extract_body(part)
            if result:
                return result
    else:
        data = payload.get('body', {}).get('data', '')
        if data:
            return base64.urlsafe_b64decode(data).decode('utf-8', errors='replace')
    return ''

def send_reply(to: str, subject: str, body: str, thread_id: str, in_reply_to: str = None):
    service = get_service()
    msg = MIMEText(body)
    msg['To'] = to
    msg['From'] = 'me'
    msg['Subject'] = subject if subject.lower().startswith('re:') else f'Re: {subject}'
    if in_reply_to:
        msg['In-Reply-To'] = in_reply_to
        msg['References'] = in_reply_to
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    return service.users().messages().send(
        userId='me',
        body={'raw': raw, 'threadId': thread_id}
    ).execute()

def mark_as_read(message_id: str):
    service = get_service()
    service.users().messages().modify(
        userId='me', id=message_id,
        body={'removeLabelIds': ['UNREAD']}
    ).execute()
