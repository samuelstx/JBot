import csv
from bot.JBot import bot
from bot.variables_globales import *

# Lectura del fichero para cargar los administradores
with open('./csv/administradores.csv','r') as csvfile_admins:
	reader = csv.reader(csvfile_admins, delimiter=';')
	for row in reader:
		administradores.append(row[0])
	csvfile_admins.close()
# Lectura del fichero para cargar los mensajes
with open('./csv/mensajes.csv', 'r') as csvfile_mensajes:
	reader = csv.reader(csvfile_mensajes, delimiter=';')
	for row in reader:
		mensajes[row[0]] = row[1]
	csvfile_mensajes.close()

# Lectura del fichero para cargar los id de los grupos
with open('./csv/grupos.csv', 'r') as csvfile_grupos:
	reader = csv.reader(csvfile_grupos, delimiter=';')
	for row in reader:
		id_grupos[row[0]] = int(row[1])
	csvfile_grupos.close()

# Comando /start (Solo funcional en chats privados)
# Tipico comando de bienvenida y esas cosas
@bot.message_handler(commands=['start'],chat_types=['private'])
def send_welcome(message):
	bot.reply_to(message, mensajes['/start'])