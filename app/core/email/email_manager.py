from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

from configuration.configs import settings

conf: ConnectionConfig = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    SUPPRESS_SEND=settings.MAIL_SUPPRESS_SEND,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)


async def send_email_async(
        subject: str,
        email_to: list,
        body: str = None,
        html: str = None
):
    message: MessageSchema = MessageSchema(
        subject=subject,
        recipients=email_to,
        subtype=MessageType.html
    )

    if body:
        message.body = body

    if html:
        message.html = html

    fm = FastMail(conf)

    await fm.send_message(
        message
    )
