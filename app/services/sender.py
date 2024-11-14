from abc import ABC, abstractmethod


class MessageSender(ABC):
    # TODO: Could add broadcast function here which takes list of reciepients.
    
    @abstractmethod
    def send() -> str:
        """
        Send a message to the recipient with the provided content.
        Returns:
            str: Status of the message delivery ("Success" or "Failed").
        """
        pass
    
    
class EmailSender(MessageSender):
    def send(self, source: str, recipient: str, content: str) -> str:
        """
        Dummy method to send an email to the recipient.
        """   
        
        print(f"Sending email to {recipient}: {content}")

        # TODO: Define specific exceptions to based on behaviours
        return "Success"


class SmsSender(MessageSender):
    def send(self, source: str, recipient: str, content: str) -> str:
        """
        Dummy method to send an email to the recipient.
        """   
        
        print(f"Sending SMS to {recipient}: {content}")
        # TODO: Define specific exceptions to based on behaviours
        return "Success"
