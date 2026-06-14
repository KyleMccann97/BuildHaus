import webview
import os
import json

BASE = os.path.dirname(os.path.abspath(__file__))

class Api:
    def get_inbox(self):
        try:
            from gmail_client import fetch_emails
            from email_scanner import scan_email
            emails = fetch_emails(max_results=30)
            inbox = []
            quarantine = []
            for email in emails:
                flags = scan_email(email['subject'], email['from'], email['body'])
                if flags:
                    email['flags'] = flags
                    quarantine.append(email)
                else:
                    inbox.append(email)
            return {'ok': True, 'inbox': inbox, 'quarantine': quarantine}
        except Exception as e:
            return {'ok': False, 'error': str(e)}

    def generate_draft(self, email_json):
        try:
            from jarvis_email import generate_reply_draft
            email = json.loads(email_json) if isinstance(email_json, str) else email_json
            draft = generate_reply_draft(email)
            return {'ok': True, 'draft': draft}
        except Exception as e:
            return {'ok': False, 'error': str(e)}

    def send_reply(self, to, subject, body, thread_id, in_reply_to=''):
        try:
            from gmail_client import send_reply
            result = send_reply(to, subject, body, thread_id, in_reply_to or None)
            return {'ok': True, 'id': result.get('id')}
        except Exception as e:
            return {'ok': False, 'error': str(e)}

    def mark_read(self, message_id):
        try:
            from gmail_client import mark_as_read
            mark_as_read(message_id)
            return {'ok': True}
        except Exception as e:
            return {'ok': False, 'error': str(e)}

html_path = os.path.join(BASE, 'dashboard.html')
api = Api()

window = webview.create_window(
    'Buildhaus Dashboard',
    url=f'file:///{html_path.replace(os.sep, "/")}',
    width=1200,
    height=800,
    min_size=(900, 600),
    background_color='#0d0d0d',
    js_api=api
)

webview.start()
