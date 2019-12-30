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
    
    html=None

    if bot.user(uID) is not None:
        url=bot.user(uID)
        options = Options()
        options.headless = True

        context.bot.sendMessage(bot.chatID(update),"Starting request on beatsaver.com, please wait...")

        driver = webdriver.Firefox(options=options)

        driver.get("https://beatsaver.com/uploader/5e08e3dd30cd920006c143dd")
        #driver.get(url)
        
        html=driver.page_source

        
        html=BeautifulSoup(html)
    
        songTitle=html.findAll('div',{'class':'outer'})
    
        print(songTitle)
    else:
        context.bot.sendMessage(bot.chatID(update),"Website registred yet")

bot.addBotCommand("start", start)
bot.addBotCommand("register", register)
bot.addBotCommand("check", check)
bot.startBot()