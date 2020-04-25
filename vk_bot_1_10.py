import datetime

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random

vk_session = vk_api.VkApi(
    token=TOKEN)

longpoll = VkBotLongPoll(vk_session, GROUP_ID)
vk = vk_session.get_api()

day = {0: 'понедельник', 1: 'вторник', 2: 'среда', 3: 'четверг',
       4: 'пятница', 5: 'суббота', 6: 'воскресенье'}


def weekday_response(request_data):
    date = datetime.datetime.strptime(request_data, '%Y-%m-%d').weekday()
    return day[date]


def help():
    return f"Write the date in the format 'YYYY-MM-DD' and I will say the day of the week."


def main():
    flag_data, flag_help = False, True
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and flag_help:
            flag_data = not flag_data
            flag_help = not flag_help
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=help(),
                             random_id=random.randint(0, 2 ** 64))

        elif event.type == VkBotEventType.MESSAGE_NEW and flag_data:
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=f"{weekday_response(event.obj.message['text'])}\n\n{help()}",
                             random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()
