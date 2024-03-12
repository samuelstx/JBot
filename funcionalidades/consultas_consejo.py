import telebot
from bot.JBot import bot
from bot.variables_globales import *

# Comando /alguienEnElConsejo (Solo funcional en chats privados)
# Este comando permite a un usuario preguntar si hay alguien en el consejo y que
# en el grupo del consejo se responda con un si o un no
@bot.message_handler(commands=['alguienEnElConsejo'],chat_types=['private'])
def alguien_en_el_consejo(message):

	mensaje = 'Consultando si hay alguien en el consejo...'

	pregunta_grupo_consejo = {'Si': {'callback_data': f'si a {message.chat.id}'}, 'No': {'callback_data' : f'no a {message.chat.id}'}}

	selector_preguntas = telebot.util.quick_markup(pregunta_grupo_consejo,row_width=2)

	bot.send_message(message.chat.id,mensaje)
	bot.send_message(id_grupos['Grupo test'],f"@{message.from_user.username} ha preguntado si hay alguien en el consejo:"
					 ,reply_markup=selector_preguntas,
					 entities=[telebot.types.MessageEntity(type="mention",offset=0,length=len(message.from_user.username)+1)])


# Captura la respuesta de la pregunta sobre si hay alguien en el consejo, permite responderle al usuario
# en funcion de la respuesta marcada por los miembros del grupo
@bot.callback_query_handler(func=lambda call: (call.message.chat.id == id_grupos['Grupo test']) and
											  (call.message.text == 'Consultando si hay alguien en el consejo...'))
def alguien_en_el_consejo_callback(call): # <- passes a CallbackQuery type object to your function
	if 'si' == call.data[:2]:
		bot.send_message(chat_id=int(call.data.replace('si a ','')), text=f"Si @{call.from_user.username} está en el consejo",
						 entities=[telebot.types.MessageEntity(type="mention",offset=3,length=len(call.from_user.username)+1)])
		bot.delete_message(message_id=call.message.id, chat_id=call.message.chat.id)
	else:
		bot.send_message(chat_id=int(call.data.replace('no a ','')), text="No hay nadie en el ahora mismo, vuelve a intentarlo más tarde")
		bot.delete_message(message_id=call.message.id, chat_id=call.message.chat.id)


