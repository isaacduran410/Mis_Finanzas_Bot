import os
import telebot
import gspread
from flask import Flask
from threading import Thread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- CONFIGURACIÓN ---
TOKEN = '8656809751:AAHvDdK8YxNi25Y7wG4XQ02LSt8WxMMqoLk'
SHEET_NAME = 'Mis_Finanzas_Bot'

# Inicializar Flask y Bot
app = Flask(__name__)
bot = telebot.TeleBot(TOKEN)

# Autenticación Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('Mis_Finanzas_Bot.json', scope)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1

# Ruta para que Render vea que el servicio está vivo
@app.route('/')
def index():
    return "Bot de Finanzas Operativo 🚀"

@bot.message_handler(func=lambda message: True)
def registrar_gasto(message):
    try:
        # Formato esperado: "Comida 15.50"
        partes = message.text.split()
        if len(partes) < 2:
            bot.reply_to(message, "⚠️ Envía: Categoria Monto (Ej: Cena 25.00)")
            return

        categoria = partes
        monto = partes.replace(',', '.') # Corregir comas por puntos
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # Insertar en la hoja según tus columnas
        fila = [message.message_id, fecha, "Telegram", "Gasto", categoria, "", "", "", "", monto, "Completado"]
        sheet.append_row(fila)
        
        bot.reply_to(message, f"✅ Guardado en Google Sheets:\n📂 {categoria}\n💰 ${monto}")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

# Función para correr el bot
def run_bot():
    bot.polling(none_stop=True)

# Función para correr Flask
def run_flask():
    # Render asigna un puerto automáticamente en la variable PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    # Iniciamos el bot en un hilo secundario
    t = Thread(target=run_bot)
    t.start()
    # Iniciamos Flask en el hilo principal
    run_flask()
