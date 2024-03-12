import telebot
import csv
from bot.JBot import bot
from bot.variables_globales import *

# Comando /listarEnlaces (Solo funcional en chats privados y grupos)
# Este comando lista los enlaces relacionados con el CEEPCC
@bot.message_handler(commands=['listarEnlaces'], chat_types=['private', 'group'])
def list_enlaces(message):
    enlaces = {}
    mensaje = 'Lista de enlaces del CEEPCC:\n\n'
    with open('./csv/enlaces.csv', 'r') as csvfile_enlaces:
        reader = csv.reader(csvfile_enlaces, delimiter=';')
        for row in reader:
            enlaces[row[0]] = {'url': row[1]}
        csvfile_enlaces.close()

    bot.send_message(message.chat.id, mensaje, reply_markup=telebot.util.quick_markup(enlaces, row_width=2))
