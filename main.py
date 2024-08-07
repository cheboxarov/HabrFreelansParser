from telebot.async_telebot import AsyncTeleBot
import telebot
import json
from Services.HabrSender import habr
from DBManager.db import DbManager
from multiprocessing import Process
from Services.FLSender import fl
from threading import Thread


settings = json.loads(open("config.json", "r").read())
db = DbManager('sqlite:///database')
token = settings["token"]
bot = AsyncTeleBot(token)

@bot.message_handler(content_types=['text'])
async def handle_message(message):
    user_id = message.from_user.id
    username = message.from_user.username
    if db.user.is_user_exist(user_id):
        await bot.send_message(user_id, "С возвращением!")
    else:
        db.user.add_user(user_id, username)
        await bot.send_message(user_id, "Добро пожаловать в бота!")

def services_pooling():
    b = telebot.TeleBot(token)
    h = habr(b, db)
    f = fl(b, db)
    first_start = True
    while True:
        try:
            th_h = Thread(target=h.main_pool, kwargs={"first_start":first_start})
            # th_f = Thread(target=f.main_pool)
            th_h.start()
            # th_f.start()
            th_h.join()
            # th_f.join()
            first_start = False
        except Exception as e:
            print("Exception occurred", e)


async def main():
    Process(target=services_pooling, daemon=False).start()
    await bot.infinity_polling()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
