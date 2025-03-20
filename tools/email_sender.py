import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

def send_email(to: str, subject: str, body: str):
    # メールサーバーの設定
    smtp_server = "smtp.gmail.com"  # Gmailの場合
    port = 587
    sender_email = os.getenv('EMAIL_USER')
    password = os.getenv('EMAIL_PASSWORD')

    if not sender_email or not password:
        raise ValueError("環境変数 EMAIL_USER と EMAIL_PASSWORD が設定されていません。")

    # メールメッセージの作成
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # メールの送信
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
        print("メールが正常に送信されました。")
    except Exception as e:
        print(f"メール送信中にエラーが発生しました: {e}")
        raise 