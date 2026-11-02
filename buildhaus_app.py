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

    def send_invoice_email(self, to, subject, html):
        try:
            from gmail_client import send_email
            send_email(to, subject, html)
            return {'ok': True}
        except Exception as e:
            return {'ok': False, 'error': str(e)}

    def open_invoice_print(self, html):
        import tempfile, webbrowser
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html)
        webbrowser.open('file:///' + f.name.replace('\\', '/'))
        return {'ok': True}

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
