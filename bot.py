import os
import telebot
from comfy_sdk import Comfy

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም! የ ComfyUI AI ቪዲዮ/ምስል ጄነሬተር ቦት ነኝ። ለማመንጨት /generate ብለህ ጻፍ።")

@bot.message_handler(commands=['generate'])
def generate_image(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "⏳ ፋይሉ በማመንጨት ላይ ነው፣ እባክዎ ትንሽ ይጠብቁ...")
    
    try:
        client = Comfy(api_key=os.environ.get("COMFY_API_KEY"))
        wf = client.workflows.from_file("workflow_api.json")
        job = client.run(wf)
        
        output_filename = "output.png"
        job.outputs[0].to_file(output_filename)
        
        with open(output_filename, 'rb') as photo:
            bot.send_photo(chat_id, photo, caption="✨ በ ComfyUI የተሰራው ውጤትዎ!")
            
    except Exception as e:
        bot.send_message(chat_id, f"❌ ስህተት ተፈጥሯል: {str(e)}")

if __name__ == "__main__":
    bot.infinity_polling()
