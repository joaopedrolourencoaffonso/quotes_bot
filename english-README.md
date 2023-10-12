# quotes_bot

<p align="center"><a href="https://t.me/dosesdesabedoria"><img src="https://github.com/joaopedrolourencoaffonso/quotes_bot/blob/main/watermark.jpg" width ="250" height="250"></a></p>

A telegram bot to share wisdom with the world! To see the results, just access [my Telegram channel](https://t.me/dosesdesabedoria) or see the phrases on the [official website](https://joaopedrolourencoaffonso.github.io/quotes_bot/).

## News

- Complete project! 🎉🎉🎉
- 1024 phrases for you to use wherever you want (and a few more when I feel like it).

## Future plans

- [x] Generate image-based captions and randomly chosen phrases from database.
- [x] Mechanism to add phrases to the database from the command line.
- [x] Option to search the database from the command line for phrases by an author
- [x] Option to search the database from the command line for phrases with a given string.
- [x] Option to search the database from the command line for sentences by an author with a given string.
- [x] Generate caption from image, phrase and author specified in command line
- [x] Option to check basic statistics about the database.
- [x] Watermark.
- [x] New letter fonts.
- [x] [Extract view statistics directly from Telegram](https://github.com/joaopedrolourencoaffonso/quotes_bot/tree/main/channel)
- [X] Schedule sending of messages automatically.
- [X] Translate code and README to english.
- [ ] Insert all the wise phrases written by the human race.
- [x] Insert all the wise phrases written by the dolphins.

## The code

## SQLite

The script uses a database called ```citations.db```, which can be created as follows:

```python
import sqlite3

con = sqlite3.connect('citations.db');
cur = con.cursor();

cur.execute("CREATE TABLE images (last int, image text, red integer, green integer, blue integer, link text)");
cur.execute("CREATE TABLE "quotes" (author text, phrase text, send int)");
con.commit()
```
The quotes I used are available [here](https://github.com/joaopedrolourencoaffonso/quotes_bot/blob/main/citacoes.json). A list of images is available [here](https://github.com/joaopedrolourencoaffonso/quotes_bot/blob/main/images.json), I emphasize, however, that I am not the owner of these images, they are all available from [ unsplash](https://unsplash.com/).

## Usage and Options
### Help
To see the available options, just access the "-h" option
```bash
>python bot.py -h
usage: bot.py [-h] [--author AUTHOR] [--phrase PHRASE] [--insert] [--delete DELETE] [--stats] [--test]

A bot to generate images and post to Telegram automatically.

options:
   -h, --help show this help message and exit
   --author AUTHOR Search for citations by a given author.
   --phrase PHRASE Search for citations that contain the entered term.
   --insert MANUALLY insert new phrases
   --delete DELETE Delete phrase based on rowid
   --stats Generate a report on the information in the database
   --test Generate caption with specific image for test
```

### author

This option allows you to view all sentences written by authors whose author fits the specified pattern. It is interesting to note that the entry is used to search the SQL, that is, you can use the "%" to check all the authors within that pattern.

```bash
>python bot.py --author "Oscar%"
author: oscar%
rowid | author | phrase
-------------------------------------------------- ----------------------------------
232 | Oscar Wilde | Crazy people are sometimes cured, imbeciles never.
-------------------------------------------------- ----------------------------------
```

### Phrase
Similar to the "author" option but searches for phrases containing the string. Can be used in combination or **separate** from the above function to search for phrases:
```bash
>python bot.py --author "Fried%" --phrase "%monkey%"
Author: Fried%
Phrase: %monkey%
rowid | author | phrase
-------------------------------------------------- ----------------------------------
125 | Friedrich Nietzsche | The monkey is too nice an animal for man to be descended from him.
-------------------------------------------------- ----------------------------------
```

### insert

Used to insert new phrases in the database and in the json file (which is used to export the phrases to Github). After pressing ENTER, a prompt will be displayed with the inserted strings. Use the opportunity to make sure you typed it correctly and type "n" if you notice any errors or "y" if everything is correct.

```bash
>python bot.py --insert --author "Terry Pratchett" --sentence "The intelligence of a creature known as a crowd is the square root of the number of people in it."

-----------------
Author: Terry Pratchett
Quote: The intelligence of a creature known as a crowd is the square root of the number of people in it.
-----------------
Can I enter (y/n)? y
Citations: 299
```

### delete

Used to delete phrases based on id:

```bash
>python bot.py --delete 299

-----------------
rowid: 299
Author: Terry Pratchett
Quote: The intelligence of a creature known as a crowd is the square root of the number of people in it.
Delete?(y/n) y
```
### stats
Provides basic statistics about the database, including total number of sentences, number of sentences to send, number of sentences to send, authors, among others:

```bash
>python bot.py --stats
GENERATING REPORT. WAIT A LITTLE BIT.
========================================================== ======
+------------------------------+------------+
| TOTAL PHRASES | 300 |
| TOTAL PHRASES SENT | 16 |
| TOTAL PHRASES NOT SENT | 284 |
+------------------------------+------------+
+-------------------------+------------+
| Abraham Lincoln | 1 |
| Agatha Christie | 3 |
| Albert Einstein | 8 |
| Andrew Carnegie | 1 |
...
| William Blake | 1 |
| William Shakespeare | 16 |
| Zeno of Citium, Greek thinker | 2 |
+-------------------------+------------+
========================================================== ======
```
### watermark
Adds a watermark to the image specified on the command line.

```bash
>python bot.py --watermark "path_to_your_image\target_image.jpg"
```
# Available Authors
| Author  | Total of Phrases |
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

## Special Tkanks
* [Unsplash](https://unsplash.com/) - Free photos for all uses.
* [Matheus Guerra](https://github.com/devmatheusguerra) - 366 perfect phrases!
* [Lonami](https://github.com/LonamiWebs) - creator of the project [Telethon](https://github.com/LonamiWebs/Telethon)
* [Pensador](https://www.pensador.com/) - Inspiring phrases for all tastes!

## Sources

* [Automate the Boring Stuff: Short tutorial on the PIL module](https://automatetheboringstuff.com/chapter17/)
* [Pillow Documentation](https://pillow.readthedocs.io/en/stable/reference/ImageFont.html#PIL.ImageFont.FreeTypeFont.getlength)
* [Telethon Documentation](https://docs.telethon.dev/en/stable/)
* [Lore Ipsum: I used it to test different sentence lengths.](https://www.lipsum.com/feed/html)
* [Breaking vectors into smaller vectors](https://www.geeksforgeeks.org/break-list-chunks-size-n-python/)
* [Watermark](https://auth0.com/blog/image-processing-in-python-with-pillow/)
* [Matheus Guerra](https://github.com/devmatheusguerra/frasesJSON/blob/main/frases.json)
