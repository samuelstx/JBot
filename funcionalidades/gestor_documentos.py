import telebot
import csv
import requests
from bot.JBot import bot
from bot.variables_globales import *

# Comando /examenes (Solo funcional en chats privados y grupos)
# Este comando consulta los documentos disponibles para descargar de la pagina de la uex de politecnica
# relacionados con los examenes, es decir, su valor en el primer campo del fichero "lista_documentos.csv"
# debe de ser "Examenes". Este metodo soporta hot reload para no tener que detener el bot.
@bot.message_handler(commands=['examenes'], chat_types=['private'])
def lista_examenes(message):
    enlaces_ficheros = {}
    mensaje = 'EXÁMENES:'
    # Consulta al fichero
    with open('./documentos/links_documentos.csv', 'r') as csvfile_ficheros:
        reader = csv.reader(csvfile_ficheros, delimiter=';')
        for row in reader:
            if row[0] == 'Examenes':
                enlaces_ficheros[row[1]] = {'callback_data': row[1]}
        csvfile_ficheros.close()
    bot.send_message(message.chat.id, mensaje, reply_markup=telebot.util.quick_markup(enlaces_ficheros, row_width=1))

# Atrapa la solicitud de descarga del documento de examenes solicitados y le envia el documento solicitado al char
# solicitado.
@bot.callback_query_handler(func=lambda call: call.message.text == 'EXÁMENES:')
def enviar_fichero_solicitado(call):
    # Consulta al fichero
    with open('./documentos/links_documentos.csv', 'r') as csvfile_ficheros:
        reader = csv.reader(csvfile_ficheros, delimiter=';')
        for row in reader:
            if row[1] == call.data:
                enlace_fichero = row[2]
        csvfile_ficheros.close()
    respuesta = requests.get(enlace_fichero)
    if respuesta.status_code == 200:
        bot.send_document(call.message.chat.id, enlace_fichero)
    else:
        bot.send_message(call.message.chat.id,'No ha sido posible enviar en estos momentos el fichero, intentelo de nuevo más tarde')
