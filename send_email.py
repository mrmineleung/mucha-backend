import ssl

from config import settings
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

from enumerations import EmailType

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    # MAIL_TLS=True,
    # MAIL_SSL=False,
    USE_CREDENTIALS=True,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    VALIDATE_CERTS=False,
    TEMPLATE_FOLDER='./templates/email'
)

ssl._create_default_https_context = ssl._create_unverified_context

async def send_email_async(email_type: EmailType, subject: str, email_to: str, body: dict):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=body,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name=email_type.value)

#
# def send_email_background(background_tasks: BackgroundTasks, subject: str, email_to: str, body: dict):
#     message = MessageSchema(
#         subject=subject,
#         recipients=[email_to],
#         template_body=body,
#         subtype=MessageType.html,
#     )
#     fm = FastMail(conf)
#     background_tasks.add_task(
#         fm.send_message, message, template_name='email-verification.html')