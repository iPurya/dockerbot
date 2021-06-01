import docker
import telebot

client = docker.from_env()

@bot.message_handler()
def message_handler(msg):
    pass

bot.infinity_polling(True)