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


'''Cria nova imagem'''
def fazedor_de_imagem(frase, autor, imagem, color):
    try:
        '''Convertendo a imagem em objeto escrevível'''
        imagem = Image.open(f"PATH_DO_DIRETORIO_COM_SUAS_IMAGENS{imagem}");
        comprimento, altura = imagem.size;
        draw = ImageDraw.Draw(imagem);

        '''tamanho da frase. CUIDADO: o path para o arquivo de fontes pode ser diferente no seu computador/OS'''
        Font = ImageFont.truetype(os.path.join("C:\Windows\Fonts", 'Timesi.ttf'), int(comprimento*0.03125));

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


def main():
    try:        
        resultado = 0;

        '''Esse loop é para garantir que, caso haja erro na geração de uma imagem, outra seja feita'''
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
            await client.send_file('me',"temp.jpg",caption=f"[Foto original]({link})")

        with client:
            client.loop.run_until_complete(enviando_mensagem());

        logger.info(f" - sucesso - '{frase}' '{autor}' '{imagem}'  - {restantes} frases restantes");

    except Exception as e:
        logger.error(f" - main - " + str(e));

if __name__ == '__main__':
    main();
