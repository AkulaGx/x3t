# -*- coding: utf-8 -*-
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
import time
import requests
import os

token = "591fb217d5d86abd92db91e8dfc02f949e447722bab77f84e1cac8f8e03c411d09cada2e3935f0842631d"  # Токен от страницы
akkid = 655998017  # ID страницы
message_send_ids = "by dan1x for WoPX with love"

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
key = ""

if not os.path.exists("files/"):
    os.mkdir("files/")

def uploading_an_doc(event, name_image):
    try:
        a = vk.docs.getMessagesUploadServer(type='doc', user_id=event.user_id)
        b = requests.post(a['upload_url'], files={'file': open(name_image, "rb")}).json()
        c = vk.docs.save(file=b['file'], title=name_image)
        d = 'doc{}_{}'.format(c['doc']['owner_id'], c['doc']['id'])
        return d
    except Exception as e:
        print(str(e))

def send_ids(event, key):
    try:
        members = vk.messages.getConversationMembers(peer_id=event.peer_id)
        #i = 0
        message_doc = ""
        #message = "Список участников в беседе:"
        for member in members['profiles']:
            #i += 1
            #message += "\nВечная ссылка: https://vk.com/id" + str(member['id']) + "\nИмя: " + member['first_name'] + " " + member['last_name']
            message_doc += "Вечная ссылка: https://vk.com/id" + str(member['id']) + "\n" + "Имя:" + " " + member['first_name'] + " " + member['last_name'] + "\n\n"
            #if i == 50:
            #    vk.messages.send(user_id=event.user_id, message=message, random_id=0)
            #    i = 0
            #    message = ""
            #    time.sleep(1)
        #if i != 0:
        #    vk.messages.send(user_id=event.user_id, message=message, random_id=0)

        vk.messages.send(user_id=event.user_id, message=message_send_ids, random_id=0)
        name_image = "files/peer_"+ str(event.peer_id) + ".txt"
        my_file = open(name_image, "w")
        my_file.write(message_doc)
        my_file.close()
        vk.messages.send(user_id=event.user_id, attachment=uploading_an_doc(event, name_image), random_id=0)
    except Exception as e:
        print(str(e))

print("Успешная авторизация!")
done = False
while not done:
    try:
        def main():
            def run_listening():
                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW:
                        index = event.text.find(']')
                        if event.text.find('[') == 0 and index > 2 and event.text.find('id' + str(akkid) + '|') == 1:
                            res = event.text[index + 2:]
                        else:
                            res = event.text
                        res1 = res
                        res = res.lower()
                        if res:
                            if res[0] == "/":
                                res = res[1:]
                        if res.startswith(".getid"):  # Если написали заданную фразу
                            #if event.user_id == akkid:
                                send_ids(event, key)

            def check_internet_connection():
                """Checks internet connection by sending a request to vk.com"""
                try:
                    request = requests.get(url='https://vk.com/')
                    if request.status_code == 200:
                        return True
                    else:
                        return True
                except requests.exceptions.RequestException:
                    return False

            while True:
                try:
                    # Run longpoll_m listening.
                    run_listening()
                except requests.exceptions.RequestException:
                    while True:
                        # Check internet connection
                        internet_status = check_internet_connection()
                        # If everything is bad, we wait and try to connect again
                        if internet_status:
                            break
                        else:
                            print('VK_BOT [Longpoll Listening Error!]: Internet does not work!')
                        # Time to rest!
                        time.sleep(120)

        if __name__ == "__main__":
            main()
    except Exception as e:
        print(str(e))
        time.sleep(1)
