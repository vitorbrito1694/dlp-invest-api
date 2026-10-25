# DLP Invest – consulta de carteira e operações

Script somente leitura (GET) para `/carteira` e `/operacoes`.

## Configurar o token (uma vez)

No PowerShell:

```powershell
setx DLP_TOKEN "DLP-seu-token-aqui"
```

Feche e reabra o terminal depois. O token não fica no código nem nesta pasta.

## Executar

```powershell
cd "C:\Users\vitor\OneDrive\Documents\ProjetosJS\dlp-invest"
pip install requests
python consulta_dlp.py
```

As respostas são salvas em `saida\` como JSON com data e hora no nome.

## Observações

- A pasta `saida\` contém dados da sua carteira. Não compartilhe nem envie para repositórios públicos.
- Para um repositório Git, adicione `saida/` e `.env` ao `.gitignore`.
