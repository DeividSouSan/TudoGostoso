from abc import ABC, abstractmethod


class IEmailSender(ABC):
    @abstractmethod
    def send_activation_code(self, email_address: str, activation_code: int) -> None: ...