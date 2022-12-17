# quotes_bot

Um bot do telegram para dividir sabedoria com o mundo!Para ver os resultados, basta acessa [meu canal do Telegram](t.me/dosesdesabedoria).

## Base de Dados

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

## O código

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

### Fontes

* [Automate the Boring Stuff: Breve tutorial sobre o módulo PIL](https://automatetheboringstuff.com/chapter17/)
* [Documentação do Pillow](https://pillow.readthedocs.io/en/stable/reference/ImageFont.html#PIL.ImageFont.FreeTypeFont.getlength)
* [Documentação do Telethon](https://docs.telethon.dev/en/stable/)
* [Lore Ipsum: Utilizei para testar diferentes tamanhos das frases.](https://www.lipsum.com/feed/html)
* [Quebrando vetores em vetores menores](https://www.geeksforgeeks.org/break-list-chunks-size-n-python/)
