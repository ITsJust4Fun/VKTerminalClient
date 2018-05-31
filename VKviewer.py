import vk_api
import time
import requests
from config import login, password
#Авторизация
vk_session = vk_api.VkApi(login, password)
vk_session.auth()
vk = vk_session.get_api()
#Получение обновлений(новые сообщения, кто-то вошёл в сеть, начал печатать сообщение и так далее)
def getdata():
    m = vk.messages.getLongPollServer()
    url = 'https://'+m['server']+'?act=a_check&key='+m['key']+'&ts='+ str(m['ts']) +'&wait=25&mode=2&version=1' 
    data = requests.get(url).json()
    return data
#Анализ полученных данных 
def messages():
    m = getdata()
    if len(m['updates']) >= 1:
        if len(m['updates'][0]) == 8:
            r = m['updates'][0][2]
            c = ''
            while r != 0:
                c = str(r % 2) + c
                r //= 2    
            if len(c) < 10:
                c = ('0' * (10 - len(c))) + c # C это флаг сообщения в двоичном коде. Например: 1000000011 означает, что сообщение исходящее, не прочитанное, и сожержит медиаконтент см: https://vk.com/dev/using_longpoll_2
            if c[-2] == '0':
                if m['updates'][0][3] < 2000000000: # 2000000000 + id это сообщение из беседы
                    if m['updates'][0][3] > 0: # id Это сообщения из ЛС
                        vk.messages.markAsRead(message_ids = m['updates'][0][1])
                        user = vk.users.get(user_id = m['updates'][0][3])
                        message = '| ' + time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(m['updates'][0][4])) + ' | ' + user[0]['first_name'] + ' ' + user[0]['last_name'] + '(ID - ' + str(m['updates'][0][3]) + '): ' + m['updates'][0][6]
                    if m['updates'][0][3] < 0: # -id Это сообщения от сообществ
                        vk.messages.markAsRead(message_ids = m['updates'][0][1])
                        group = vk.groups.getById(group_id = m['updates'][0][3] * (-1))
                        message = '| ' + time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(m['updates'][0][4])) + ' | ' + 'Сообщество ' + group[0]['name']  + '(ID - ' + str(m['updates'][0][3] * (-1)) + '): ' + m['updates'][0][6]
                else: # Это беседа ВК
                    vk.messages.markAsRead(message_ids = m['updates'][0][1])
                    userid = int(m['updates'][0][7]['from'])
                    groupchat_user = vk.users.get(user_id = userid, name_case = 'ins')
                    groupchat_user = groupchat_user[0]['first_name'] + ' ' + groupchat_user[0]['last_name']
                    message = '| ' + time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(m['updates'][0][4])) + ' | ' + 'Отправлено из беседы ' + m['updates'][0][5] + '(ID: ' + str(m['updates'][0][3])+ ')' + ' ' + groupchat_user + ' (ID: '+ str(userid)+ ' )' + ': ' + m['updates'][0][6]
            else: # Это исходящее сообщение
                if m['updates'][0][3] < 2000000000:
                    if m['updates'][0][3] > 0: # Исходящее в ЛС
                        vk.messages.markAsRead(message_ids = m['updates'][0][1])
                        user = vk.users.get(user_id = m['updates'][0][3], name_case='dat')
                        message = '| ' + time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(m['updates'][0][4])) + ' | ' + 'Вы отправили сообщение ' + user[0]['first_name'] + ' ' + user[0]['last_name'] + '(ID - ' + str(m['updates'][0][3]) + '): ' + m['updates'][0][6]
                    if m['updates'][0][3] < 0: # Исходящее в Сообщество
                        vk.messages.markAsRead(message_ids = m['updates'][0][1])
                        group = vk.groups.getById(group_id = m['updates'][0][3] * (-1))
                        message = '| ' + time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(m['updates'][0][4])) + ' | ' + 'Вы отправили сообщение сообществу ' + group[0]['name'] + '(ID - ' + str(m['updates'][0][3] * (-1)) + '): ' + m['updates'][0][6]
                else: # Исходящее в беседу
                    vk.messages.markAsRead(message_ids = m['updates'][0][1])
                    userid = int(m['updates'][0][7]['from'])
                    message = '| ' + time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(m['updates'][0][4])) + ' | ' + 'Сообщение отправлено вами в беседу ' + m['updates'][0][5] +' (ID: ' + str(m['updates'][0][3])+ ')' + ': ' + m['updates'][0][6]
        else:
            message = 'Нет новых сообщений'
    else:
        message = 'Нет новых сообщений'
    return message
while True: # Бесконечный цикл
    f = messages()
    if f != 'Нет новых сообщений':
        print(f)
