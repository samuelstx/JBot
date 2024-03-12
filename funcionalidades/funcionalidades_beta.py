import telebot
import csv
import requests
from bot.JBot import bot
from bot.variables_globales import *


# Comando /addToBetaTest (Solo funcional en chats privados)
# Este comando envia el enlace para unirse al grupo de test del bot
@bot.message_handler(commands=['addToBetaTest'], chat_types=['private'])
def add_betaTester(message):
    bot.reply_to(message, mensajes['/addToBetaTest'])

