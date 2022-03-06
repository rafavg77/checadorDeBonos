import os
import logging
from telebot import types, telebot
from configparser import ConfigParser
from utils.consultarBonos import checadorBonos

# Cargar archivo de configuración
thisfolder = os.path.dirname(os.path.abspath(__file__))
initfile = os.path.join(thisfolder, 'utils/config/config.ini')
config = ConfigParser()
config.read(initfile)

# Configuracion de loggeo
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurar parametros
BOT_TOKEN = config.get('params','telegram_token')
BOT_CHAT = config.get('params','telegram_chat_id')
USARUIOS_PERMITIDOS = config.get('base','permited')
USERNAME = config.get('bonos',"bond_user")
PASSWORD = config.get('bonos',"bond_pass")
USERNAME2 = config.get('bonos',"bond_user2")
PASSWORD2 = config.get('bonos',"bond_pass2")

# Configuración de Constantes
saldoBonos = '💳 Consultar saldo de Bonos 💳'
saldoLuz = '💡 Consultar Recibo de Luz 💡'
saldoAgua = '🚿 Consultar Recibo de Agua 🚿'
saldoGas = '🔥 Consultar Recivo de Gas 🔥'
bonos1 = '🎸 Bonos de usuario 1 🎸'
bonos2 = '🐕 Bonos de usuario 2 🐕'
regresar = '⬅️ Regresar ⬅️'

# Inicializar funcionamiento del Bot
bot = telebot.TeleBot(BOT_TOKEN)

def esPermitido(message):
    if str(message.chat.id) in USARUIOS_PERMITIDOS:
        permitido = True
        logging.info("Usuario permitido {}".format(message.chat.id))
    else:
        permitido = False
        id = str(message.chat.id)
        if message.chat.type == 'group':
            user = message.chat.title
        else:
            user = message.chat.username
        logger.warning("Warning user without permission: " + id + " "+ user)
        bot.send_message(message.chat.id, "No tienes privilegios suficientes")
        bot.send_message(BOT_CHAT, "REPORTE usuario no permitido id: " + id + " nombre: "+ user)
    return permitido


# Condifuración del teclado
def keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=5)
    itembtna = types.KeyboardButton(saldoBonos)
    itembtnv = types.KeyboardButton(saldoLuz)
    itembtnc = types.KeyboardButton(saldoAgua)
    itembtnd = types.KeyboardButton(saldoGas)
    markup.row(itembtna)
    markup.row(itembtnv)
    markup.row(itembtnc)
    markup.row(itembtnd)
    return markup

def keyboard_bonos():
    markup = types.ReplyKeyboardMarkup(row_width=3)
    itemUno = types.KeyboardButton(bonos1)
    itemDos = types.KeyboardButton(bonos2)
    itemTres = types.KeyboardButton(regresar)
    markup.row(itemUno)
    markup.row(itemDos)
    markup.row(itemTres)
    return markup


# Leer comandos de '/start' y '/help y crear teclado' 
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if esPermitido(message):
        bot.send_message(message.chat.id, "Puedes utilizar el teclado",reply_markup=keyboard())

@bot.message_handler(commands=['consultarBonos'])
def consultarBonos(message):
    if esPermitido(message):
        bot.send_message(message.chat.id, "Selecciona el usuario",reply_markup=keyboard_bonos())

# Funcion para consultar saldo de bonos
@bot.message_handler(commands=['consultarBonosUsuario'])
def consultarBonosUsuario(message,usuario):
    if esPermitido(message):
        status = "Consultando bonos de {} ...".format(usuario)
        bot.send_message(message.chat.id, status)
        bonos = checadorBonos()

        if usuario == "usuario1":
            user = USERNAME
            password = PASSWORD
        elif usuario == "usuario2":
            user = USERNAME2
            password = PASSWORD2

        try:
            saldo = bonos.consultarSaldoBonos(user,password)
        except:
            saldo = "No se pudo obtener el saldo"
            pass

        bot.send_message(message.chat.id, saldo)

# Funcion para consultar saldo de luz
@bot.message_handler(commands=['consultarLuz'])
def consultarLuz(message):
    if esPermitido(message):
        status = "Funcionalidad no implementada actualmente"
        bot.send_message(message.chat.id, status)

# Funcion para consultar saldo de Agua
@bot.message_handler(commands=['consultarAgua'])
def consultarAgua(message):
    if esPermitido(message):
        status = "Funcionalidad no implementada actualmente"
        bot.send_message(message.chat.id, status)

# Funcion para consultar saldo de Gas
@bot.message_handler(commands=['consultarGas'])
def consultarGas(message):
    if esPermitido(message):
        status = "Funcionalidad no implementada actualmente"
        bot.send_message(message.chat.id, status)

# Funcion para detectar entradas de teclado de telegram
@bot.message_handler(func=lambda message:True)
def all_messages(message):
    if esPermitido(message):
        if message.text == saldoBonos:
            consultarBonos(message)
        elif message.text ==  saldoLuz:
            consultarLuz(message)
        elif message.text == saldoAgua:
            consultarAgua(message)
        elif message.text == saldoGas:
            consultarGas(message)
        elif message.text == bonos1:
            consultarBonosUsuario(message,"usuario1")
        elif message.text == bonos2:
            consultarBonosUsuario(message, "usuario2")
        elif message.text == regresar:
            bot.send_message(message.chat.id, "Regresando a teclado Inicial",reply_markup=keyboard())


# Ejecución Inicial del Bot
logger.info("🐧Bot is Running 🐧")
bot.send_message(BOT_CHAT, "🐧Bot is Running 🐧")
bot.infinity_polling()