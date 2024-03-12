import csv
import datetime

import telebot
from bot.JBot import bot
from bot.variables_globales import *

# Comando /nevera (Solo funcional en chats privados y grupales)
# Este comando permite a un usuario registrar el consumo de productos de la nevera
@bot.message_handler(commands=['nevera'],chat_types=['private','group'])
def coger_nevera(message):

    mensaje = 'Selecciona el producto:'
    lista_productos = {}

    with open('./csv/productos_nevera.csv','r') as csvfile_productos:
        reader = csv.reader(csvfile_productos,delimiter=';')
        for row in reader:
            lista_productos[row[0]] = {'callback_data':f'{message.from_user.username};{row[0]};{row[1]}'}

    selector_productos = telebot.util.quick_markup(lista_productos,row_width=2)

    mensaje_enviado = bot.send_message(message.chat.id,mensaje,
                     reply_markup=selector_productos)

    #bot.delete_message(mensaje_enviado.chat.id,mensaje_enviado.message_id)

# Captura la respuesta de la pregunta sobre el producto seleccionado de la nevera y anota en tu cuenta
# el producto, si no tenias cuenta la crea
@bot.callback_query_handler(func=lambda call: call.message.text == 'Selecciona el producto:')
def registrar_deuda_nevera(call): # <- passes a CallbackQuery type object to your function
    usuario = call.data.split(';')[0]
    producto = call.data.split(';')[1]
    precio = float(call.data.split(';')[2])
    usuarios_en_cuentas = []
    lineas = []
    with open('./csv/cuentas_nevera.csv', 'r') as csvfile_cuentas:
        reader = csvfile_cuentas.readlines()
        csvfile_cuentas.close()

    with open('./csv/cuentas_nevera.csv', 'w') as csvfile_cuentas:
        for row_without_split in reader:
            row = row_without_split.replace('\n','').split(';')
            usuarios_en_cuentas.append(row[0])
            if row[0] == usuario:
                cuenta = float(row[1])+precio
                lineas.append(f"{usuario};{cuenta}\n")
            else:
                lineas.append(f"{row[0]};{row[1]}\n")
        if usuario not in usuarios_en_cuentas:
            lineas.append(f"{usuario};{precio}\n")
        csvfile_cuentas.writelines(lineas)
        csvfile_cuentas.close()
    with open('./csv/historial_nevera.csv','a') as historial_nevera:
        historial_nevera.write(f"{usuario};{producto};{precio};{datetime.date.today().strftime('%d/%m/%Y')}\n")
        historial_nevera.close()

    bot.send_message(call.message.chat.id,f"Se ha registrado que has cogido un producto nevera: {producto}")

# Comando /cuenta (Solo funcional en chats privados y grupales)
# Este comando permite saber a un usuario cuanto debe
@bot.message_handler(commands=['cuenta'],chat_types=['private','group'])
def obtener_deuda_nevera(message):
    usuario = message.from_user.username
    deuda = 0
    with open('./csv/cuentas_nevera.csv','r') as csvfile_cuentas:
        reader = csv.reader(csvfile_cuentas,delimiter=';')
        for row in reader:
            if row[0] == usuario:
                deuda = float(row[1])
        csvfile_cuentas.close()
    bot.send_message(message.chat.id,f"Tu deuda es de: {deuda}€")

# Comando /deudaPagada (Solo funcional en chats privados de administradores)
# Sirve para poner a 0 la deuda de un usuario
@bot.message_handler(commands=['deudaPagada'],chat_types=['private','group'],
                     func=lambda message: message.from_user.username in administradores)
def saldar_deuda(message):
    usuarios = {}
    mensaje = "Selecciona un usuario para eliminar su deuda:"
    with open('./csv/cuentas_nevera.csv','r') as csvfile_cuentas:
        reader = csv.reader(csvfile_cuentas,delimiter=';')
        for row in reader:
            usuarios[row[0]] = {'callback_data': f"{row[0]};{row[1]}"}
        csvfile_cuentas.close()
    seleccion_usuario = telebot.util.quick_markup(usuarios)
    bot.send_message(message.chat.id,mensaje,reply_markup=seleccion_usuario)

# Captura la respuesta de la pregunta sobre el producto seleccionado de la nevera y anota en tu cuenta
# el producto, si no tenias cuenta la crea
@bot.callback_query_handler(func=lambda call: (call.message.text == 'Selecciona un usuario para eliminar su deuda:'))
def eliminar_deuda_nevera(call): # <- passes a CallbackQuery type object to your function
    usuario = call.data.split(';')[0]
    deuda = call.data.split(';')[1]
    with open('./csv/cuentas_nevera.csv','r') as csvfile_cuentas:
        reader = csvfile_cuentas.readlines()
        fichero = []
        csvfile_cuentas.close()

    with open('./csv/cuentas_nevera.csv','w') as csvfile_cuentas:
        for row_without_split in reader:
            data = row_without_split.replace('\n','')
            row = data.split(';')
            if row[0] == usuario:
                fichero.append(f"{usuario};0\n")
                bot.send_message(call.message.chat.id,
                                 f"Se ha saldado la deuda de @{usuario} de un total de {deuda}€",
                                 entities=[
                                     telebot.types.MessageEntity(type="mention", offset=28, length=len(usuario) + 1)])
            else:
                fichero.append(data+'\n')
        csvfile_cuentas.writelines(fichero)
        csvfile_cuentas.close()
