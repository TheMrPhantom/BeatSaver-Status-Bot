import PythonTelegramWraper.bot as bot
from bs4 import BeautifulSoup
import requests
import dryscrape

def start(update, context):
    context.bot.sendMessage(bot.chatID(update),"Register your Beatsaver page with /register <url>")

def register(update, context):
    websiteURL=update.message.text.split()[1]
    bot.modifyUser(bot.chatID(update),websiteURL)
    context.bot.sendMessage(bot.chatID(update),"Website registred")

def check(update, context):
    uID=bot.chatID(update)
    url=bot.user(uID)
    print("response")
    html=None

    html=requests.get('https://beatsaver.com/uploader/5e08e3dd30cd920006c143dd').text
    print("response")
    session = dryscrape.Session()
    print("response")
    sess.set_header('user-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0')
    sess.set_attribute('auto_load_images', False)          
    sess.set_timeout(360)
    print("response")
    session.visit("https://beatsaver.com/uploader/5e08e3dd30cd920006c143dd")
    print("response")
    response = session.body()

    print(response)
    html=BeautifulSoup(html)
    print(html)

    if bot.user(uID) is not None:
        print("hu")
    else:
        context.bot.sendMessage(bot.chatID(update),"Website registred yet")

bot.addBotCommand("start", start)
bot.addBotCommand("register", register)
bot.addBotCommand("check", check)
bot.startBot()