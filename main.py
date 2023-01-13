import sys
import time
import schedule
import requests
import telebot
from threading import Thread
from bs4 import BeautifulSoup as bs


token = '5583865102:AAHkK2aug6hgpP6k6HazLMZXf5iAM1YUCRw'
# token = '5809634567:AAFsKbJrHXauGDO3SGnCOhk_mrmafbJJjtk'
bot = telebot.TeleBot(token, threaded=False)
can_close = False
# '1159410829'


def get_user_id():
    file = open('user_id.txt', 'r')

    user_id = []
    for id in file:
        if str(int(id)) not in user_id:
            user_id.append(str(int(id)))

    file.close()

    return user_id


def ad_user_id(new_id):
    file = open('user_id.txt', 'a')

    if str(int(new_id)) in get_user_id():
        return

    file.write(str(new_id) + "\n")
    file.close()

    print("id added")


def get_temp():
    print("get_temp")
    try:
        # soup = bs(open('test.html', 'r').read(), "html.parser")

        URL_TEMPLATE = "http://192.168.0.20/"
        r = requests.get(URL_TEMPLATE)
        soup = bs(r.text, "html.parser")

        temp_values = soup.find_all('tr')
        data = ""
        for name in temp_values:
            if "Socket" in name.text:
                data += "\n" + name.text + " "
            else:
                data += name.text

        return data
    except:
        return "не найден файл"


def send_to_all():
    try:
        user_id = get_user_id()
        if len(user_id) > 0:
            for id in user_id:
                url_request = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + id + "&text=" + get_temp()
                results = requests.get(url_request)
        print("send_to_all")
    except:
        print("error_send_to_all")


def daily_sending():
    print("daily_sending_start")

    schedule.every().day.at("17:48").do(send_to_all)
    # schedule.every(3).seconds.do(close_program())
    while True:
        schedule.run_pending()
        time.sleep(5)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '/start':
        ad_user_id(message.from_user.id)

    elif message.text == '/get':
        bot.send_message(message.from_user.id, get_temp())

    elif message.text == '/get_all_id':
        print("get all id")
        bot.send_message(message.from_user.id, "\n".join(get_user_id()))

    elif message.text == "/help":
        print("/help")
        msg = "/start - подписка на ежедневную рассылку\n" \
              "/get - получить текущую температуру\n" \
              "/get_all_id - получить список id всех пользователей"

        bot.send_message(message.from_user.id, msg)


th = Thread(target=daily_sending, args=())
th.start()


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        time.sleep(15)




