import PythonTelegramWraper.bot as bot
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


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
        timeout = 5
        options = Options()
        options.headless = True

        context.bot.sendMessage(bot.chatID(update),"Starting request on beatsaver.com, please wait...")

        driver = webdriver.Firefox(options=options)

        driver.get("https://beatsaver.com/uploader/5e08e3dd30cd920006c143dd")
        #driver.get(url)
        
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'outer'))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException:
            print ("Timed out waiting for page to load")

        print("Wait for images")
        time.sleep(8)
        print("Done Waiting")

        html=driver.page_source

        
        html=BeautifulSoup(html)
        songTitles=[]
        songImages=[]

        #Processing titels
        songTitlesRAW=html.findAll('div',{'class':'details'})
        for s in songTitlesRAW:
            inner=s.find('h1',{'class':'has-text-weight-light'})
            inner=inner.find('a').decode_contents()
            songTitles.append(inner)

        print("Done Titles")

        #Processing images
        songImagesRAW=html.findAll('div',{'class':'cover'})
        for c in songImagesRAW:
            inner=c.find('img')
            inner=inner['src']
            inner="https://www.beatsaver.com"+inner
            songImages.append(inner)

        print("Done Images")

        #Processing infos
        songInfosRAW=html.findAll('div',{'class':'stats'})
        print(songInfosRAW)
        for si in songInfosRAW:
            inner=si.findAll('li',{'class':'mono'})
            print(inner)
            #inner=inner['src']
            #inner="https://www.beatsaver.com"+inner
            #songImages.append(inner)




        print(songTitles)
    else:
        context.bot.sendMessage(bot.chatID(update),"Website registred yet")

bot.addBotCommand("start", start)
bot.addBotCommand("register", register)
bot.addBotCommand("check", check)
bot.startBot()