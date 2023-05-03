# Modulo de importo
from telethon import TelegramClient
from datetime import datetime, timedelta

# Linha de comando
import argparse

# Configuracao
api_id = "API_ID";
api_hash = "API_HASH";

#logging
import logging
log_format = "%(levelname)s ;; %(asctime)s ;; %(message)s";
logging.basicConfig(level=logging.INFO,filename="channel.log",format=log_format);
logger = logging.getLogger();

#Permite exportar para arquivos pelo ">"
import sys
sys.stdout.reconfigure(encoding='utf-8')

client = TelegramClient('bot', api_id, api_hash)

async def lista_dialogos():
    try:
        print("+--------------------------+--------------------------+")
        async for dialog in client.iter_dialogs():
            print("|{:<25} | {:<25}|".format(dialog.name,dialog.id));

        print("+--------------------------+--------------------------+")

    except Exception as e:
        print("Erro, por favor, veja os logs");
        logger.error(f" - lista_dialogos - " + str(e));

async def estatisticas(channel_id, min_id, max_id, limite, text):
    try:
        if isinstance(limite, int):
            mensagens = client.iter_messages(int(channel_id), reverse=True, limit=int(limite))

        else:
            if not min_id:
                min_id = 1
                
            if not max_id:
                max_id = 1000000000;

            mensagens = client.iter_messages(int(channel_id), reverse=True, min_id=int(min_id), max_id=int(max_id))
        
        #pegando todas as mensagens desde o ultimo id
        async for message in mensagens:
            try:
                if message.reactions is None:
                    #timedelta for correcting to my timezone (Brasilia)
                    registro = f"{message.date - timedelta(hours=3)}, {message.id}, {message.views}";

                else:
                    temp = ""
                    for reaction in message.reactions.results:
                        emoticon = reaction.reaction.emoticon;
                        count = reaction.count;
                        temp = temp + f"{emoticon}|{count} - ";

                    registro = f"{message.date - timedelta(hours=3)}, {message.id}, {message.views},{temp}";

                if text:
                    texto_da_mensagem = str(message.text);
                    registro = registro + "||| " + str(texto_da_mensagem.replace("\n"," "));
                    # o "|||" é para deixar mais fácil separar o texto da mensagem do restante do output
                    # o replace "\n" é para botar as mensagens em uma única linha

            except Exception as e:
                registro = "ERRO: " + str(e);

            print(registro)

    except Exception as e:
        print("Erro, por favor, veja os logs");
        logger.error(f" - main - " + str(e));

parser = argparse.ArgumentParser(description='Um script para extrair estatísticas sobre canais do Telegram.');
parser.add_argument('--dialogos',action="store_true",default=False, help='Gera uma lista com todos os diálogos do usuário.');
parser.add_argument('--channel',default=False, help='Retorna estatísticas sobre um canal.');
parser.add_argument('--min_id',default=False, help='Retorna mensagens com id SUPERIOR ao específicado, ou seja, desde aquele ponto.');
parser.add_argument('--max_id',default=False, help='Retorna mensagens com id INFERIOR ao específicado, ou seja, desde aquele ponto.');
parser.add_argument('--limite',default=False, help='Retorna as últimas "N" mensagens.');
parser.add_argument('--text',action="store_true",default=False, help='Retorna output com o texto das mensagens.');

args = parser.parse_args();

if __name__ == '__main__':
    with client:
        if args.dialogos:
            client.loop.run_until_complete(lista_dialogos())
        
        if args.channel:
            client.loop.run_until_complete(estatisticas(args.channel, args.min_id, args.max_id, args.limite, args.text));

        if not (args.dialogos or args.channel):
            print("E necessario passar argumentos, verifique a funcao help")
