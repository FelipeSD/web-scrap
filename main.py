import os
import hashlib
import requests
from bs4 import BeautifulSoup
from email_service import EmailService

class WebScraper:
    def __init__(self, url, recipients):
        self.url = url
        self.recipients = recipients
        self.cache_file = 'last_site_state.txt'
    
    def get_site_content(self, selector: str) -> str:
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            element = soup.select_one(selector)
            return element.get_text() if element else ''
        
        except requests.RequestException as e:
            print(f"Erro ao acessar o site: {e}")
            return ''
    
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
    
    def load_last_hash(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                return f.read().strip()
        return None
    
    def save_current_hash(self, current_hash):
        with open(self.cache_file, 'w') as f:
            f.write(current_hash)
    
    def check_for_updates(self):
        selector = os.getenv('SCRAPE_SELECTOR', '')
        current_content = self.get_site_content(selector)
        if not current_content:
            print("Não foi possível obter o conteúdo do site.")
            return
        
        current_hash = self.calculate_content_hash(current_content)
        last_hash = self.load_last_hash()
        
        if last_hash:
            if current_hash != last_hash:
                self.send_email_notification(
                    f"""Conteúdo do site foi atualizado!

                    {current_content}
                    """
                )
            else:
                self.send_email_notification(
                    f"""
                    Conteúdo foi verificado, mas não houve mudanças!

                    {current_content}
                    
                    Continuaremos monitorando.
                    """
                )
        else:
            print("Primeira execução. Nenhuma hash anterior encontrada.")
        
        self.save_current_hash(current_hash)

def main():
    recipients = os.getenv('EMAIL_RECIPIENTS', '').split(',')
    scraper = WebScraper(os.getenv('SCRAPE_URL'), recipients)
    scraper.check_for_updates()

if __name__ == "__main__":
    main()