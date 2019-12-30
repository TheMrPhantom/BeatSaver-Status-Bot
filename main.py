import PythonTelegramWraper.bot as bot
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def start(update, context):
    context.bot.sendMessage(bot.chatID(update),"Register your Beatsaver page with /register <url>")

def register(update, context):
    websiteURL=update.message.text.split()[1]
    bot.modifyUser(bot.chatID(update),websiteURL)
    context.bot.sendMessage(bot.chatID(update),"Website registred")

def check(update, context):
    uID=bot.chatID(update)
    url=bot.user(uID)
    html=None

    options = Options()
    options.headless = True

    print("a")
    driver = webdriver.Firefox(options=options)
    print("b")
    driver.get("https://beatsaver.com/uploader/5e08e3dd30cd920006c143dd")
    print("c")
    
    html=driver.page_source

    print(html)
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