# quotes_bot

<p align="center"><a href="https://t.me/dosesdesabedoria"><img src="https://github.com/joaopedrolourencoaffonso/quotes_bot/blob/main/watermark.jpg" width="250" height="250"></a></p>

Um bot do telegram para dividir sabedoria com o mundo! Para ver os resultados, basta acessa [meu canal do Telegram](https://t.me/dosesdesabedoria).

## Novidades

- Nossa base de dados chegou em 852 frases! 🎉🎉🎉
- Nova opção "watermark" permite adicionar watermarks à imagens por meio da linha de comando.
- Novas opções de fontes

## Planos Futuros

- [x] Gerar captions com base em imagem e frases escolhidas aleatoriamente a partir de base de dados.
- [x] Mecanismo para adicionar frases na base de dados a partir da linha de comando.
- [x] Opção para pesquisar na base de dados a partir da linha de comando por frases de um autor
- [x] Opção para pesquisar na base de dados a partir da linha de comando por frases com determinada string.
- [x] Opção para pesquisar na base de dados a partir da linha de comando por frases de um autor com determinada string.
- [x] Gerar caption a partir de imagem, frase e autor especificados na linha de comando
- [x] Opção para verificar estatísticas básicas sobre a base de dados.
- [x] Watermark.
- [x] Novas fontes de letra.
- [x] [Extrair estatísticas de visualização diretamente do Telegram](https://github.com/joaopedrolourencoaffonso/quotes_bot/tree/main/channel)
- [X] Agendar envio de mensagens automaticamente.
- [ ] Opção "install" para criar base de dados sqlite a partir de um único comando.
- [ ] Automatizar upload das novas frases no Github (feito por git push manual atualmente) 
- [ ] Translate code and README to english.
- [ ] Gerar imagens com base em inteligência artificial
- [ ] Inserir todas as frases sábias escritas pela raça humana.
- [x] Inserir todas as frases sábias escritas pelos golfinhos.

## O código

## SQLite

O script utiliza uma base de dados chamada ```citacoes.db```, a qual pode ser criada conforme abaixo:

```python
import sqlite3

con = sqlite3.connect('citacoes.db');
cur = con.cursor();

cur.execute("CREATE TABLE images (ultima int, image text, red integer, green integer, blue integer, link text)");
cur.execute("CREATE TABLE "citacoes" (autor text, frase text, enviar int)");
con.commit()
```
As citações que eu utilizei estão  disponíves [aqui](https://github.com/joaopedrolourencoaffonso/quotes_bot/blob/main/citacoes.json). Uma lista das imagens está disponível [aqui](https://github.com/joaopedrolourencoaffonso/quotes_bot/blob/main/images.json), destaco, porém, que eu não sou proprietário dessas imagens, sendo todas disponibilizadas a partir do [unsplash](https://unsplash.com/).

## Python

O código é bem simples, temos três funções: ```main, quebra_lista_alt, fazedor_de_imagem```.

### main

É a responsável por selecionar a frase, a imagem e enviar para o Telegram.<br>
O código abaixo é usado para selecionar a frase, perceba que o campo "_enviar_" é utilizado como um marcador, para evitar que uma frase já enviada seja enviada novamente. "_Mas por que não excluir da BD?_", eu preetendo reutilizar algumas frases à medida que eu for adicionando novas imagens.

```python
# Selecionando a frase
rowid, autor, frase = cur.execute(f"select rowid, autor, frase from citacoes where enviar = 0 ORDER BY RANDOM() LIMIT 1;").fetchall()[0];
cur.execute(f"update citacoes set enviar=1 where rowid = {rowid};");
con.commit();
```
Abaixo, a seleção da frase, mas com o foco de evitar apenas que a mesma imagem seja enviado duas vezes seguidas:
```python
imagem, red, green, blue, link = cur.execute(f"SELECT image, red, green, blue, link FROM images WHERE ultima=0 ORDER BY RANDOM() LIMIT 1;").fetchall()[0];
cur.execute(f"update images set ultima=0 where ultima=1;");
cur.execute(f"update images set ultima=1 where image = '{imagem}';");
con.commit();
color = (red, green, blue);
```
"_Mas por que você não usou uma API de imagem como..._", de fato, eu pensei em usar APIs do tipo como a [loremflickr](https://loremflickr.com/) e a [Lorem Picsum](https://picsum.photos/), o problema é que, como as imagens são aleatórias, há o risco de as palavras terem a mesma cor que o fundo da imagem, tornando a caption ilegível. Eu até considerei editar a imagem com um quadrado monocromático e escrever dentro dele, mas os resultados não me agradaram. No momento, o uso de APIs de imagem continua uma meta de **desenvolvimento futuro**.

O envio da imagem é feito por uma função assíncrona _improvisada_, o link é só uma forma de agradecer a [Unsplash](https://unsplash.com/) pelas imagens gratuitas:
```python
async def enviando_mensagem():
    await client.send_file('me',"temp.jpg",caption=f"[Foto original]({link})");

with client:
    client.loop.run_until_complete(enviando_mensagem());
```
### fazedor_de_imagem
É a função responsável por escrever a frase selecionada na imagem. Por padrão, a frase é escrita a partir do meio da imagem, utilizando a ```quebra_lista_alt``` para quebrar a frase em diferentes linhas (evitando que a frase saia da imagem). No futuro, pretendo adicionar uma variável "offset" com o objetivo de controlar o ponto de início da frase.

## Utilização e Opções
### Help
Para ver as opções disponíveis, basta acessar a opção "-h"
```bash
>python bot.py -h
usage: bot.py [-h] [--autor AUTOR] [--frase FRASE] [--inserir] [--delete DELETE] [--stats] [--teste]

Um bot para gerar imagens e postar no Telegram automaticamente.

options:
  -h, --help       show this help message and exit
  --autor AUTOR    Pesquisar citações de um dado autor.
  --frase FRASE    Pesquisar citações que contenham o termo inserido.
  --inserir        Inserir MANUALMENTE novas frases
  --delete DELETE  Deletar frase com base no rowid
  --stats          Gera relatório sobre as informações na base de dados
  --teste          Gera caption com imagem específica para teste
```

### autor

Essa opção permite visualizar todas as frases escritas pelos autores cujo autor se encaixe no padrão especificado. É interessante notar que a entrada é usada para pesquisar no SQL, ou seja, você pode utilizar o "%" para verificar todos os autores dentro daquele padrão.

```bash
>python bot.py --autor "Oscar%"
autor:  Oscar%
rowid      | autor                | frase
------------------------------------------------------------------------------------
232        | Oscar Wilde          | Os loucos às vezes se curam, os imbecis nunca.
------------------------------------------------------------------------------------
```

### Frase
Similar à opção "autor" porém procura por frases contendo a string. Pode ser utilizada em combinação ou **separado** da função a cima para pesquisar por frases:
```bash
>python bot.py --autor "Fried%" --frase "%macaco%"
autor:  Fried%
frase:  %macaco%
rowid      | autor                | frase
------------------------------------------------------------------------------------
125        | Friedrich Nietzsche  | O macaco é um animal demasiado simpático para que o homem descenda dele.
------------------------------------------------------------------------------------
```

### inserir

Usada para inserir frases novas na base de dados e no arquivo json (o qual é usado para exportar as frases para o Github). Após apertar ENTER será exibido um prompt com as strings inseridas. Use a oportunidade para garantir que digitou corretamente e digite "n" caso tenha notado algum erro ou "y" caso tudo certo.

```bash
>python bot.py --inserir --autor "Terry Pratchett" --frase "A inteligência de uma criatura conhecida como multidão é a raiz quadrada do número de pessoas dentro dela."

-----------------
autor: Terry Pratchett
frase: A inteligência de uma criatura conhecida como multidão é a raiz quadrada do número de pessoas dentro dela.
-----------------
Posso inserir (y/n)? y
Citações:  299
```

### delete

Usada para deletar frases com base no id:

```bash
>python bot.py --delete 299

-----------------
rowid: 299
autor: Terry Pratchett
frase: A inteligência de uma criatura conhecida como multidão é a raiz quadrada do número de pessoas dentro dela.
Deletar?(y/n) y
```
### stats
Fornece estatísticas básicas sobre a base de dados, incluindo número de total de frases, número de frases a ser enviado, número de frases para enviar, autores, dentre outras:

```bash
>python bot.py --stats
GERANDO RELATÓRIO. AGUARDE UM POUCO.
========================================================
+------------------------------+------------+
|        TOTAL DE FRASES       | 300        |
|   TOTAL DE FRASES ENVIADAS   | 16         |
| TOTAL DE FRASES NÃO ENVIADAS | 284        |
+------------------------------+------------+
+-------------------------+------------+
| Abraham Lincoln                | 1          |
| Agatha Christie                | 3          |
| Albert Einstein                | 8          |
| Andrew Carnegie                | 1          |
...
| William Blake                  | 1          |
| William Shakespeare            | 16         |
| Zenão de Cítio, pensador grego | 2          |
+-------------------------+------------+
========================================================
```
### watermark
Adiciona watermark à imagem especificada na linha de comando.

```bash
>python bot.py --watermark "path_para_sua_imagem\imagem_alvo.jpg"
```
## Agradecimentos
* [Unsplash](https://unsplash.com/) - Fotos gratuitas para todos os usos.
* [Matheus Guerra](https://github.com/devmatheusguerra) - 366 frases perfeitas!
* [Lonami](https://github.com/LonamiWebs) - criador do projeto [Telethon](https://github.com/LonamiWebs/Telethon)

## Fontes

* [Automate the Boring Stuff: Breve tutorial sobre o módulo PIL](https://automatetheboringstuff.com/chapter17/)
* [Documentação do Pillow](https://pillow.readthedocs.io/en/stable/reference/ImageFont.html#PIL.ImageFont.FreeTypeFont.getlength)
* [Documentação do Telethon](https://docs.telethon.dev/en/stable/)
* [Lore Ipsum: Utilizei para testar diferentes tamanhos das frases.](https://www.lipsum.com/feed/html)
* [Quebrando vetores em vetores menores](https://www.geeksforgeeks.org/break-list-chunks-size-n-python/)
* [Watermark](https://auth0.com/blog/image-processing-in-python-with-pillow/)
* [Matheus Guerra](https://github.com/devmatheusguerra/frasesJSON/blob/main/frases.json)
