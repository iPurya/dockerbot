import re
import time
import config
import docker
import telebot
from telebot.types import InlineKeyboardButton as btn
from telebot.types import InlineKeyboardMarkup as newkb

client = docker.from_env()
bot = telebot.TeleBot(config.TOKEN)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler_function(call):
    data = call.data
    chat_id = call.message.chat.id
    msg_id  = call.message.message_id
    if data == "restart_all":
        bot.edit_message_text("Please wait...", chat_id, msg_id, reply_markup=None)
        for container in client.containers.list():
            container.restart()
            bot.edit_message_text(f"Container <code>{container.name}</code> restarted!", chat_id, msg_id, reply_markup=None, parse_mode="HTML")
            time.sleep(0.5)

        bot.edit_message_text("✅ All containers restarted successfully!", chat_id, msg_id, reply_markup=None)
    elif match := re.match(r"in:(.*)", data):
        container_id = match.group(1)
        #TODO: Show all info about container from `container.attrs`
        #TODO: add buttons to start,stop,restart,... for container
        
@bot.message_handler()
def message_handler(msg):
    #if not msg.chat.id == config.MANAGE_GP: return
    text = str(msg.text)
    if re.match(r"/[Pp]s",text):
        txt = "Container lists :\n\n"
        i = 0
        kb = newkb()
        kb.add(btn("🔄 Restart all 🔄",callback_data=f"restart_all"))
        for container in client.containers.list():
            i+=1
            txt += f"<b>{i}.</b> <code>{container.name}</code> — {container.status}\n" #TODO: add more detail about container
            #kb.add(btn(container.name,callback_data=f"in:{container.short_id}")) #TODO: will be added later
        txt +="\nUse buttons to manage containers:"
        
        bot.send_message(msg.chat.id, txt, reply_markup=kb, parse_mode="HTML")

bot.infinity_polling(True)
