# quotes_bot

<p align="center"><a href="https://t.me/dosesdesabedoria"><img src="https://github.com/joaopedrolourencoaffonso/quotes_bot/blob/main/watermark.jpg" width ="250" height="250"></a></p>

A telegram bot to share wisdom with the world! To see the results, just access [my Telegram channel](https://t.me/dosesdesabedoria) or see the phrases on the [official website](https://joaopedrolourencoaffonso.github.io/quotes_bot/).

## News

- Our database reached 983 phrases! 🎉🎉🎉
- New "watermark" option allows adding watermarks to images via the command line.
- New font options

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
- [ ] "install" option to create sqlite database from a single command.
- [ ] Automate upload of new phrases on Github (currently done by manual git push)
- [ ] Translate code and README to english.
- [ ] Generate images based on artificial intelligence
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

## Thanks
* [Unsplash](https://unsplash.com/) - Free photos for all uses.
* [Matheus Guerra](https://github.com/devmatheusguerra) - 366 perfect phrases!
* [Lonami](https://github.com/LonamiWebs) - creator of the project [Telethon](https://github.com/LonamiWebs/Telethon)

## Sources

* [Automate the Boring Stuff: Short tutorial on the PIL module](https://automatetheboringstuff.com/chapter17/)
* [Pillow Documentation](https://pillow.readthedocs.io/en/stable/reference/ImageFont.html#PIL.ImageFont.FreeTypeFont.getlength)
* [Telethon Documentation](https://docs.telethon.dev/en/stable/)
* [Lore Ipsum: I used it to test different sentence lengths.](https://www.lipsum.com/feed/html)
* [Breaking vectors into smaller vectors](https://www.geeksforgeeks.org/break-list-chunks-size-n-python/)
* [Watermark](https://auth0.com/blog/image-processing-in-python-with-pillow/)
* [Matheus Guerra](https://github.com/devmatheusguerra/frasesJSON/blob/main/frases.json)
