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
logging.basicConfig(level=logging.INFO,filename="quotes_bot.log",format=log_format);
logger = logging.getLogger();

async def main():
    try:
        #ultimo id recebido
        try:
            with open("stats.csv", "r") as file:
                last_id = file.readlines()[-1];
                last_id = int(last_id.split(",")[1]);
                
        except:
            last_id = 1;
        
        #pegando todas as mensagens desde o ultimo id
        async for message in client.iter_messages("id_do_canal_do_telegram", reverse=True, min_id=last_id):
            if message.reactions is None:
                #timedelta for correcting to my timezone
                registro = f"\n{message.date - timedelta(hours=3)}, {message.id}, {message.views}";

            else:
                temp = ""
                for reaction in message.reactions.results:
                    emoticon = reaction.reaction.emoticon;
                    count = reaction.count;
                    temp = temp + f"{emoticon}|{count} - ";

                registro = f"\n{message.date - timedelta(hours=3)}, {message.id}, {message.views},{temp}";

            open("stats.csv","a",encoding='utf-8').write(registro)

    except Exception as e:
        print("Erro, por favor, veja os logs");
        logger.error(f" - main - " + str(e));

parser = argparse.ArgumentParser(description='Pegando estatísticas do canal');
        
if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
