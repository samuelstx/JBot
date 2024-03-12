from bot.JBot import bot
from bot.variables_globales import *
from bot.funciones_globales import *

# Comando /sugerencia (Solo funcional en chats privados y grupos)
# Este comando recoge la informacion aportada por el usuario junto a la fecha y su nombre
# y la almacena en un fichero llamado "sugerencias.csv"
@bot.message_handler(commands=['sugerencia'],chat_types=['private','group'])
def send_sugerencia(message):
	sugerencias = open('./csv/sugerencias.csv', 'a')
	contenido = message.text.replace("/sugerencia ","")
	autor = message.from_user.first_name
	fecha = fecha_y_hora(message)
	sugerencias.write(f"{autor};{fecha};{contenido}\n")
	sugerencias.flush()
	bot.reply_to(message, mensajes['/sugerencia'])
	sugerencias.close()
	#bot.delete_message(message.chat.id, message.id)

# Comando /sugerencia (Solo funcional para usuarios administradores)
# Este comando envia el fichero que recoge las sugerencias llamado "sugerencias.csv"
@bot.message_handler(commands=['obtenerSugerencias'],chat_types=['private'],
					 func=lambda message: message.from_user.username in administradores)
def get_sugerencias(message):
	doc = open('./csv/sugerencias.csv', 'rb')
	bot.send_document(message.chat.id, doc)
	doc.close()

