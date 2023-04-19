import telebot
from database import DatabaseConnector as DC
import getpass



TOKEN = '6144079415:AAEdTd_9LsSURCpUy7ZXEFiRjfBsha_Y4Ec'
bot = telebot.TeleBot(TOKEN)
USERNAME = getpass.getuser()
PORT = 5433
db = DC(USERNAME, PORT)


#-----------------------------------------------------------------------------------------------------------------------
@bot.message_handler(commands=['add'])
def add_book(message):
    bot.send_message(message.chat.id, "Введите название книги:")
    bot.register_next_step_handler(message, add_book_author)


def add_book_author(message):
    book_name = message.text
    bot.send_message(message.chat.id, "Введите автора:")
    bot.register_next_step_handler(message, add_book_year, book_name)


def add_book_year(message, book_name):
    book_author = message.text
    bot.send_message(message.chat.id, "Введите год издания:")
    bot.register_next_step_handler(message, add_book_done, book_name, book_author)


def add_book_done(message, book_name, book_author):
    book_year = int(message.text)
    # Добавляем книгу в базу данных
    book_id = db.add(book_name, book_author, book_year)
    if book_id:
        bot.send_message(message.chat.id, f"Книга добавлена (id {book_id})")
    else:
        bot.send_message(message.chat.id, "Ошибка при добавлении книги") 


#-----------------------------------------------------------------------------------------------------------------------
@bot.message_handler(commands=['delete'])
def delete_book(message):
    bot.send_message(message.chat.id, "Введите название книги:")
    bot.register_next_step_handler(message, delete_book_author)


def delete_book_author(message):
    book_name = message.text
    bot.send_message(message.chat.id, "Введите автора:")
    bot.register_next_step_handler(message, delete_book_year, book_name)


def delete_book_year(message, book_name):
    book_author = message.text
    bot.send_message(message.chat.id, "Введите год издания:")
    bot.register_next_step_handler(message, delete_book_confirm, book_name, book_author)


def delete_book_confirm(message, book_name, book_author):
    book_year = message.text
    # Проверяем, есть ли книга в базе данных
    book_id = db.get_book(book_name, book_author, book_year)
    if book_id:
        bot.send_message(message.chat.id, f"Найдена книга: {book_name} {book_author} {book_year}. Удаляем?")
        bot.register_next_step_handler(message, delete_book_done, book_id[0][0])
    else:
        bot.send_message(message.chat.id, "Невозможно удалить книгу")


def delete_book_done(message, book_id):
    if message.text.lower() == 'да':
        # Удаляем книгу из базы данных
        db.delete(book_id)
        bot.send_message(message.chat.id, "Книга удалена")
    else:
        bot.send_message(message.chat.id, "Книга не удалена")


#-----------------------------------------------------------------------------------------------------------------------
@bot.message_handler(commands=['find'])
def find_book(message):
    bot.send_message(message.chat.id, "Введите название книги:")
    bot.register_next_step_handler(message, find_book_author)


def find_book_author(message):
    book_name = message.text
    bot.send_message(message.chat.id, "Введите автора:")
    bot.register_next_step_handler(message, find_book_year, book_name)


def find_book_year(message, book_name):
    book_author = message.text
    bot.send_message(message.chat.id, "Введите год издания:")
    bot.register_next_step_handler(message, find_book_done, book_name, book_author)


def find_book_done(message, book_name, book_author):
    book_year = message.text
    # Ищем книгу в базе данных
    book = db.get_book(book_name, book_author, book_year)
    if len(book) != 0:
        bot.send_message(message.chat.id, f"Найдена книга: {book_name} {book_author} {book_year}")
    else:
        bot.send_message(message.chat.id, "Такой книги у нас нет")


# -----------------------------------------------------------------------------------------------------------------------
@bot.message_handler(commands=['borrow'])
def borrow_book(message):
    bot.send_message(message.chat.id, "Введите название книги:")
    bot.register_next_step_handler(message, borrow_book_author)


def borrow_book_author(message):
    book_name = message.text
    bot.send_message(message.chat.id, "Введите автора:")
    bot.register_next_step_handler(message, borrow_book_year, book_name)


def borrow_book_year(message, book_name):
    book_author = message.text
    bot.send_message(message.chat.id, "Введите год издания:")
    bot.register_next_step_handler(message, borrow_book_confirm, book_name, book_author)


def borrow_book_confirm(message, book_name, book_author):
    book_year = message.text
    book_id = db.get_book(book_name, book_author, book_year)
    if book_id:
        bot.send_message(message.chat.id, f"Найдена книга: {book_name} {book_author} {book_year}. Берем?")
        bot.register_next_step_handler(message, borrow_book_done, book_id[0][0])


def borrow_book_done(message, book_id):
    if message.text.lower() == 'да':
        if (db.borrow(book_id, message.from_user.id)):
            bot.send_message(message.chat.id, "Вы взяли книгу")
        else:
            bot.send_message(message.chat.id, "Книгу сейчас невозможно взять")


# -----------------------------------------------------------------------------------------------------------------------
@bot.message_handler(commands=['list'])
def send_list(message):
    # тут нужна функция которая возвращает список всех книг
    book_list = db.list_books()
    str_list = ''
    for book in book_list:
        str_list += f'{book[1]}, {book[2]}, {book[3]}'
        if not(book[-1] is None):
            str_list += ' (удалена)'
        str_list += ';\n'
    bot.send_message(message.chat.id, str_list)


# -----------------------------------------------------------------------------------------------------------------------
@bot.message_handler(commands=['retrieve'])
def retrieve_book(message):
    str = db.retrieve(message.from_user.id)
    if(str != False):
        retrieve_msg = f'Вы вернули книгу {str}'
        bot.send_message(message.chat.id, retrieve_msg)


# -----------------------------------------------------------------------------------------------------------------------
@bot.message_handler(commands=['stats'])
def send_stats(message):
    bot.send_message(message.chat.id, 'Введите название книги:')
    bot.register_next_step_handler(message, get_book_title)


def get_book_title(message):
    book_title = message.text
    bot.send_message(message.chat.id, 'Введите автора:')
    bot.register_next_step_handler(message, get_book_author, book_title)


def get_book_author(message, book_title):
    book_author = message.text
    bot.send_message(message.chat.id, 'Введите год издания:')
    bot.register_next_step_handler(message, get_book_year, book_title, book_author)


def get_book_year(message, book_title, book_author):
    book_year = message.text
    book_id = db.get_book(book_title, book_author, book_year)
    if book_id:
        bot.send_message(message.chat.id, f'Статистика доступна по адресу http://127.0.0.1:8080/download/{book_id[0][0]}')
    else:
        bot.send_message(message.chat.id, "Нет такой книги")




bot.polling()
