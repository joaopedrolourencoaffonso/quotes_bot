# Modulo de importo
import sqlite3, os#, sys
from telethon import TelegramClient
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# Linha de comando
import argparse

#logging
import logging
log_format = "%(levelname)s ;; %(asctime)s ;; %(message)s";
logging.basicConfig(level=logging.INFO,filename="quotes_bot.log",format=log_format);
logger = logging.getLogger();

api_id = API_ID;
api_hash = "API_HASH";

client = TelegramClient('bot', api_id, api_hash)


def watermark(picture):
    try:
        image1 = Image.open('PATH_PARA_SUA_WATERMARK\\watermark.jpg');
        image2 = Image.open(picture);
        altura, comprimento = image2.size;
        watermark = image1.resize((int(altura*0.05), int(altura*0.05)));
        image2.paste(watermark, (int(0.92*altura), int(0.92*comprimento)));
        image2.save(picture);
        image1.close();
        image2.close();
        logger.info(f" - watermark - Watermark adicionada à imagem: {picture}.");

    except Exception as e:
        print("Erro, por favor, veja os logs");
        logger.error(" - watermark - " + str(e));

def stats():
    try:
        con = sqlite3.connect('citacoes.db');
        cur = con.cursor();
        
        print("========================================================");
        '''PEGANDO INFO'''
        total = cur.execute("select count(*) from citacoes;").fetchall()[0][0];
        enviadas = cur.execute("select count(*) from citacoes where enviar = 1;").fetchall()[0][0];
        nao_enviadas = cur.execute("select count(*) from citacoes where enviar = 0;").fetchall()[0][0];
        tamanho_max = cur.execute("select max(length(autor)) from citacoes;").fetchall()[0][0];
        autores = cur.execute("select autor, count(*) from citacoes group by autor").fetchall();

        '''EXPONDO INFO'''
        print("+------------------------------+------------+");
        print("|        TOTAL DE FRASES       | {:<10} |".format(str(total)));
        print("|   TOTAL DE FRASES ENVIADAS   | {:<10} |".format(str(enviadas)));
        print("| TOTAL DE FRASES NÃO ENVIADAS | {:<10} |".format(str(nao_enviadas)));
        print("+------------------------------+------------+");

        print(f"+-{23*'-'}-+-{10*'-'}-+");
        formato = "| {:<" + str(tamanho_max) + "} | {:<10} |";
        for autor in autores:
            print(formato.format(str(autor[0]),str(autor[1])));
        print(f"+-{23*'-'}-+-{10*'-'}-+");

        print("========================================================");

    except Exception as e:
        print("Erro, por favor, veja os logs");
        logger.error(" - stats - " + str(e));

def delete(rowid):
    try:
        if rowid.isdigit():
            rowid = int(rowid);
            con = sqlite3.connect('citacoes.db');
            cur = con.cursor();

            temp = cur.execute(f"select * from citacoes where rowid = {rowid};").fetchall();

            if temp == []:
                return "Desculpe, o rowid especificado não foi encontrado."

            else:
                autor, frase = temp[0][0], temp[0][1];

                print(f'''-----------
    rowid: {rowid}
    autor: {autor}
    frase: {frase};''');

                decisao = input("Deletar?(y/n) ");

                if decisao.lower() in ("y","ye","yes"):
                    cur.execute(f"delete from citacoes where rowid = {rowid};");
                    con.commit();
                    logger.info(f" - Frase deletada - '{rowid}' '{frase}' '{autor}'");

                else:
                    print("Deleção cancelada.");

                con.close();
            

        else:
            return "Desculpe, rowid não é um número inteiro, tente novamente."

    except Exception as e:
        logger.error(" - delete - " + str(e));
    

def inserir_manual(autor, frase):
    try:
        autor = str(autor);
        frase = str(frase);

        print(f"\n-----------------\nautor: {autor}\nfrase: {frase}")

        x = input("-----------------\nPosso inserir (y/n)? ");

        if x not in ('n','y'):
            print("Erro, opção não reconhecida.")
                
        elif frase.find("'") > 0:
            print("Erro, não pode incluir aspas simples");

        elif x == 'n':
            print("Inserção cancelada.");

        else:
            con = sqlite3.connect('PATH_DO_SEU_COMPUTADOR\\citacoes.db');
            cur = con.cursor();

            cur.execute("insert into citacoes values (?,?,0)", (autor, frase));
            con.commit();

            x = cur.execute("select count(*) from citacoes;").fetchall()[0][0];
            print("Citações: ", x);

            '''Editando o arquivo. As edições são mais tarde salvas por comando git'''
            frases = open("PATH_DO_SEU_COMPUTADOR\\citacoes.json","r",encoding="utf8").read();
            frases = frases[:-2] + ',\n {\n  "autor":"' + autor + '",\n  "frase":"' + frase + '"\n}\n]';
            open("PATH_DO_SEU_COMPUTADOR\\citacoes.json","w",encoding="utf8").write(frases);

            con.close();

    except Exception as e:
        logger.error(" - inserir_manual - " + str(e));


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
        imagem = Image.open(f"PATH_PARA_O_DIRETORIO_ONDE_VC_GUARDA_SUAS_IMAGENS\\{imagem}");
        comprimento, altura = imagem.size;
        draw = ImageDraw.Draw(imagem);

        '''tamanho da frase'''
        '''ALERTA: o path abaixo só é válido para o windows 10, edite para outros sistemas operacionais'''
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
parser.add_argument('--delete',default=False, help='Deletar frase com base no rowid');
parser.add_argument('--stats',action="store_true",default=False, help='Gera relatório sobre as informações na base de dados');
parser.add_argument('--teste',action="store_true",default=False, help='Gera caption com imagem específica para teste');
parser.add_argument('--watermark',default=False, type=Path,help='Adciona uma watermark à imagem especificada');

args = parser.parse_args();

def main():
    try:
        '''Adicionando watermark à imagem'''
        if args.watermark:
            watermark(args.watermark);
            exit();
            
        '''PARA TESTAR SE IMAGEM É ADEQUADA OU NÃO'''
        if args.teste:
            color = input("Cor: ");
            imagem = input("Imagem: ");
            frase = input("Frase: ");
            autor = input("Autor: ")
            fazedor_de_imagem(frase, autor, imagem, color);
            exit();
            
        '''OPCOES PARA MANIPULAR A BASE DE DADOS'''
        if args.stats:
            print("GERANDO RELATÓRIO. AGUARDE UM POUCO.");
            stats();
            exit();
            
        if args.delete and (args.frase or args.autor or args.inserir):
            print("Desculpe, mas a opção update não aceita outras opções.");
            exit();

        if args.delete and not (args.frase or args.autor or args.inserir):
            delete(args.delete);
            exit();
        
        if args.inserir and not (args.frase and args.autor):
            print("Desculpe, mas é preciso uma frase e um autor, cada um envolto em áspas duplas.");
            exit();

        if args.inserir and args.frase and args.autor:
            inserir_manual(args.autor, args.frase);
            exit();
            
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
    main();
