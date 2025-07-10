import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client
from datetime import datetime

class AlertsManager:
    """
    Handles sending alerts via email and SMS (Twilio).
    Manages alert history and notification settings.
    """
    def __init__(self, email_config=None, sms_config=None):
        self.email_config = email_config or {}
        self.sms_config = sms_config or {}
        self.history = []

    def send_email_alert(self, subject, message, recipient):
        """Send an email alert to the recipient."""
        try:
            smtp_server = self.email_config.get('smtp_server', 'smtp.gmail.com')
            smtp_port = self.email_config.get('smtp_port', 587)
            username = self.email_config.get('username') or ""
            password = self.email_config.get('password') or ""
            sender = self.email_config.get('sender', username) or ""
            recipient = recipient or ""
            msg = MIMEText(message)
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = recipient
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(username, password)
                server.sendmail(sender, [recipient], msg.as_string())
            self.history.append({'type': 'email', 'to': recipient, 'subject': subject, 'message': message, 'timestamp': datetime.now().isoformat(sep=' ', timespec='seconds')})
            return True
        except Exception as e:
            self.history.append({'type': 'email', 'to': recipient, 'subject': subject, 'message': message, 'error': str(e), 'timestamp': datetime.now().isoformat(sep=' ', timespec='seconds')})
            return False

    def send_sms_alert(self, message, phone_number):
        """Send an SMS alert to the phone number."""
        try:
            account_sid = self.sms_config.get('account_sid')
            auth_token = self.sms_config.get('auth_token')
            from_number = self.sms_config.get('from_number')
            client = Client(account_sid, auth_token)
            client.messages.create(body=message, from_=from_number, to=phone_number)
            self.history.append({'type': 'sms', 'to': phone_number, 'message': message, 'timestamp': datetime.now().isoformat(sep=' ', timespec='seconds')})
            return True
        except Exception as e:
            self.history.append({'type': 'sms', 'to': phone_number, 'message': message, 'error': str(e), 'timestamp': datetime.now().isoformat(sep=' ', timespec='seconds')})
            return False

    def get_history(self):
        return self.history
