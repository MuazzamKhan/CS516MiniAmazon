from flask_mail import Mail, Message
from flask import current_app as app

def send_email(to, subject, template):
    
    mail = Mail()
    mail.init_app(app)

    msg = Message(
            subject,
            recipients=[to],
            html=template,
            sender=app.config.get("MAIL_USERNAME")
        )
    
    mail.send(msg)

