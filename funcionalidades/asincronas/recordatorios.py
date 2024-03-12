import csv
import datetime
import telebot
import threading
import time

from bot.JBot import bot
from bot.variables_globales import *


# Comando /recordatorio (Solo funcional para usuarios administradores)
# Este comando agrega un recordatorio
@bot.message_handler(commands=['recordatorio'], chat_types=['private', 'group'],
                     func=lambda message: message.from_user.username in administradores)
def add_recordatorio(message):
    doc = open('./csv/recordatorios.csv', 'a')
    contenido = message.text.replace("/recordatorio ", "")
    fecha = contenido.split(' ')[0]
    hora = contenido.split(' ')[1]
    recordatorio = contenido.replace(fecha + ' ', '').replace(hora + ' ', '')
    autor = message.from_user.first_name;
    doc.write(f"{autor};{fecha};{hora};{recordatorio}\n")
    doc.close()
    bot.reply_to(message, "Recordatorio creado!")


# Comando /recordatorio (Solo funcional para usuarios administradores)
# Este comando agrega un recordatorio
@bot.message_handler(commands=['listarRecordatorios'], chat_types=['private', 'group'])
def listar_recordatorios(message):
    recordatorios = {}
    fechas_visitadas = []
    # Lectura del fichero para cargar los recordatorios
    with open('./csv/recordatorios.csv', 'r') as csvfile_recordatorios:
        reader = csv.reader(csvfile_recordatorios, delimiter=';')
        for row in reader:
            fecha_recordatorios = row[1]
            if fecha_recordatorios not in fechas_visitadas:
                fechas_visitadas.append(fecha_recordatorios)
                recordatorios[fecha_recordatorios] = {'callback_data': f"{fecha_recordatorios}"}
        csvfile_recordatorios.close()
        print(recordatorios)
    bot.send_message(message.chat.id, "Listado de recordatorios:",
                     reply_markup=telebot.util.quick_markup(recordatorios, row_width=1))


# Captura la respuesta de la pregunta sobre si hay alguien en el consejo, permite responderle al usuario
# en funcion de la respuesta marcada por los miembros del grupo
@bot.callback_query_handler(func=lambda call: call.message.text == "Listado de recordatorios:")
def alguien_en_el_consejo_callback(call):  # <- passes a CallbackQuery type object to your function
    with open('./csv/recordatorios.csv', 'r') as csvfile_recordatorios:
        reader = csv.reader(csvfile_recordatorios, delimiter=';')
        for row_fecha in reader:
            fecha_recordatorios = call.data
            recordatorios_misma_fecha = f"Recordatorios para {fecha_recordatorios}:\n\n"
            for row_misma_fecha in reader:
                if fecha_recordatorios == row_misma_fecha[1]:
                    recordatorios_misma_fecha += f" - De {row_misma_fecha[0]} a las {row_misma_fecha[2]}: {row_misma_fecha[3]}\n\n"
        csvfile_recordatorios.close()
    bot.send_message(call.message.chat.id, recordatorios_misma_fecha)


def enviar_recordatorios():
    recordatorios = {}
    contador = 0
    # Lectura del fichero para cargar los recordatorios
    with open('./csv/recordatorios.csv', 'r') as csvfile_recordatorios:
        reader = csv.reader(csvfile_recordatorios, delimiter=';')
        for row in reader:
            recordatorios[contador] = {
                'fecha': row[1],
                'hora': row[2],
                'recordatorio': row[3],
                'autor': row[0]
            }
            contador = contador + 1
        csvfile_recordatorios.close()

    for i in range(0,len(recordatorios)):
        if f"{recordatorios[i]['fecha']}" == datetime.date.today().strftime('%d/%m/%Y'):
            bot.send_message(id_grupos['Grupo test'], f"{recordatorios[i]['autor']} te recuerda que hoy a las " +
                             f"{recordatorios[i]['hora']} tienes: {recordatorios[i]['recordatorio']}")

def notificacion_diaria():
    while True:
        enviar_recordatorios()
        time.sleep(60*60*24) #60 segundos x 60 minutos x 24 horas

# Iniciar la ejecución en segundo plano.
t = threading.Thread(target=notificacion_diaria)
t.start()