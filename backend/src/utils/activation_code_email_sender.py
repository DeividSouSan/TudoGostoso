import email.message
import os
import smtplib

from dotenv import load_dotenv

load_dotenv()


class ActivationCodeEmailSender:
    @staticmethod
    def send_activation_code(email_address: str, activation_code: int):
        body = f"Click the link to activate your account: http://localhost:8000/users/verify/{activation_code}"

        msg = email.message.Message()
        msg.add_header("Content-Type", "text/html")
        msg["Subject"] = "Account activation code"
        msg["From"] = os.getenv("SENDER_EMAIL_ADDRESS")
        msg["To"] = email_address
        msg.set_payload(body)

        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()

        s.login(os.getenv("SENDER_EMAIL_ADDRESS"), os.getenv("SENDER_EMAIL_PASSWORD"))
        s.sendmail(msg["From"], msg["To"], msg.as_string())
        s.quit()
