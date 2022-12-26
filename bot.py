# Modulo de importo
import sqlite3, os
from telethon import TelegramClient
from PIL import Image, ImageDraw, ImageFont

#logging
import logging
log_format = "%(levelname)s ;; %(asctime)s ;; %(message)s";
logging.basicConfig(level=logging.INFO,filename="quotes_bot.log",format=log_format);
logger = logging.getLogger();

api_id = SUA_API_ID;
api_hash = "SUA_API_HASH";

client = TelegramClient('bot', api_id, api_hash)

def inserir_manual(autor, frase):
    autor = str(autor);
    frase = str(frase);

    print(f"\n-----------------\nautor: {autor}\nfrase: {frase}")

    x = input("-----------------\nPosso inserir (y/n)?");

    if x not in ('n','y'):
        print("Erro, opção não reconhecida.")
            
    elif frase.find("'") > 0:
        print("Erro, não pode incluir aspas simples");

    elif x == 'n':
        print("Inserção cancelada.");

    else:
        con = sqlite3.connect('seu_path\\citacoes.db');
        cur = con.cursor();

        cur.execute("insert into citacoes values (?,?,0)", (autor, frase));
        con.commit();

        x = cur.execute("select count(*) from citacoes;").fetchall()[0][0];
        print("Citações: ", x);

        print("{");
        print(f'  "autor":"{autor}"');
        print(f'  "frase":"{frase}"');
        print("},")

        con.close();


def quebra_lista_alt(lista,comprimento,Font):
    try:
        pedacos = [];
        while lista != []:
            temp = str(lista[0]);
            lista.pop(0);        
            
            while (13/16)*comprimento >= Font.getlength(temp) and len(lista) != 0:
                temp = temp + " " + str(lista[0]);
                lista.pop(0);

            pedacos.append(temp)

        return pedacos;

    except Exception as e:
        logger.error(" - quebra_lista_alt - " + str(e));


def fazedor_de_imagem(frase, autor, imagem, color):
    try:
        '''Convertendo a imagem em objeto escrevível'''
        imagem = Image.open(f"seu_path\\{imagem}");
        comprimento, altura = imagem.size;
        draw = ImageDraw.Draw(imagem);

        '''tamanho da frase'''
        Font = ImageFont.truetype(os.path.join("C:\Windows\Fonts", 'Timesi.ttf'), int(comprimento*0.03125))

        diferenca = 0;
        
        '''Ajustando a frase'''
        if Font.getlength(frase) <= (1.1*comprimento)/4:
            draw.text((comprimento/4, altura/2), frase, fill=color, font=Font);

        else:
            lista = frase.split(" ");

            pedacos  = quebra_lista_alt(lista,comprimento,Font);

            for pedaco in pedacos:
                draw.text((comprimento/16, altura/2 + diferenca), pedaco, fill=color, font=Font);
                diferenca += int(comprimento*0.03125*1.1);

            draw.text((comprimento/4, altura/2 + diferenca), "-- " + autor, fill=color, font=Font);

        imagem.save("temp.jpg")
        return 1;

    except Exception as e:
        logger.error(" - fazedor_de_imagem - " + str(e));
        return 0;


parser = argparse.ArgumentParser(description='Um bot para gerar imagens e postar no Telegram automaticamente.');
parser.add_argument('--autor',default=False, help='Pesquisar citações de um dado autor.');
parser.add_argument('--frase',default=False, help='Pesquisar citações que contenham o termo inserido.');
parser.add_argument('--inserir',action="store_true",default=False, help='Inserir MANUALMENTE novas frases');

args = parser.parse_args();

def main():
    try:
        '''OPCOES PARA MANIPULAR A BASE DE DADOS'''
        '''Mensagem de erro para caso alguém tente inserir uma frase mas esqueça um campo.'''
        if args.inserir and not (args.frase and args.autor):
            print("Desculpe, mas é preciso uma frase e um autor, cada um envolto em áspas duplas.");
            logger.info(f" Erro de insercao de frase");
            exit();

        '''Inserindo frase. Utiliza input pois supõe que você está fazendo MANUALMENTE. Não é difícil fazer uma versão sem, mas como não preciso, vou deixar assim.'''
        if args.inserir and args.frase and args.autor:
            inserir_manual(args.autor, args.frase);
            exit();
            
        '''Pesquisar frases na base de dados entradas que tenham autor E frase com as palavras especificadas. Perceba que não há filtro contra
        injeções SQL, justamente para facilitar lançar queryes'''
        if args.autor and args.frase:
            con = sqlite3.connect('citacoes.db');
            cur = con.cursor();
            
            print("autor: ",str(args.autor));
            print("frase: ",str(args.frase));
            print("{:<10} | {:<20} | {:<100}".format("rowid","autor", "frase"));
            print("------------------------------------------------------------------------------------");
            for row in cur.execute(f"select rowid, * from citacoes where autor like '{str(args.autor)}' and frase like '{str(args.frase)}'").fetchall():
                print ("{:<10} | {:<20} | {:<100}".format(row[0], row[1], row[2]))
                print("------------------------------------------------------------------------------------");

            con.close()
            exit();
        
        '''Pesquisar todas as entradas na DB cujo o nome do autor tenha as palavras especificadas'''
        if args.autor:
            con = sqlite3.connect('citacoes.db');
            cur = con.cursor();
            
            print("autor: ",str(args.autor));
            print("{:<10} | {:<20} | {:<100}".format("rowid","autor", "frase"));
            print("------------------------------------------------------------------------------------");
            for row in cur.execute(f"select rowid, * from citacoes where autor like '{str(args.autor)}'").fetchall():
                print ("{:<10} | {:<20} | {:<100}".format(row[0], row[1], row[2]))
                print("------------------------------------------------------------------------------------");

            con.close()
            exit();

        '''Pesquisar todas as entradas na DB cuja frase tenha as palavras especificadas'''
        if args.frase:
            con = sqlite3.connect('citacoes.db');
            cur = con.cursor();
            
            print("frase: ",str(args.frase));
            print("{:<10} | {:<20} | {:<100}".format("rowid","autor", "frase"));
            print("------------------------------------------------------------------------------------");
            for row in cur.execute(f"select rowid, * from citacoes where frase like '{str(args.frase)}'").fetchall():
                print ("{:<10} | {:<20} | {:<100}".format(row[0], row[1], row[2]))
                print("------------------------------------------------------------------------------------");

            con.close()
            exit();

        '''GERANDO E ENVIANDO IMAGEM'''
        resultado = 0;
        while resultado == 0:
            con = sqlite3.connect('citacoes.db');
            cur = con.cursor();

            # Selecionando a frase
            rowid, autor, frase = cur.execute(f"select rowid, autor, frase from citacoes where enviar = 0 ORDER BY RANDOM() LIMIT 1;").fetchall()[0];
            cur.execute(f"update citacoes set enviar=1 where rowid = {rowid};");
            con.commit();

            # Selecionando a imagem
            imagem, red, green, blue, link = cur.execute(f"SELECT image, red, green, blue, link FROM images WHERE ultima=0 ORDER BY RANDOM() LIMIT 1;").fetchall()[0];
            cur.execute(f"update images set ultima=0 where ultima=1;");
            cur.execute(f"update images set ultima=1 where image = '{imagem}';");
            con.commit();
            color = (red, green, blue);

            restantes = cur.execute("select count(*) from citacoes where enviar = 0;").fetchall()[0][0];

            con.close();

            resultado = fazedor_de_imagem(frase, autor, imagem, color);

        async def enviando_mensagem():
            await client.send_file('me',"temp.jpg",caption=f"[Foto original]({link})");

        with client:
            client.loop.run_until_complete(enviando_mensagem());

        logger.info(f" - sucesso - '{frase}' '{autor}' '{imagem}' - {restantes} frases restantes");

    except Exception as e:
        logger.error(f" - main - " + str(e));

if __name__ == '__main__':
    main()
