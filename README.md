# Web Scraper - Monitoramento de Alterações em Sites

Este projeto é um **Web Scraper** desenvolvido para monitorar alterações em sites específicos. Ele verifica diariamente o conteúdo de uma página web e, caso detecte mudanças, envia um e-mail de notificação para os destinatários configurados. O objetivo é automatizar o acompanhamento de atualizações em sites, eliminando a necessidade de verificações manuais.


## Funcionalidades Principais

- **Monitoramento Diário**: O script é executado diariamente para verificar se houve alterações no conteúdo do site.
- **Notificação por E-mail**: Caso seja detectada uma mudança, um e-mail é enviado para os destinatários configurados.
- **Persistência de Estado**: O script armazena o estado anterior do site (usando hash MD5) para comparar com a versão atual.
- **Configuração Dinâmica**: URLs, seletores de conteúdo e destinatários de e-mail são configuráveis via variáveis de ambiente.


## Como Funciona

1. **Acesso ao Site**: O script acessa a URL configurada e extrai o conteúdo da página.
2. **Interação com a Página (Opcional)**: Caso necessário, o script clica em abas ou botões para revelar conteúdo escondido.
3. **Comparação de Conteúdo**: O conteúdo atual é comparado com a versão anterior (armazenada em um arquivo de estado).
4. **Notificação por E-mail**:
   - Se houver alterações, um e-mail é enviado informando que o conteúdo foi atualizado.
   - Se não houver alterações, um e-mail de confirmação é enviado para garantir que o monitoramento está ativo.
5. **Atualização do Estado**: O estado atual do site é salvo para futuras comparações.


## Configuração

### Variáveis de Ambiente

Para configurar o script, defina as seguintes variáveis de ambiente seguindo o modelo exemplo .env.example:

- `SCRAPE_URL`: URL do site a ser monitorado.
- `SCRAPE_SELECTOR`: Seletor CSS do elemento a ser extraído (ex: `div#content`).
- `EMAIL_RECIPIENTS`: Lista de e-mails dos destinatários, separados por vírgula (ex: `email1@exemplo.com,email2@exemplo.com`).

## Tecnologias Utilizadas
- Python: Linguagem principal do projeto.
- BeautifulSoup: Biblioteca para extrair dados de páginas HTML.
- SMTP: Protocolo para envio de e-mails.
- GitHub Actions: Automação de execução do script em ambiente cloud.