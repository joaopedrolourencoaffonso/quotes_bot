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
        print("+---------------------+---------------------+")
        async for dialog in client.iter_dialogs():
            print("|{:<20} | {:<20}|".format(dialog.name,dialog.id));

        print("+---------------------+---------------------+")

    except Exception as e:
        print("Erro, por favor, veja os logs");
        logger.error(f" - lista_dialogos - " + str(e));

async def estatisticas(channel_id, last_id):
    try:
        if not last_id:
            last_id = 1
        
        #pegando todas as mensagens desde o ultimo id
        async for message in client.iter_messages(int(channel_id), reverse=True, min_id=int(last_id)):
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

            print(registro)

    except Exception as e:
        print("Erro, por favor, veja os logs");
        logger.error(f" - main - " + str(e));

parser = argparse.ArgumentParser(description='Um script para extrair estatísticas sobre canais do Telegram.');
parser.add_argument('--dialogos',action="store_true",default=False, help='Gera uma lista com todos os diálogos do usuário.');
parser.add_argument('--channel',default=False, help='Retorna estatísticas sobre um canal.');
parser.add_argument('--last_id',default=False, help='Usado em associacao a "--channel" retorna mensagens com id superior ao especificado, ou seja, desde aquele ponto.');

args = parser.parse_args();

if __name__ == '__main__':
    with client:
        if args.dialogos:
            client.loop.run_until_complete(lista_dialogos())
        
        if args.channel:
            client.loop.run_until_complete(estatisticas(args.channel, args.last_id));

        if not (args.dialogos or args.channel):
            print("E necessario passar argumentos, verifique a funcao help")
