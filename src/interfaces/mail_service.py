from abc import ABC, abstractmethod
from typing import Self, Optional


class IMailService(ABC):
    """
    Interface for sending emails.

    This abstract base class defines the contract for an email sending service.
    Implementations of this interface must provide the actual mechanism to send
    an email with optional CC, BCC, and file attachments.
    """

    @abstractmethod
    def send_email(self, to: str, subject: str, body: str,
                   cc: Optional[str] = None, bcc: Optional[str] = None,
                   attach: Optional[list[str]] = None) -> bool:
        """
        Sends an email with the specified parameters.

        Args:
            to (str): Recipient email address.
            subject (str): Subject of the email.
            body (str): Body content of the email.
            cc (Optional[str], optional): CC (carbon copy) recipients. Defaults to None.
            bcc (Optional[str], optional): BCC (blind carbon copy) recipients. Defaults to None.
            attach (Optional[list[str]], optional): List of file paths to attach. Defaults to None.

        Returns:
            bool: True if the email was sent successfully, False otherwise.
        """
        pass