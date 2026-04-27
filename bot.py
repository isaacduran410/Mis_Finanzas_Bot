import os
import telebot
import gspread
from flask import Flask
from threading import Thread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- CONFIGURACIÓN ---
# Tu Token de Telegram
TOKEN = '8656809751:AAHvDdK8YxNi25Y7wG4XQ02LSt8WxMMqoLk'
# El nombre exacto de tu Google Sheet
SHEET_NAME = 'Mis_Finanzas_Bot'

# Inicializar Flask y el Bot
app = Flask(__name__)
bot = telebot.TeleBot(TOKEN)

# Configuración de Google Sheets
def conectar_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # Usamos el nombre del archivo JSON que ya tienes
    creds = ServiceAccountCredentials.from_json_keyfile_name('Mis_Finanzas_Bot.json', scope)
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME).sheet1

# Ruta para que Render mantenga el bot vivo
@app.route('/')
def index():
    return "Bot de Finanzas Isaac: ¡En línea y trabajando! 🚀"

# Comando de bienvenida
@bot.message_handler(commands=['start', 'help'])
def enviar_bienvenida(message):
    bot.reply_to(message, "¡Hola Isaac! Envíame tus gastos así: \n\n`Comida 25.50` \n(Categoría espacio Monto)")

# Manejador de mensajes para registrar datos
@bot.message_handler(func=lambda message: True)
def registrar_transaccion(message):
    try:
        sheet = conectar_google_sheets()
        partes = message.text.split()
        
        if len(partes) < 2:
            bot.reply_to(message, "⚠️ Error. Usa el formato: Categoria Monto")
            return

        categoria = partes
        # Cambiamos coma por punto por si acaso
        monto = partes.replace(',', '.')
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # Estructura de tu fila (A: ID_Tx, B: Fecha, C: Entidad, J: Monto_Neto)
        # Ajustamos los espacios vacíos para que el monto caiga en la columna J (columna 10)
        fila = [message.message_id, fecha, "Telegram", "Gasto", categoria, "", "", "", "", monto, "Completado"]
        
        sheet.append_row(fila)
        bot.reply_to(message, f"✅ ¡Listo!\n📅 {fecha}\n📂 {categoria}\n💰 ${monto}")
        
    except Exception as e:
        bot.reply_to(message, f"❌ Error al conectar con Sheets: {str(e)}")

# Hilos para ejecutar Flask y el Bot al mismo tiempo
def run_bot():
    bot.polling(none_stop=True)

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    t = Thread(target=run_bot)
    t.start()
    run_flask()
