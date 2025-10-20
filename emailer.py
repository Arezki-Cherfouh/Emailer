from email.message import EmailMessage
import smtplib
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64,os
from dotenv import load_dotenv
load_dotenv()
def send_email(email: str):
    sender_email = "your_email@gmail.com"
    sender_password = "ilca hxxo sulk vvgl"
    msg = EmailMessage()
    msg["Subject"] = "Qwerify, make your day"
    msg["From"] = sender_email
    msg["To"] = email
    msg.add_alternative(f"""Hi from smtp""", subtype='html')
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        print(f"✅ Sent via Gmail smtp")
    except Exception as e:
        print(f"❌ Gmail smtp Failed: {e}")
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    try:
        service = build('gmail', 'v1', credentials=creds)
        message = MIMEText("hi")
        message['to'] = email
        message['from'] = "your_email@gmail.com"
        message['subject'] = "Gmail API Test"
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        send_result = service.users().messages().send(userId="me", body={'raw': raw}).execute()
        print(f"✅ Sent via Gmail API")
    except Exception as e2:
        print("❌ Gmail API Failed:", e2)
    try:
        br_response = requests.post(
            "https://api.brevo.com/v3/smtp/email",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "api-key": os.getenv("BREVO_API_KEY"),
            },
            json={
                "sender": {"email": sender_email, "name": "Qwerify"},
                "to": [{"email": email}],
                "subject": msg["Subject"],
                "htmlContent": "Hi from brevo",
            }
        )
        if br_response.status_code in (200, 201, 202):
            print("✅ Sent via Brevo")
        else:
            print("❌ Brevo error:", br_response.text)
    except Exception as e3:
        print("❌ Brevo failed:", e3)
    try:
        mj_response = requests.post(
            "https://api.mailjet.com/v3.1/send",
            auth=(os.getenv("MAILJET_API_KEY"),os.getenv("MAILJET_SECRET_KEY")),
            json={
                "Messages": [
                    {
                        "From": {"Email": sender_email, "Name": "Qwerify"},
                        "To": [{"Email": email}],
                        "Subject": msg["Subject"],
                        "HTMLPart": "Hi from mailjet",
                    }
                ]
            }
        )
        if mj_response.status_code == 200:
            print("✅ Sent via Mailjet")
        else:
            print("❌ Mailjet error:", mj_response.text)
    except Exception as e4:
        print("❌ Mailjet failed:", e4)
    sendgrid_api_key=os.getenv("SENDGRID_API_KEY")
    try:
        api_url = "https://api.sendgrid.com/v3/mail/send"
        payload = {
            "personalizations": [{"to": [{"email": email}]}],
            "from": {"email": sender_email},
            "subject": msg["Subject"],
            "content": [{"type": "text/html", "value": f"""Hi from sendgrid"""}]
        }
        headers = {
            "Authorization": f"Bearer {sendgrid_api_key}",
            "Content-Type": "application/json"
        }
        res = requests.post(api_url, json=payload, headers=headers, timeout=10)
        res.raise_for_status()
        if res.status_code == 202:
            print("✅ Sent via Sendgrid")
    except Exception as e5:
        print("❌ Sendgrid failed:", e5)
send_email("target@gmail.com")