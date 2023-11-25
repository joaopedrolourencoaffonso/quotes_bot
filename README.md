# quotes_bot

<p align="center"><a href="https://t.me/dosesdesabedoria"><img src="https://github.com/joaopedrolourencoaffonso/quotes_bot/blob/main/watermark.jpg" width="250" height="250"></a></p>

Um bot do telegram para dividir sabedoria com o mundo! Para ver os resultados, basta acessar [meu canal do Telegram](https://t.me/dosesdesabedoria), o [site oficial](https://joaopedrolourencoaffonso.github.io/quotes_bot/) ou meu [canal no Youtube](https://www.youtube.com/@ShortsdeSabedoria/shorts).

## Detalhes

- Projeto completo! 🎉🎉🎉
- 1139 frases para você usar onde quiser (e mais algumas quando eu tiver vontade). 

## Autores

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
- [X] Translate code and README to english.
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

## Autores Disponíveis
| Autor  | Total de Frases |
| ------------- | ------------- |
| Machado de Assis               | 44         |
| Mark Twain                     | 42         |
| Abraham Lincoln                | 36         |
| Stephen King                   | 31         |
| Ruy Barbosa                    | 30         |
| Jean-Jacques Rousseau          | 27         |
| Robert Frost                   | 18         |
| Helen Keller                   | 17         |
| Marco Aurélio                  | 17         |
| Provérbio Chinês               | 17         |
| William Shakespeare            | 17         |
| Douglas Adams                  | 16         |
| Martin Luther King Jr.         | 16         |
| Mahatma Gandhi                 | 15         |
| Benjamin Franklin              | 15         |
| Oscar Wilde                    | 15         |
| Stephen Hawking                | 14         |
| Confúcio                       | 13         |
| John Lock                      | 13         |
| Fernando Pessoa                | 12         |
| Winston Churchill              | 12         |
| Sun Tzu                        | 12         |
| Voltaire                       | 12         |
| Jean-Paul Sartre               | 12         |
| Adam Smith                     | 11         |
| Ayn Rand                       | 11         |
| Pitágoras                      | 11         |
| Charles Chaplin                | 11         |
| Simone de Beauvoir             | 11         |
| Erasmo de Roterdã              | 11         |
| Albert Einstein                | 10         |
| Florence Nightingale           | 10         |
| Franklin D. Roosevelt          | 10         |
| Nicolau Maquiavel              | 10         |
| Pablo Neruda                   | 10         |
| Sêneca                         | 10         |
| Clarice Lispector              | 9          |
| Immanuel Kant                  | 9          |
| Thomas Hobbes                  | 9          |
| Franz Kafka                    | 8          |
| T. S. Eliot                    | 8          |
| Charles Bukowski               | 7          |
| Graciliano Ramos               | 7          |
| Milton Santos                  | 7          |
| René Descartes                 | 7          |
| Carl Sagan                     | 6          |
| Karl Marx                      | 6          |
| Marie Curie                    | 6          |
| Dito Popular                   | 6          |
| Friedrich Nietzsche            | 6          |
| Renato Russo                   | 6          |
| Simone Weil                    | 6          |
| Edmund Burke                   | 6          |
| Harvey Specter                 | 6          |
| Henry Ford                     | 5          |
| Malcolm X                      | 5          |
| Jean-Jacques Russeu            | 5          |
| Neil deGrasse Tyson            | 5          |
| Buda                           | 4          |
| Júlio Verne                    | 4          |
| Kurt Vonnegut                  | 4          |
| São Tomás de Aquino            | 4          |
| Steve Jobs                     | 4          |
| Terry Pratchett                | 4          |
| Rachel de Queiroz              | 4          |
| Robin Williams                 | 4          |
| Tommas Shelby                  | 4          |
| Lao-Tsé                        | 4          |
| Otto von Bismarck              | 4          |
| Agatha Christie                | 3          |
| Aristóteles                    | 3          |
| Peter Drucker                  | 3          |
| Carl Sewell                    | 3          |
| Stan Lee                       | 3          |
| Richard Adams                  | 3          |
| Nikola Tesla                   | 3          |
| Claus Moller                   | 3          |
| Malala Yousafzai               | 3          |
| Dalai Lama                     | 2          |
| Elbert Hubbard                 | 2          |
| Samuel Johnson                 | 2          |
| Eleanor Roosvelt               | 2          |
| Mozi                           | 2          |
| Dito Popular Brasileiro        | 2          |
| Carl Sandburg                  | 2          |
| Walt Disney                    | 2          |
| Zenão de Cítio, pensador grego | 2          |
| Provérbio italiano             | 2          |
| Protágoras de Abdera           | 2          |
| Provérbio Alemão               | 2          |
| Will Rogers                    | 2          |
| Will Smith                     | 2          |
| John F. Kennedy                | 2          |
| John Nash                      | 2          |
| Michael Jordan                 | 2          |
| Aldous Huxley                  | 1          |
| Alexander G. Bell              | 1          |
| Alexander Soljenitsyn          | 1          |
| Alfred Tennyson                | 1          |
| Alvin Toffler                  | 1          |
| Amelia Earhart                 | 1          |
| Anatole France                 | 1          |
| Anderson Silva                 | 1          |
| Andrew Carnegie                | 1          |
| André Gide                     | 1          |
| Anne Frank                     | 1          |
| Antoine de Saint               | 1          |
| Ashton Kutcher                 | 1          |
| Audrey Hepburn                 | 1          |
| Ayn Randy                      | 1          |
| Babe Ruth                      | 1          |
| Barrie Hopson                  | 1          |
| Bertrand Russell               | 1          |
| Beverly Sills                  | 1          |
| Bill Gates                     | 1          |
| Bob Esponja                    | 1          |
| Bob Marley                     | 1          |
| Booker T. Washington           | 1          |
| Carmen Miranda                 | 1          |
| Catherine Romano               | 1          |
| Cesare Cant                    | 1          |
| Charles Brower                 | 1          |
| Charles Dickens                | 1          |
| Charles Swindoll               | 1          |
| Churton Collin                 | 1          |
| Coco Chanel                    | 1          |
| Constantino C. Vigil           | 1          |
| Cotton                         | 1          |
| Célia Chaim                    | 1          |
| Dave Lewis                     | 1          |
| Dave Weinbaum                  | 1          |
| Dean Rusk                      | 1          |
| Denis Waitley                  | 1          |
| Denis Walker                   | 1          |
| Diógenes Laércio               | 1          |
| Dom Resende Costa              | 1          |
| Doutor Seuss                   | 1          |
| Duke Ellington                 | 1          |
| Earle Wilson                   | 1          |
| Elmer Letterman                | 1          |
| Enzo Ferrari                   | 1          |
| Ernest Hemingway               | 1          |
| Eugène Ionesco                 | 1          |
| Eugéne Ionesco                 | 1          |
| Fiódor Dostoiévski             | 1          |
| Forrest Gump                   | 1          |
| François La Rochefoucauld      | 1          |
| Georg Wilhelm                  | 1          |
| George Eliot                   | 1          |
| George Gurdjieff               | 1          |
| George Lichtenberg             | 1          |
| George Lucas                   | 1          |
| George Santayana               | 1          |
| George Savile                  | 1          |
| George Washington              | 1          |
| Geraldo Vandré                 | 1          |
| Gloria Steinem                 | 1          |
| H. Jackson Brown Jr.           | 1          |
| H. Ross Perot                  | 1          |
| Harols Abbott                  | 1          |
| Henri Barbusse                 | 1          |
| Henry D. Thoreau               | 1          |
| Horácio                        | 1          |
| Hugh Prather                   | 1          |
| J. P. L. Affonso               | 1          |
| J. Walters                     | 1          |
| Jacques Prévert                | 1          |
| Jan Carlzon                    | 1          |
| Jean Paul Sartre               | 1          |
| Joel L. Griffith               | 1          |
| Joel Osteen                    | 1          |
| John S. Mill                   | 1          |
| John Sewell                    | 1          |
| John Tschohl                   | 1          |
| John Wayne                     | 1          |
| John Young                     | 1          |
| João Guimar                    | 1          |
| Karl Albrecht                  | 1          |
| Ken O                          | 1          |
| Kevin Kruse                    | 1          |
| Lao Tsu                        | 1          |
| Lao Tzu                        | 1          |
| Lao-Tze                        | 1          |
| Larry Wilson                   | 1          |
| Laurence J. Peter              | 1          |
| Lecouve                        | 1          |
| Leonard Berry                  | 1          |
| Lord Chesterfield              | 1          |
| Louis Pasteur                  | 1          |
| Louisa M. Alcott               | 1          |
| M. J. Babcock                  | 1          |
| Malcolm Forbes                 | 1          |
| Marabel Morgan                 | 1          |
| Mario Andretti                 | 1          |
| Mark van Doren                 | 1          |
| Marry W. Shelley               | 1          |
| Masaaki Imai                   | 1          |
| Michael de Montaigne           | 1          |
| Moliere                        | 1          |
| N. V. Peale                    | 1          |
| Neil Armstrong                 | 1          |
| Nelson Mandel                  | 1          |
| Norman Bawes                   | 1          |
| Norman V. Peale                | 1          |
| Norman Vaughan                 | 1          |
| Norman Vincent Peale           | 1          |
| Oliver W. Holmes               | 1          |
| Omar Khayyam                   | 1          |
| Onassis                        | 1          |
| Oprah Winfrey                  | 1          |
| Orison S. Marden               | 1          |
| Orson Welles                   | 1          |
| Paul Deschanel                 | 1          |
| Paulo Freire                   | 1          |
| Peter Ducker                   | 1          |
| Peter Schutz                   | 1          |
| Phill Knight                   | 1          |
| Abbie Hoffman                  | 1          |
| Platão                         | 1          |
| Provérbio Chin                 | 1          |
| Provérbio Estadunidense        | 1          |
| Provérbio Galês                | 1          |
| Provérbio Islandês             | 1          |
| Provérbio Japonês              | 1          |
| Provérbio Latino               | 1          |
| Provérbio Oriental             | 1          |
| Provérbio Persa                | 1          |
| Provérbio espanhol             | 1          |
| Provérbio grego                | 1          |
| Provérbio romano               | 1          |
| R. Buckminster Fuller          | 1          |
| Ralph W. Emerson               | 1          |
| Reinaldo Polito                | 1          |
| Richard Whiteley               | 1          |
| Robert Frost (adaptado)        | 1          |
| Robert H. Schuller             | 1          |
| Robert Peterson                | 1          |
| Ron Bern                       | 1          |
| Ronald Osborn                  | 1          |
| Roy L. Smith                   | 1          |
| Sam Walton                     | 1          |
| Samuel Beckett                 | 1          |
| Samuel Smiles                  | 1          |
| Santo Agostinho                | 1          |
| Segundo Mandamento da TAM      | 1          |
| Sholom Aleichem                | 1          |
| Simone de Beauvoi              | 1          |
| Soren Kierkegaard              | 1          |
| Stephen Covey                  | 1          |
| Stubby Currence                | 1          |
| Sérgio Almeida                 | 1          |
| Sétimo Mandamento da TAM       | 1          |
| Sócrates                       | 1          |
| Sófocles                       | 1          |
| T.S. Eliot                     | 1          |
| Theodore Roosvelt              | 1          |
| Thomas Carlyle                 | 1          |
| Vincent Van Gogh               | 1          |
| W. F. Grenfel                  | 1          |
| W. S. Landor                   | 1          |
| Walter Gagehot                 | 1          |
| Walter Reuther                 | 1          |
| Warren Buffet                  | 1          |
| Warren Buffett                 | 1          |
| William Blake                  | 1          |
| William McKnight               | 1          |
| xkcd                           | 1          |
| Abigail Van Buren              | 1          |

## Agradecimentos
* [Unsplash](https://unsplash.com/) - Fotos gratuitas para todos os usos.
* [Matheus Guerra](https://github.com/devmatheusguerra) - 366 frases perfeitas!
* [Lonami](https://github.com/LonamiWebs) - criador do projeto [Telethon](https://github.com/LonamiWebs/Telethon)
* [Pensador](https://www.pensador.com/) - Frases inspiradoras para todos os gostos!

## Fontes

* [Automate the Boring Stuff: Breve tutorial sobre o módulo PIL](https://automatetheboringstuff.com/chapter17/)
* [Documentação do Pillow](https://pillow.readthedocs.io/en/stable/reference/ImageFont.html#PIL.ImageFont.FreeTypeFont.getlength)
* [Documentação do Telethon](https://docs.telethon.dev/en/stable/)
* [Lore Ipsum: Utilizei para testar diferentes tamanhos das frases.](https://www.lipsum.com/feed/html)
* [Quebrando vetores em vetores menores](https://www.geeksforgeeks.org/break-list-chunks-size-n-python/)
* [Watermark](https://auth0.com/blog/image-processing-in-python-with-pillow/)
* [Matheus Guerra](https://github.com/devmatheusguerra/frasesJSON/blob/main/frases.json)
