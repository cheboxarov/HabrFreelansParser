import requests
from bs4 import BeautifulSoup
import lxml
import telebot
token = "TOKEN"
bot = telebot.TeleBot(token)
orders = []
@bot.message_handler(content_types=['text'])
def handle_message(message):
    print(message.from_user.id)
def main():
    first_start = True
    while True:
        haprParsing(first_start)
        first_start = False

def haprParsing(first_start=None):
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
                pr = ''
                if price:
                    pr = "\n"+price.text
                print(title.text + pr + "\nhttps://freelance.habr.com" + url + "\n")
                if not first_start:
                    bot.send_message(954803445, title.text + pr + "\nhttps://freelance.habr.com" + url + "\n")
        first_start = False
    else:
        print('No content found')

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
