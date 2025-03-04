# WEB SCRAPER
Extrai as informações do site para rastreamento de alterações.

O arquivo script.py foi criado para ser executado por agendamento diário.

Para ser rodado a cada reinicialização do windows, um arquivo bat foi criado, para acessar:

```
Pressione Win + R
Digite shell:startup
```
Crie um arquivo .bat na pasta de inicialização com o conteúdo:
```bat
@echo off
start pythonw C:\caminho\completo\para\seu\script.py
```