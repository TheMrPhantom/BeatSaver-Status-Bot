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
    context.bot.sendMessage(bot.chatID(update), "Register your Beatsaver page with /register <url>")


def register(update, context):
    websiteURL = update.message.text.split()[1]
    bot.modifyUser(bot.chatID(update), websiteURL)
    context.bot.sendMessage(bot.chatID(update), "Website registred")

def searchURL(bot, chatID, searchURL, sendMessage="Starting request on beatsaver.com, please wait...",maxResults=10):
    timeout = 60
    options = Options()
    options.headless = True

    bot.sendMessage(
        chatID, sendMessage)

    driver = webdriver.Firefox(options=options)
    print(searchURL)
    driver.get(searchURL)

    try:
        element_present = EC.presence_of_element_located(
            (By.CLASS_NAME, 'outer'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
        bot.sendMessage(chatID, "Timed out waiting for page to load")

    print("Wait for images")
    time.sleep(8+maxResults)
    print("Done Waiting")

    html = driver.page_source

    driver.close()
    driver.quit()

    html = BeautifulSoup(html)

    songTitles = []
    songImages = []
    songInfos = []

    # Processing titels
    songTitlesRAW = html.findAll('div', {'class': 'details'})
    maxCounter=0
    for s in songTitlesRAW:
        maxCounter+=1
        if maxCounter>=maxResults:
            break
        inner = s.find('h1', {'class': 'has-text-weight-light'})
        inner = inner.find('a').decode_contents()
        songTitles.append(inner)

    print("Done Titles")

    # Processing images
    songImagesRAW = html.findAll('div', {'class': 'cover'})
    maxCounter=0
    for c in songImagesRAW:
        maxCounter+=1
        if maxCounter>=maxResults:
            break
        inner = c.find('img')
        inner = inner['src']
        inner = "https://www.beatsaver.com"+inner
        songImages.append(inner)

    print("Done Images")

    # Processing infos
    songInfosRAW = html.findAll('div', {'class': 'stats'})

    counter = 0
    maxCounter=0
    for si in songInfosRAW:
        maxCounter+=1
        if maxCounter>=maxResults:
            break
        songInfos.append([])
        inner = si.findAll('li', {'class': 'mono'})
        for info in inner:
            songInfos[counter].append(info.decode_contents())

        counter += 1

    print("Done Infos")

    songCount = len(songTitles)
    maxCounter=0
    for i in range(0, songCount):
        maxCounter+=1
        if maxCounter>=maxResults:
            break
        infos = songInfos[i]
        caption = "*"+songTitles[i]+"*\n"
        for info in infos:
            caption += info+"\n"
        bot.sendPhoto(chatID, songImages[i], captionText=caption)


def search(update, context):
    searchKey=str(update.message.text.split()[1])
    searchURL(context.bot,bot.chatID(update),"https://beatsaver.com/search?q="+searchKey,maxResults=5,sendMessage=("Searching for '"+searchKey+"'"),)

def check(update, context):
    uID = bot.chatID(update)

    if bot.user(uID) is not None:
        url = bot.user(uID)
        searchURL(context.bot, uID, url)
    else:
        context.bot.sendMessage(bot.chatID(update), "Website registred yet")

bot.addBotCommand("start", start)
bot.addBotCommand("register", register)
bot.addBotCommand("check", check)
bot.addBotCommand("search", search)
bot.startBot()
