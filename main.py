import requests
from bs4 import BeautifulSoup
import lxml
import telebot
import json

settings = json.loads(open("config.json", "r").read())

token = settings["token"]
bot = telebot.TeleBot(token)
orders = []

class Order:
    def __init__(self, title:str, description:str, price:str, meta:str):
        self._title = title.replace("\n", "")
        self._description = description
        self._price = price.replace("\n", "")
        self._meta = meta.replace("\n", "")

    def generate_order_text(self):
        order_text = f"Заголовок: {self._title}\n{self._meta}\nЦена: {self._price}\nОписание: {self._description}"
        return order_text

@bot.message_handler(content_types=['text'])
def handle_message(message):
    print(message.from_user.id)
def main():
    first_start = True
    while True:
        haprParsing(first_start)
        first_start = False

def haprParsing(first_start=False):
    content = getHabrHTML()
    if content != None:
        soup = BeautifulSoup(content, 'lxml')
        tasks = soup.find_all('li', class_='content-list__item')
        for val in tasks:
            title = val.find('div', class_='task__title')
            price = val.find('span', class_='count')
            if not orders.count(title.text):
                orders.append(title.text)
                url = title.find('a').get('href')
                order_url = "https://freelance.habr.com" + url
                order = get_order_info(order_url)
                print(order.generate_order_text())
                if not first_start:
                    bot.send_message(954803445, order.generate_order_text() + "\n" + order_url)
        first_start = False
    else:
        print('No content found')

def get_order_info(order_url):
    response = requests.get(order_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    title_soup = soup.find("h2", class_="task__title")
    title = title_soup.text if title_soup is not None else "Без тайтла"
    price_soup = soup.find("div", class_="task__finance")
    price = ""
    if price_soup:
        count_soup = price_soup.find("span", class_="count")
        if count_soup:
            price = count_soup.text if count_soup else ""
    meta_soup = soup.find("div", class_="task__meta")
    meta = meta_soup.text if meta_soup else ""
    desc_soup = soup.find("div", class_="task__description")
    desc = desc_soup.text if desc_soup else ""
    order = Order(title, desc, price, meta)
    return order



def getHabrHTML():
    url = 'https://freelance.habr.com/tasks?categories=development_all_inclusive%2Cdevelopment_backend%2Cdevelopment_frontend%2Cdevelopment_prototyping%2Cdevelopment_ios%2Cdevelopment_android%2Cdevelopment_desktop%2Cdevelopment_bots%2Cdevelopment_games%2Cdevelopment_1c_dev%2Cdevelopment_scripts%2Cdevelopment_voice_interfaces%2Cdevelopment_other'
    responce = requests.get(url)
    if responce.status_code == 200:
        return responce.text
    else:
        print(responce)
        return None

if __name__ == "__main__":
    main()
