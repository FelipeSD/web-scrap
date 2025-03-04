import os
import hashlib
import requests
from bs4 import BeautifulSoup
from email_service import EmailService

class WebScraper:
    def __init__(self, url, recipients):
        self.url = url
        self.recipients = recipients
        self.state_file = 'last_site_state.txt'
    
    def get_site_content(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            return soup.get_text()
        
        except requests.RequestException as e:
            print(f"Erro ao acessar o site: {e}")
            return None
    
    def calculate_content_hash(self, content):
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def send_email_notification(self, message):
        try:
            email_service = EmailService()
            subject = 'Relatório do monitoramento do site'
            
            body = f"""
            {message}
            
            Link do site: {self.url}
            """
            success = email_service.send_notification(subject, body, self.recipients)
            
            if success:
                print("Email enviado com sucesso!")
            else:
                print("Falha no envio do email")

        except Exception as e:
            print(f"Erro ao enviar email: {e}")
    
    def check_for_updates(self):
        current_content = self.get_site_content()
        
        if not current_content:
            print("Não foi possível obter o conteúdo do site.")
            return
        
        current_hash = self.calculate_content_hash(current_content)
        
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                last_hash = f.read().strip()
            
            if current_hash != last_hash:
                self.send_email_notification(
                    "Conteúdo do site foi atualizado!"
                )
            else:
                self.send_email_notification(
                    """
                    Conteúdo foi verificado, mas não houve mudanças!

                    Continuaremos monitorando.
                    """
                )

        with open(self.state_file, 'w') as f:
            f.write(current_hash)

def main():
    recipients = os.getenv('EMAIL_RECIPIENTS', '').split(',')
    scraper = WebScraper(os.getenv('SCRAPE_URL'), recipients)
    scraper.check_for_updates()

if __name__ == "__main__":
    main()