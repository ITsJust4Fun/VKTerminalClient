import vk_api
import time
from config import login, password
# Авторизация
vk_session = vk_api.VkApi(login, password)
vk_session.auth()
vk = vk_session.get_api()
# Написанние сообщения
def otvet():
    print('Введите ID пользователя (id положительный) или сообщества (id отрицательный) или беседы (2000000000 + id) и сообщение через пробел')
    mess = input()
    g = mess.find(' ')
    userid = int(mess[:g]) # id беседы (2000000000 + id), user (id), сообщества (-id)
    mess = mess[g+1:]  # Сообщение которое нужно отправить
    if userid < 2000000000:
        if userid > 0: # Отправить сообщение ЛС
            yid = vk.messages.send(user_id = userid, message = mess)
            vk.messages.markAsRead(message_ids = yid)
            m = vk.users.get(user_id = userid, name_case = 'dat')
            name = m[0]['first_name'] + ' ' + m[0]['last_name']
            print('Сообщение отправлено',name,'( ID:',str(userid),')')
        if userid < 0: # Отправить сообщение сообществу
            yid = vk.messages.send(user_id = userid, message = mess)
            vk.messages.markAsRead(message_ids = yid)
            userid = userid * (-1)
            m = vk.groups.getById(group_id = userid)
            print('Сообщение отправлено сообществу',m[0]['name'],'( ID:',str(userid),')')
    else: # Отправить сообщение в беседу
        userid -= 2000000000
        yid = vk.messages.send(chat_id = userid, message = mess)
        vk.messages.markAsRead(message_ids = yid)
        chat = vk.messages.getChat(chat_id = userid)
        userid += 2000000000
        print('Сообщение отправлено в беседу', chat['title'], '( ID: ', str(userid), ')')
    otvet()
otvet()
    
