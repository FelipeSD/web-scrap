import schedule
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from main import main as run_web_scraper

def job():
    """
    Função para executar o script diariamente
    """
    try:
        run_web_scraper()
        print(f"Tarefa executada com sucesso em {time.strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print(f"Erro na execução: {e}")

def main():
    schedule.every().day.at("12:30").do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()