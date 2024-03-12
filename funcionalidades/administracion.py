from bot.JBot import bot
from bot.variables_globales import *

# Comando /nuevoAdministrador (Solo funcional para usuarios administradores)
# Este comando agrega un usuario a la lista de administradores
@bot.message_handler(commands=['nuevoAdministrador'],chat_types=['private'],
					 func=lambda message: message.from_user.username in administradores)
def add_admin(message):
	doc = open('./csv/administradores.csv', 'a')
	contenido = message.text.replace("/nuevoAdministrador ", "")
	administradores.append(contenido)
	doc.write(contenido+"\n")
	doc.close()
	bot.send_message(message.chat.id,f"El usuario @{contenido} ahora es un administrador")

# Comando /borrarAdministrador (Solo funcional para usuarios administradores)
# Este comando borra un usuario de la lista de administradores
@bot.message_handler(commands=['borrarAdministrador'],chat_types=['private'],
					 func=lambda message: message.from_user.username in administradores)
def remove_admin(message):
	doc = open('./csv/administradores.csv', 'r+')
	contenido = message.text.replace("/borrarAdministrador ", "")
	administradores_fichero = doc.readlines()
	doc.seek(0)
	doc.truncate()

	for administrador in administradores_fichero:
		if not administrador.replace('\n','') == contenido.replace('\n',''):
			doc.write(administrador)

	doc.close()
	administradores.remove(contenido)
	bot.send_message(message.chat.id, f"El usuario @{contenido} ya no es un administrador")

# Comando /listarAdministradores (Solo funcional para usuarios administradores)
# Este comando lista los ususarios con permisos de administrador
@bot.message_handler(commands=['listarAdministradores'],chat_types=['private'],
					 func=lambda message: message.from_user.username in administradores)
def list_admin(message):
	mensaje = "Lista de usuarios con permisos de administrador:\n\n"
	for administrador in administradores:
		mensaje+=f"- {administrador}\n"

	bot.send_message(message.chat.id, mensaje)
