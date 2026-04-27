import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# CONFIGURACIÓN
TOKEN = '8656809751:AAHvDdK8YxNi25Y7wG4XQ02LSt8WxMMqoLk'
SHEET_NAME = 'Mis_Finanzas_Bot'

# Autenticación con Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# Aquí usarás el contenido del JSON que me pasaste
creds = ServiceAccountCredentials.from_json_keyfile_name('Mis_Finanzas_Bot.json', scope)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def registrar_gasto(message):
    try:
        # Ejemplo simple: "Comida 15.50"
        datos = message.text.split()
        categoria = datos
        monto = datos
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # Preparamos la fila (ajustada a tus columnas A, B, C, D...)
        # ID_Tx, Fecha_Hora, Entidad, Movimiento, Categoria, Monto_Neto...
        fila = [message.message_id, fecha, "Telegram", "Gasto", categoria, "", "", "", "", monto, "Completado"]
        
        sheet.append_row(fila)
        bot.reply_to(message, f"✅ Registrado: {categoria} por {monto}")
    except Exception as e:
        bot.reply_to(message, "❌ Error. Envía: Categoría Monto (Ej: Cafe 3.50)")

bot.polling()
