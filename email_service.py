import os
import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from abc import ABC, abstractmethod
from dotenv import load_dotenv
import logging
from typing import List, Optional

# Carregar variáveis de ambiente
load_dotenv()

# Configuração de Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='email_service.log'
)
logger = logging.getLogger(__name__)

class EmailSenderInterface(ABC):
    """
    Interface para definir o contrato de envio de emails
    Princípio da Segregação de Interface (ISP)
    """
    @abstractmethod
    def send_email(
        self, 
        subject: str, 
        body: str, 
        to_emails: List[str]
    ) -> bool:
        """
        Método abstrato para envio de emails
        """
        pass

class EmailConfiguration:
    """
    Classe para gerenciar configurações de email
    Princípio da Responsabilidade Única (SRP)
    """
    def __init__(self):
        """
        Carrega configurações seguras de variáveis de ambiente
        """
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        
        # Validação de configurações
        self._validate_config()
    
    def _validate_config(self):
        """
        Valida as configurações de email
        """
        required_configs = [
            self.smtp_server, 
            self.sender_email, 
            self.sender_password
        ]
        
        if not all(required_configs):
            raise ValueError("Configurações de email incompletas")

class SMTPEmailSender(EmailSenderInterface):
    """
    Implementação concreta de envio de emails via SMTP
    Princípio Aberto/Fechado (OCP)
    """
    def __init__(self, config: EmailConfiguration):
        """
        Inicializa o sender com configurações
        
        :param config: Configurações de email
        """
        self._config = config
    
    def send_email(
        self, 
        subject: str, 
        body: str, 
        to_emails: List[str],
        cc_emails: Optional[List[str]] = None,
        bcc_emails: Optional[List[str]] = None
    ) -> bool:
        """
        Envia email com tratamento de erros e logging
        
        :param subject: Assunto do email
        :param body: Corpo do email
        :param to_emails: Lista de destinatários
        :param cc_emails: Lista de destinatários em cópia
        :param bcc_emails: Lista de destinatários em cópia oculta
        :return: Booleano indicando sucesso do envio
        """
        try:
            # Criar mensagem
            msg = MIMEMultipart()
            msg['From'] = self._config.sender_email
            msg['To'] = ', '.join(to_emails)
            
            # Adicionar CC e BCC se existirem
            if cc_emails:
                msg['Cc'] = ', '.join(cc_emails)
                to_emails.extend(cc_emails)
            
            if bcc_emails:
                to_emails.extend(bcc_emails)
            
            msg['Subject'] = subject
            
            # Adicionar corpo do email
            msg.attach(MIMEText(body, 'plain'))
            context = ssl.create_default_context()

            with smtplib.SMTP(
                self._config.smtp_server, 
                self._config.smtp_port
            ) as server:
                server.starttls(context=context)
                server.login(
                    self._config.sender_email, 
                    self._config.sender_password
                )
                
                # Enviar email
                server.send_message(msg)
            
            # Logging de sucesso
            logger.info(f"Email enviado para {to_emails}")
            return True
        
        except smtplib.SMTPException as smtp_error:
            # Logging de erro de SMTP
            logger.error(f"Erro SMTP: {smtp_error}")
            return False
        
        except Exception as error:
            # Logging de erros gerais
            logger.error(f"Erro inesperado no envio de email: {error}")
            return False

class EmailService:
    """
    Fachada para simplificar o uso do serviço de email
    Princípio da Inversão de Dependência (DIP)
    """
    def __init__(self):
        """
        Inicializa o serviço de email
        """
        config = EmailConfiguration()
        self._sender = SMTPEmailSender(config)
    
    def send_notification(
        self, 
        subject: str, 
        body: str, 
        recipients: List[str]
    ) -> bool:
        """
        Método de alto nível para envio de notificações
        
        :param subject: Assunto do email
        :param body: Corpo do email
        :param recipients: Lista de destinatários
        :return: Booleano indicando sucesso do envio
        """
        return self._sender.send_email(subject, body, recipients)

# Exemplo de uso
def main():
    # Exemplo de como usar o serviço de email
    email_service = EmailService()
    
    subject = "Notificação de Atualização"
    body = "Conteúdo do site foi atualizado!"
    recipients = ["destinatario@exemplo.com"]
    
    success = email_service.send_notification(subject, body, recipients)
    
    if success:
        print("Email enviado com sucesso!")
    else:
        print("Falha no envio do email")

if __name__ == "__main__":
    main()