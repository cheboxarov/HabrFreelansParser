import time

import requests
import telebot
from bs4 import BeautifulSoup
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from DBManager.db import DbManager
from g4f.client import Client
from g4f import Provider
import g4f


class Order:
    def __init__(self, title:str, description:str, price:str, meta:str):
        self._title = ''.join([title[i] for i in range(0, len(title)-1) if title[i]+title[i+1] != '  '])
        self._description = ''.join([description[i] for i in range(0, len(description)-1) if description[i]+description[i+1] != '  '])
        self._price = price.replace("\n", "")
        self._meta = meta.replace("\n", "")

    def generate_order_text(self):
        order_text = f"<em>Заявка с <b>freelance.habr.com</b></em>\n\n<b>{self._title}</b><em>\n\n{self._meta}\n\n{self._price}</em>\n{self._description}"
        return order_text


class habr:
    def __init__(self, bot:telebot.TeleBot, db:DbManager):
        self.orders = []
        self.bot = bot
        self.db = db

    def main_pool(self,first_start=False):
        content = self.get_html()
        if content != None:
            soup = BeautifulSoup(content, 'html.parser')
            tasks = soup.find_all('li', class_='content-list__item')
            tasks = tasks[:3]
            tasks = reversed(tasks)
            for val in tasks:
                title = val.find('div', class_='task__title')
                price = val.find('span', class_='count')
                if not self.orders.count(title.text):
                    self.orders.append(title.text)
                    url = title.find('a').get('href')
                    order_url = "https://freelance.habr.com" + url
                    order = self.get_order_info(order_url)
                    if not first_start:
                        markup = InlineKeyboardMarkup()
                        markup.add(InlineKeyboardButton("Ссылка", url=order_url))

                        default = open("prompt.txt", 'r', encoding='utf-8').read()
                        text = order.generate_order_text()
                        client = Client()
                        response = client.chat.completions.create(
                            messages=[{"role": "user", "content": default + text}],
                            provider=Provider.Pizzagpt,
                            model=g4f.models.default
                        )
                        time.sleep(3)
                        print(text)
                        print(response.choices[0].message.content)
                        if "НЕ ПОДХОДИТ" in response.choices[0].message.content:
                            continue
                        for user in self.db.user.get_all_users():
                            self.bot.send_message(user.user_id, text, reply_markup=markup, parse_mode="html")
            first_start = False
        else:
            print('No content found')

    def get_html(self):
        url = 'https://freelance.habr.com/tasks?categories=development_all_inclusive%2Cdevelopment_backend%2Cdevelopment_frontend%2Cdevelopment_prototyping%2Cdevelopment_ios%2Cdevelopment_android%2Cdevelopment_desktop%2Cdevelopment_bots%2Cdevelopment_games%2Cdevelopment_1c_dev%2Cdevelopment_scripts%2Cdevelopment_voice_interfaces%2Cdevelopment_other'
        responce = requests.get(url)
        if responce.status_code == 200:
            return responce.text
        else:
            print(responce)
            return None

    def get_order_info(self, order_url):
        response = requests.get(order_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        title_soup = soup.find("h2", class_="task__title")
        title = title_soup.text if title_soup is not None else "Без тайтла"
        price_soup = soup.find("div", class_="task__finance")
        price = "Цена не указана"
        if price_soup:
            count_soup = price_soup.find("span", class_="count")
            if count_soup:
                price = count_soup.text if count_soup else "Цена не указана"
        meta_soup = soup.find("div", class_="task__meta")
        meta = meta_soup.text if meta_soup else ""
        desc_soup = soup.find("div", class_="task__description")
        desc = desc_soup.text if desc_soup else "Описание не указано"
        order = Order(title, desc, price, meta)
        return order