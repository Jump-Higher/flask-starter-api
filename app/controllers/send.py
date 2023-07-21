from flask_mail import Message
from app import mail

def send_email():
    msg = Message('Hello', recipients=['moch.sandhyka@gmail.com'],sender='fearlessteams27@gmail.com')
    msg.body = 'This is a test email sent from Flask-Mail'
    mail.send(msg)
    return 'Email sent!'