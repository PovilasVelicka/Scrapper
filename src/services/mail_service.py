import smtplib
import ssl
import time
from typing import Optional
from email.message import EmailMessage
from smtplib import SMTPException, SMTPServerDisconnected, SMTPConnectError
from socket import timeout as SocketTimeout

from src.interfaces.logger import ILogger
from src.interfaces.mail_service import IMailService


class GmailService(IMailService):
    """
    Gmail implementation of the MailService interface.
    Supports App Password authentication, semicolon-separated email addresses,
    retry on failures, and structured logging via ILogger-compatible interface.
    """

    def __init__(self, username: str, app_password: str, logger: ILogger):
        self.__username = username
        self.__password = app_password
        self.__logger = logger
        self.__smtp_server = "smtp.gmail.com"
        self.__smtp_port = 465  # SSL


    def _split_addresses(self, addresses: Optional[str]) -> list[str]:
        if not addresses:
            return []
        return [addr.strip() for addr in addresses.replace(';', ',').split(',') if addr.strip()]


    def send_email(self, to: str, subject: str, body: str,
                   cc: Optional[str] = None, bcc: Optional[str] = None,
                   attach: Optional[list[str]] = None) -> bool:

        to_list = self._split_addresses(to)
        cc_list = self._split_addresses(cc)
        bcc_list = self._split_addresses(bcc)

        all_recipients = to_list + cc_list + bcc_list

        msg = EmailMessage()
        msg["From"] = self.__username
        msg["To"] = ', '.join(to_list)
        if cc_list:
            msg["Cc"] = ', '.join(cc_list)
        msg["Subject"] = subject
        msg.set_content(body)

        # Add attachments
        if attach:
            for file_path in attach:
                try:
                    with open(file_path, "rb") as f:
                        file_data = f.read()
                        file_name = file_path.split("/")[-1]
                        msg.add_attachment(file_data, maintype="application",
                                           subtype="octet-stream", filename=file_name)
                except Exception as e:
                    self.__logger.log_error(f"Failed to attach file {file_path}: {e}")
                    return False

        # Retry logic
        for attempt in range(1, 4):
            try:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(self.__smtp_server, self.__smtp_port, context=context, timeout=10) as server:
                    server.login(self.__username, self.__password)
                    server.send_message(msg, from_addr=self.__username, to_addrs=all_recipients)
                self.__logger.log_info(f"Email sent To {to_list}, CC: {cc_list}, BCC: {len(bcc_list)} recipients.")
                return True
            except (SMTPServerDisconnected, SMTPConnectError, SMTPException, SocketTimeout) as e:
                self.__logger.log_warning(f"Send email to {to} attempt {attempt} failed: {e}")
                if attempt < 3:
                    time.sleep(2)
                else:
                    self.__logger.log_error("All attempts to send email failed.")
                    return False
        return False