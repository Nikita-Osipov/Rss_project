from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
import random
import json
import requests
from bs4 import BeautifulSoup as bs
from nltk.stem.snowball import SnowballStemmer
import re

modeOut = 0
modeUrl = 0

ps = SnowballStemmer('russian')
'''
Примермы rss лент, которые пользователь может парсить.
'''
url = ['https://news.yandex.ru/sport.rss',
       'https://news.yandex.ru/cyber_sport.rss',
       'https://news.yandex.ru/politics.rss',
       'https://news.yandex.ru/business.rss',
       'https://news.yandex.ru/computers.rss',      
       'https://news.yandex.ru/movies.rss',
       'https://news.yandex.ru/science.rss']

'''
Функция получает ключевые слова, находит их "обычную" форму и возвращает.
'''
def key_words(wrds):
    lst = []
    wrds = wrds.replace(',','')
    wrds = wrds.split()
    for w in wrds:
        lst.append(ps.stem(w))
    return lst
'''
Функция передеывает слова заголовка в "обычную" форму для более точного поиска слов в нем.
'''
def title_words(txt):
    lst = []
    txt = txt.replace(',','')
    wrds = txt.split()
    for w in wrds:
        lst.append(ps.stem(w))
    wrds = ''.join(lst)
    return wrds
'''
Фунция ищет ключевые слова в заголовке, если они там есть, то новость отбирается дальше.
'''
def wordInStr(wrds,dflt_ttl):
    for i in wrds:
        try:
            result = re.search(i,dflt_ttl)
            if result != None:
                return True
                Break()
        except:
            continue
    return False
'''
Поиск и отбор новостей.
'''
def rsc(url,kWrds):
    news = []
    keyW = key_words(kWrds)
    req = requests.get(url)
    soup = bs(req.text,'lxml')
    divs = soup.findAll('item')
    for div in divs:
        ttl = div.find('title')
        txt = div.find('description')
        dflt_ttl = title_words(ttl.text)
        dflt_dsc = title_words(txt.text)
        if wordInStr(keyW,dflt_ttl) == True or wordInStr(keyW,dflt_dsc) == True:
            lnk = div.find('guid')
            news.append(ttl.text+'\n\n'+txt.text+'\n\n'+lnk.text+'\n\n')
    return news

token = "Тут должен быть token вашего сообщества в vk."#Warning

vk_session = vk_api.VkApi(token=token)

longpoll = VkLongPoll(vk_session)
session_api = vk_session.get_api()

def get_button(label, color, payload=""):
    return{
        "action":{
            "type":"text",
            "payload":json.dumps(payload),
            "label":label
            },
        "color":color
        }

'''
Основная клавиатура.
'''
keyboard = {
    "one_time":True,
    "buttons":[
    [get_button(label="Спорт",color="primary"),get_button(label="Кибер спорт",color="primary")],
    [get_button(label="Политика",color="primary"),get_button(label="Экономика",color="primary")],
    [get_button(label="Технологии",color="primary"),get_button(label="Кино",color="primary")],
    [get_button(label="Наука",color="primary"),get_button(label="Ввести RSS ленту",color="primary")]
        ]
    }

keyboard = json.dumps(keyboard,ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))
'''
Побочная клавиатура.
'''
keyboardBack = {
    "one_time":True,
    "buttons":[[get_button(label="Вернуться к категориям",color="negative")]]
    }

keyboardBack = json.dumps(keyboardBack,ensure_ascii=False).encode('utf-8')
keyboardBack = str(keyboardBack.decode('utf-8'))


hlp =  "\n\nСписок команд:\nНачать\nСпорт\nКибер Спорт\nПолитика\nЭкономика\nТехнологии\nКино\nНаука\nВвести RSS ленту\nВернуться к категориям"
info = 'Вы можете выбрать заготовленную ленту, а так же ввести ту, которую хотите изучить.\nПримеры:\nhttps://www.sostav.ru/rss\nhttps://lenta.ru/rss\nБудьте внимательны, я изучаю не все RSS ленты.\n\n'
helloMes = 'Здравствуй!\n Если вы в первый раз пользуетесь мной, то изучите список команд!\nЯ помогу искать те новости, которые вам будут интересны!\n'+str(info)+'\nПожалуйста, используйте русский язык для ввода ключевых слов.'+str(hlp)+'\n\nВыберите тематику!',

'''
Бесконечный цикл, который работает от входящих сообщений.
'''
while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if modeOut == 0:
                if event.text.lower() == 'начать':
                    session_api.messages.send(
                            user_id = event.user_id,
                            message = helloMes,
                            keyboard = keyboard,
                            random_id = random.randint(0, 10000000))
                elif event.text.lower() == 'спорт':
                    session_api.messages.send(
                            user_id = event.user_id,
                            message = 'Введите ключевые слова, которые вас интересуют.',
                            keyboard = keyboardBack,
                            random_id = random.randint(0, 10000000))
                    modeOut = 1
                    modeUrl = 0
                elif event.text.lower() == 'кибер спорт':
                    session_api.messages.send(
                            user_id = event.user_id,
                            message = 'Введите ключевые слова, которые вас интересуют.',
                            keyboard = keyboardBack,
                            random_id = random.randint(0, 10000000))
                    modeOut = 1
                    modeUrl = 1
                elif event.text.lower() == 'политика':
                    session_api.messages.send(
                            user_id = event.user_id,
                            message = 'Введите ключевые слова, которые вас интересуют.',
                            keyboard = keyboardBack,
                            random_id = random.randint(0, 10000000))
                    modeOut = 1
                    modeUrl = 2
                elif event.text.lower() == 'экономика':
                    session_api.messages.send(
                            user_id = event.user_id,
                            message = 'Введите ключевые слова, которые вас интересуют.',
                            keyboard = keyboardBack,
                            random_id = random.randint(0, 10000000))
                    modeOut = 1
                    modeUrl = 3
                elif event.text.lower() == 'технологии':
                    session_api.messages.send(
                            user_id = event.user_id,
                            message = 'Введите ключевые слова, которые вас интересуют.',
                            keyboard = keyboardBack,
                            random_id = random.randint(0, 10000000))
                    modeOut = 1
                    modeUrl = 4
                elif event.text.lower() == 'кино':
                    session_api.messages.send(
                            user_id = event.user_id,
                            message = 'Введите ключевые слова, которые вас интересуют.',
                            keyboard = keyboardBack,
                            random_id = random.randint(0, 10000000))
                    modeOut = 1
                    modeUrl = 5
                elif event.text.lower() == 'наука':
                    session_api.messages.send(
                            user_id = event.user_id,
                            message = 'Введите ключевые слова, которые вас интересуют.',
                            keyboard = keyboardBack,
                            random_id = random.randint(0, 10000000))
                    modeOut = 1
                    modeUrl = 6
                elif event.text.lower() == 'ввести rss ленту':
                    session_api.messages.send(
                            user_id = event.user_id,
                            message = 'Введите RSS ленту',
                            keyboard = keyboardBack,
                            random_id = random.randint(0, 10000000))
                    modeOut = 2
                elif event.text.lower() == 'вернуться к категориям':
                    session_api.messages.send(
                            user_id = event.user_id,
                            message = 'Выберите направленность новостного сайта!',
                            keyboard = keyboard,
                            random_id = random.randint(0, 10000000))
                else:
                    session_api.messages.send(
                            user_id = event.user_id,
                            message = helloMes,
                            keyboard = keyboard,
                            random_id = random.randint(0, 10000000))                    

            elif modeOut == 1:
                if len(event.text.lower()) == 0 or event.text.lower() == 'вернуться к категориям':
                    modeOut = 0
                    session_api.messages.send(
                            user_id = event.user_id,
                            message = 'Неверные данные. Попытайтесь снова!',
                            keyboard = keyboard,
                            random_id = random.randint(0, 10000000))
                else:
                    modeOut = 0
                    out = rsc(url[modeUrl],event.text.lower())
                    for i in out:
                        session_api.messages.send(
                                user_id = event.user_id,
                                message = i,
                                keyboard = keyboard,
                                random_id = random.randint(0, 10000000))
                    if len(out) == 0:
                        numberNews = 'За последнее время не было новостей с данной тематикой.'
                    else:
                        numberNews = 'Статьи найдены!'
                    session_api.messages.send(
                            user_id = event.user_id,
                            message = numberNews,
                            keyboard = keyboard,
                            random_id = random.randint(0, 10000000))
            elif modeOut == 2:
                if event.text.lower() != 'вернуться к категориям':
                    modeOut = 3    
                    newRss = event.text.lower()
                    session_api.messages.send(
                            user_id = event.user_id,
                            message = 'Введите ключевые слова, которые вас интересуют.',
                            keyboard = keyboardBack,
                            random_id = random.randint(0, 10000000))
                else:
                    modeOut = 0
                    session_api.messages.send(
                            user_id = event.user_id,
                            message = 'Выберите направленность новостного сайта!',
                            keyboard = keyboard,
                            random_id = random.randint(0, 10000000))                    
            elif modeOut == 3:
                if event.text.lower() != 'вернуться к категориям':                
                    modeOut = 0
                    try:
                        outR = rsc(newRss,event.text.lower())
                        for i in outR:
                            session_api.messages.send(
                                    user_id = event.user_id,
                                    message = i,
                                    keyboard = keyboard,
                                    random_id = random.randint(0, 10000000))
                        if len(outR) == 0:
                            numberNews = 'За последнее время не было новостей с данной тематикой или представленная ссылка не выводит файл формата RSS или xml.'
                        else:
                            numberNews = 'Статьи найдены!'                    
                        session_api.messages.send(
                                user_id = event.user_id,
                                message = numberNews,
                                keyboard = keyboard,
                                random_id = random.randint(0, 10000000))
                    except Exception:
                        session_api.messages.send(
                                user_id = event.user_id,
                                message = "Упс! Или Rss лента неверна, или teg'и отсутствуют.\nПопробуйте снова! ",
                                keyboard = keyboard,
                                random_id = random.randint(0, 10000000))                    
                else:
                    modeOut = 0
                    session_api.messages.send(
                            user_id = event.user_id,
                            message = 'Выберите направленность новостного сайта!',
                            keyboard = keyboard,
                            random_id = random.randint(0, 10000000)) 
