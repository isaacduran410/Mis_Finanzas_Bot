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

app = Flask(__name__)
bot = telebot.TeleBot(TOKEN)

# Conexión a Google Sheets
def conectar_hoja():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('Mis_Finanzas_Bot.json', scope)
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME).sheet1

@app.route('/')
def health_check():
    return "Bot Isaac Operativo 🚀"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Listo para registrar! Envía: Categoria Monto (Ej: Almuerzo 15.50)")

@bot.message_handler(func=lambda message: True)
def registrar_en_hoja(message):
    try:
        sheet = conectar_hoja()
        datos = message.text.split()
        
        if len(datos) < 2:
            bot.reply_to(message, "⚠️ Formato incorrecto. Usa: Categoria Monto")
            return

        categoria = datos
        monto = datos.replace(',', '.')
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # Fila según tus columnas (A: ID, B: Fecha, E: Categoria, J: Monto)
        fila = [message.message_id, fecha, "Telegram", "Gasto", categoria, "", "", "", "", monto, "Completado"]
        
        sheet.append_row(fila)
        bot.reply_to(message, f"✅ Registrado:\n📂 {categoria}\n💰 ${monto}")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

# Hilos para mantener ambos servicios
def run_bot():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    t = Thread(target=run_bot)
    t.start()
    # Render usa la variable de entorno PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
