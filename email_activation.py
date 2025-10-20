from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64, pickle, pyperclip
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)
token_bytes = pickle.dumps(creds)
b64_token = base64.b64encode(token_bytes).decode()
pyperclip.copy(b64_token)
print("✅ Token copied to clipboard as base64 (ready for Render env variable).")
try:
    service = build('gmail', 'v1', credentials=creds)
    message = MIMEText("hi")
    message['to'] = "target@gmail.com"
    message['from'] = "your_email@gmail.com"
    message['subject'] = "Gmail API Test"
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    send_result = service.users().messages().send(userId="me", body={'raw': raw}).execute()
    print(f"✅ Test email sent successfully! Message ID: {send_result['id']}")
except Exception as e:
    print("❌ Failed to send test email:", e)
