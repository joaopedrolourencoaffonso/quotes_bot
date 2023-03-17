# Estatísticas do Canal

## Propósito
Este repositório é parte do projeto [quotes_bot](https://github.com/joaopedrolourencoaffonso/quotes_bot) e tem como objetivo armazenar scripts voltados para análise estatística do canal, isto é, monitorar engajamento dos usuários, visualizações, mensagens mais populares, etc...

## Objetivos

- [x] Visualizações por mensagem _do meu canal_
- [x] Reações por mensagem _do meu canal_
- [x] Extrair estatísticas acima de um canal arbitrário fornecido pelo usuário
- [x] Extrair estatísticas acima e armazenar em um arquivo csv especificado pelo usuário
- [x] Pegar mensagens a partir de id especificado
- [ ] Pegar mensagens até id especificado
- [ ] Relacionar id de mensagem enviada com frase na base de dados (analisar logs)
- [ ] Aplicar ciência de dados para identificar palavras/temas mais populares

## Atualizações
Após avaliar as necessidades do meu projeto, percebir que abrir o arquivo diretamente pelo script era desnecessário e pouco flexível.
A nova versão do script "printa" os resultados diretamente na linha de comando, para dar liberdade ao usuário de escolher como armazenar a saída (por padrão, csv).
