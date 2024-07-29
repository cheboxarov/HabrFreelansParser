import requests
from bs4 import BeautifulSoup
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from DBManager.db import DbManager

class Order:
    def __init__(self, title:str, price:str, desc:str, deadline:str, link:str):
        self.title = ''.join([title[i] for i in range(0, len(title)-1) if title[i]+title[i+1] != '  '])
        self.price = price
        self.desc = ''.join([desc[i] for i in range(0, len(desc)-1) if desc[i]+desc[i+1] != '  '])
        self.deadline = deadline
        self.link = link
    def __str__(self):
        text = f'<em>Заявка с <b>fl.ru</b>\n\n</em><b>{self.title}</b>\n\n<em>{self.price}\n\n{self.deadline}</em>\n\n{self.desc}'
        return text

class fl:
    orders = []
    _cookies = {
        '__ddg1_': 'Jkcm5u7NL3oUIrkOxxyy',
        '_gid': 'GA1.2.783434416.1720002259',
        '_ga_cid': '1763790807.1720002259',
        '_ym_uid': '1720002259578971447',
        '_ym_d': '1720002259',
        '_ym_isad': '2',
        '_ym_visorc': 'w',
        'analytic_id': '1720002259950148',
        'XSRF-TOKEN': '2xn4rq2eghOgbgTDm77Z1rvOw6YtmZFZPBeh6znv',
        'id': '8679323',
        'name': 'wlovemrock',
        'pwd': '80e36715ea2c0721aced8fd3465069fb',
        'PHPSESSID': 'Gjt8Obu7CCvhvrhimR7ygfOB8G1h7Zn1dRG8CJ2G',
        'user_device_id': '9ow3thzc110ln66wu1g0eddfph1keduu',
        'mindboxDeviceUUID': '0af512b8-9939-42e9-979c-11b4cbb69755',
        'directCrm-session': '%7B%22deviceGuid%22%3A%220af512b8-9939-42e9-979c-11b4cbb69755%22%7D',
        'new_pf0': '1',
        'new_pf10': '1',
        'hidetopprjlenta': '0',
        '_ga': 'GA1.2.1763790807.1720002259',
        '_ga_RD9LL0K106': 'GS1.1.1720002258.1.1.1720002474.36.0.0',
    }
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru-RU,ru;q=0.9',
        'cache-control': 'max-age=0',
        # 'cookie': '__ddg1_=Jkcm5u7NL3oUIrkOxxyy; _gid=GA1.2.783434416.1720002259; _ga_cid=1763790807.1720002259; _ym_uid=1720002259578971447; _ym_d=1720002259; _ym_isad=2; _ym_visorc=w; analytic_id=1720002259950148; XSRF-TOKEN=2xn4rq2eghOgbgTDm77Z1rvOw6YtmZFZPBeh6znv; id=8679323; name=wlovemrock; pwd=80e36715ea2c0721aced8fd3465069fb; PHPSESSID=Gjt8Obu7CCvhvrhimR7ygfOB8G1h7Zn1dRG8CJ2G; user_device_id=9ow3thzc110ln66wu1g0eddfph1keduu; mindboxDeviceUUID=0af512b8-9939-42e9-979c-11b4cbb69755; directCrm-session=%7B%22deviceGuid%22%3A%220af512b8-9939-42e9-979c-11b4cbb69755%22%7D; new_pf0=1; new_pf10=1; hidetopprjlenta=0; _ga=GA1.2.1763790807.1720002259; _ga_RD9LL0K106=GS1.1.1720002258.1.1.1720002474.36.0.0',
        'priority': 'u=0, i',
        'referer': 'https://www.fl.ru/projects/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }

    def __init__(self, bot:telebot.TeleBot, db:DbManager):
        self.bot = bot
        self.db = db

    def main_pool(self):
        for order in self.get_orders():
            if order.link in self.orders:
                continue
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("Ссылка", url=order.link))
            print(self.db.user.get_all_users())
            for user in self.db.user.get_all_users():
                self.bot.send_message(user.user_id, str(order), reply_markup=markup, parse_mode="html")
            self.orders.append(order.link)

    def _get_order(self, link):
        response = requests.get(link, cookies=self._cookies,
                                headers=self.headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('h1', class_='text-1 d-flex align-items-center').text.replace('\n', '').replace('\t', '').replace('  ', '')
        try:
            price = soup.find('div', class_='text-4 mb-4').text.replace('\n', '').replace('\t', '').replace('  ', '')
        except:
            price = "Цена не указана"
        try:
            desc = soup.find('div', class_='text-5 b-layout__txt_padbot_20').text.replace('\n', ' ').replace('\t', '').replace('  ', '')
        except:
            desc = "Описание не указано"
        try:
            deadline = soup.find('div', class_="mt-12 text-4").text.replace('\n', '').replace('\t', '').replace('  ', '')
        except:
            deadline = 'Дедлайн не указан'
        print(title,'\n', price, '\n', desc, '\n', deadline)
        order = Order(title, price, desc, deadline, link)
        return order

    def get_orders(self):
        response = requests.get('https://www.fl.ru/projects/category/programmirovanie/', cookies=self._cookies,
                                headers=self.headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        orders = []
        for order_html in  soup.findAll('div', attrs={'data-id': 'qa-lenta-1'}):
            title_soup = order_html.find('a')
            link = title_soup.get("href")
            order = self._get_order('https://www.fl.ru'+link)
            orders.append(order)
        return orders
