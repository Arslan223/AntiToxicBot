import json
import requests
import telebot
import gdata
import time
from math import floor
from consts import API_KEY, BOT_API_KEY



def get_toxicity(phrase, lang="ru", api_key=API_KEY):
    url = ('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze' +
           '?key=' + api_key)
    data_dict = {
        'comment': {'text': phrase},
        'languages': [lang],
        'requestedAttributes': {'TOXICITY': {}}
    }
    response = requests.post(url=url, data=json.dumps(data_dict))
    response_dict = json.loads(response.content)
    return response_dict["attributeScores"]["TOXICITY"]["summaryScore"]["value"]


def main():
    bot = telebot.TeleBot(BOT_API_KEY)

    @bot.message_handler(commands=["settings"])
    def on_settings(message):
        chat_id = str(message.chat.id)
        user_id = str(message.from_user.id)
        data = gdata.load()
        if not (chat_id in data):
            data.update({chat_id: {"users": {}, "mode": 1, "value": 0.85, "can_del": True}})
            gdata.update(data)

        data = gdata.load()
        if not (user_id in data[chat_id]["users"]):
            data[chat_id]["users"].update({user_id: {"limit": None, "score": 0,
                                                     "first_name": message.from_user.first_name,
                                                     "last_name": message.from_user.last_name, "id": user_id,
                                                     "count": 1}})
        gdata.update(data)
        admins = [str(member.user.id) for member in bot.get_chat_administrators(chat_id)]
        if user_id in admins:
            markup = telebot.types.InlineKeyboardMarkup()
            btn1 = telebot.types.InlineKeyboardButton(f"Все" if data[chat_id]["can_del"] else f"Только админы", callback_data="ch_c_all")
            btn2 = telebot.types.InlineKeyboardButton("Режим", callback_data="ch_r")
            btn3 = telebot.types.InlineKeyboardButton("Чувствительность", callback_data="h_c")
            markup.row(btn1)
            markup.row(btn2)
            markup.row(btn3)
            bot.reply_to(message, "*Настройки бота:*\n\n_Кто может удалять токсичные сообщения?_", reply_markup=markup, parse_mode="Markdown")

    @bot.message_handler(commands=["limit"])
    def on_settings(message):
        try:
            chat_id = str(message.chat.id)
            user_id = str(message.from_user.id)
            data = gdata.load()
            if not (chat_id in data):
                data.update({chat_id: {"users": {}, "mode": 1, "value": 0.85, "can_del": True}})
                gdata.update(data)

            data = gdata.load()
            if not (user_id in data[chat_id]["users"]):
                data[chat_id]["users"].update({user_id: {"limit": None, "score": 0,
                                                         "first_name": message.from_user.first_name,
                                                         "last_name": message.from_user.last_name, "id": user_id,
                                                         "count": 1}})
            gdata.update(data)
            data = gdata.load()
            buser_id = str(message.reply_to_message.from_user.id)
            admins = [str(member.user.id) for member in bot.get_chat_administrators(chat_id)]
            flag = False
            try:
                limit = float(message.text[7:])
            except ValueError:
                flag = True
            if len(message.text) < 8 or limit > 1 or limit < 0 or not(user_id in admins) or buser_id == '1442103439' or flag:
                bot.reply_to(message, "⛔️")
            else:
                if limit == 0:
                    limit = None
                try:
                    data[chat_id]["users"][buser_id]["limit"] = limit
                    gdata.update(data)
                    bot.reply_to(message.reply_to_message,
                                 "Новый лимит пользователя - " + (str(limit) if limit != None else "по умолчанию"))
                except:
                    bot.reply_to(message, "⛔️")

        except AttributeError:
            pass

    @bot.message_handler(commands=["top"])
    def on_top(message):
        chat_id = str(message.chat.id)
        user_id = str(message.from_user.id)
        data = gdata.load()
        if not (chat_id in data):
            data.update({chat_id: {"users": {}, "mode": 1, "value": 0.85, "can_del": True}})
            gdata.update(data)

        data = gdata.load()
        if not (user_id in data[chat_id]["users"]):
            data[chat_id]["users"].update({user_id: {"limit": None, "score": 0,
                                                     "first_name": message.from_user.first_name,
                                                     "last_name": message.from_user.last_name, "id": user_id,
                                                     "count": 1}})
        gdata.update(data)
        data = gdata.load()
        string = "*Адекватность*\n\n"
        users = [data[chat_id]["users"][i] for i in data[chat_id]["users"]]
        users = sorted(users, key=lambda user: user["score"] // data[chat_id]['users'][str(user['id'])]['count'])
        # users.reverse()
        medals = ["🥇", "🥈", "🥉"]
        for i in range(len(users)):
            if i < 3:
                string += medals[i] + " "
            user = users[i]
            user_last_name = user["last_name"] if user["last_name"] is not None else ""
            string += f"_{user['first_name']} {user_last_name}_ - `{data[chat_id]['users'][str(user['id'])]['score'] // data[chat_id]['users'][str(user['id'])]['count']}` 🍬\n"
        bot.reply_to(message, string, parse_mode="Markdown")

    @bot.message_handler(commands=["users"])
    def on_top(message):
        chat_id = str(message.chat.id)
        user_id = str(message.from_user.id)
        data = gdata.load()
        if not (chat_id in data):
            data.update({chat_id: {"users": {}, "mode": 1, "value": 0.85, "can_del": True}})
            gdata.update(data)

        data = gdata.load()
        if not (user_id in data[chat_id]["users"]):
            data[chat_id]["users"].update({user_id: {"limit": None, "score": 0,
                                                     "first_name": message.from_user.first_name,
                                                     "last_name": message.from_user.last_name, "id": user_id,
                                                     "count": 1}})
        gdata.update(data)
        data = gdata.load()
        string = "*Пользователи*\n\n"
        users = [data[chat_id]["users"][i] for i in data[chat_id]["users"]]
        users = sorted(users, key=lambda user: user["score"])
        # users.reverse()
        medals = ["🥇", "🥈", "🥉"]
        for i in range(len(users)):
            user = users[i]
            user_last_name = user["last_name"] if user["last_name"] is not None else ""
            string += f"_{user['first_name']} {user_last_name}_ - `{data[chat_id]['users'][str(user['id'])]['limit']}` 🦴\n"
        bot.reply_to(message, string, parse_mode="Markdown")

    @bot.message_handler(commands=["help"])
    def on_top(message):
        string = "*Помощь*\nЗдравствуйте, этот бот необходим для того, чтобы бороться с токсиками!\n\nКоманды:\n"+\
                "/top - _Отображает топ пользователей по адекватности_\n"+\
                 "/settings - _Отображает меню настроек бота (только для админов)_\n"+\
                "/limit `{значение от 0 до 1 включительно}` - _Изменить чувствительность для конкретного пользователя. \n"+\
                "При значении 0 лимит сбрасывается. (только для админов)_\n"+\
                "/users - _Отображает список пользователей и их лимиты_\n"+\
                "\n\nБаг репорт - @arslan2233"
        bot.reply_to(message, string, parse_mode="Markdown")




    @bot.message_handler(content_types=['text', 'audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice', 'location', 'contact', 'new_chat_members', 'left_chat_member', 'new_chat_title', 'new_chat_photo', 'delete_chat_photo', 'group_chat_created', 'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message'], func=lambda message: True)
    def reply_message(message):
        chat_id = str(message.chat.id)
        user_id = str(message.from_user.id)

        data = gdata.load()
        if not(chat_id in data):
            data.update({chat_id: {"users": {}, "mode": 1, "value": 0.85, "can_del": True}})
            gdata.update(data)

        data = gdata.load()
        if not(user_id in data[chat_id]["users"]):
            data[chat_id]["users"].update({user_id: {"limit": None, "score": 0, "first_name": message.from_user.first_name, "last_name": message.from_user.last_name, "id": user_id, "count": 1}})
        data[chat_id]["users"][user_id]["count"] += 1
        gdata.update(data)

        try:
            toxicity = get_toxicity(message.text)
            if toxicity is None:
                raise Exception
        except Exception as e:
            print(e)
            toxicity = 0
        data = gdata.load()
        try:
            print(data[chat_id]["users"][user_id]["limit"])
            data[chat_id]["users"][user_id]["score"] += floor(toxicity * 100)
            if toxicity > (data[chat_id]["users"][user_id]["limit"] if data[chat_id]["users"][user_id]["limit"] is not None else data[chat_id]["value"]):
                if data[chat_id]["mode"] == 2:
                    bot.delete_message(chat_id, message.message_id)
                elif data[chat_id]["mode"] == 1:
                    markup = telebot.types.InlineKeyboardMarkup()
                    btn = telebot.types.InlineKeyboardButton("Delete", callback_data=f"del{str(message.message_id)}")
                    markup.row(btn)
                    bot.reply_to(message, f"Toxic alert", parse_mode="Markdown", reply_markup=markup)

            gdata.update(data)
        except TypeError as e:
            print(e)
            pass

    @bot.callback_query_handler(func=lambda query: query.data.startswith("del"))
    def to_query(query):
        data = gdata.load()
        user_id = str(query.from_user.id)
        chat_id = str(query.message.chat.id)
        admins = [str(member.user.id) for member in bot.get_chat_administrators(chat_id)]
        # print(user_id, admins)
        if user_id in admins or data[chat_id]["can_del"]:
            m_id = query.data[3:]
            bot.delete_message(query.message.chat.id, m_id)
            bot.delete_message(query.message.chat.id, query.message.message_id)
        else:
            bot.answer_callback_query(query.id, "Вы не админ", show_alert=True)

    @bot.callback_query_handler(func=lambda query: query.data == "ch_c_all")
    def ch_c_all(query):
        chat_id = str(query.message.chat.id)
        user_id = str(query.from_user.id)
        admin_id = str(query.message.reply_to_message.from_user.id)
        admins = [str(member.user.id) for member in bot.get_chat_administrators(chat_id)]
        data = gdata.load()
        if user_id == admin_id:
            data[chat_id]["can_del"] = not(data[chat_id]["can_del"])
            gdata.update(data)
            markup = telebot.types.InlineKeyboardMarkup()
            btn1 = telebot.types.InlineKeyboardButton(f"Все" if data[chat_id]["can_del"] else f"Только админы", callback_data="ch_c_all")
            btn2 = telebot.types.InlineKeyboardButton("Режим", callback_data="ch_r")
            btn3 = telebot.types.InlineKeyboardButton("Чувствительность", callback_data="h_c")
            markup.row(btn1)
            markup.row(btn2)
            markup.row(btn3)
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=query.message.message_id, reply_markup=markup)
        else:
            bot.answer_callback_query(query.id, "Эту панель настроек вызвали не вы", show_alert=True)

    @bot.callback_query_handler(func=lambda query: query.data == "ch_r")
    def ch_r(query):
        chat_id = str(query.message.chat.id)
        user_id = str(query.from_user.id)
        admin_id = str(query.message.reply_to_message.from_user.id)
        admins = [str(member.user.id) for member in bot.get_chat_administrators(chat_id)]
        data = gdata.load()
        if user_id == admin_id:
            markup = telebot.types.InlineKeyboardMarkup()
            func = lambda mode: mode == data[chat_id]["mode"]
            mark1 = lambda mode: ">" if func(mode) else ""
            mark2 = lambda mode: "<" if func(mode) else ""
            btn1 = telebot.types.InlineKeyboardButton(f"{mark1(0)} Выключен {mark2(0)}", callback_data="chmode0")
            btn2 = telebot.types.InlineKeyboardButton(f"{mark1(1)} Обычный {mark2(1)}", callback_data="chmode1")
            btn3 = telebot.types.InlineKeyboardButton(f"{mark1(2)} Тихий {mark2(2)}", callback_data="chmode2")
            btn4 = telebot.types.InlineKeyboardButton(f"↩️", callback_data="back")
            markup.row(btn1)
            markup.row(btn2)
            markup.row(btn3)
            markup.row(btn4)

            bot.edit_message_text(chat_id=chat_id, message_id=query.message.message_id, text="*Изменение режима*", parse_mode="Markdown")
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=query.message.message_id, reply_markup=markup)
        else:
            bot.answer_callback_query(query.id, "Эту панель настроек вызвали не вы", show_alert=True)

    @bot.callback_query_handler(func=lambda query: query.data.startswith("h_c"))
    def ch_cc(query):
        chat_id = str(query.message.chat.id)
        user_id = str(query.from_user.id)
        admin_id = str(query.message.reply_to_message.from_user.id)
        admins = [str(member.user.id) for member in bot.get_chat_administrators(chat_id)]
        data = gdata.load()
        if user_id == admin_id:
            markup = telebot.types.InlineKeyboardMarkup()
            func = lambda mode: mode == data[chat_id]["value"]
            mark1 = lambda mode: ">" if func(mode) else ""
            mark2 = lambda mode: "<" if func(mode) else ""
            val = 1
            btn = telebot.types.InlineKeyboardButton(f"{mark1(val)} {str(val)} {mark2(val)}",
                                                     callback_data=f"c_c{str(val)}")
            markup.row(btn)
            for i in range(0, 5):
                val = round(0.95 - i / 10, 2)
                btn = telebot.types.InlineKeyboardButton(f"{mark1(val)} {str(val)} {mark2(val)}", callback_data=f"c_c{str(val)}")
                markup.row(btn)
            btn4 = telebot.types.InlineKeyboardButton(f"↩️", callback_data="back")
            markup.row(btn4)

            bot.edit_message_text(chat_id=chat_id, message_id=query.message.message_id, text="*Изменение чувствительности*\n\n_Чем больше чувствительность - тем на менее агрессивные сообщения будет реагировать бот_", parse_mode="Markdown")
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=query.message.message_id, reply_markup=markup)
        else:
            bot.answer_callback_query(query.id, "Эту панель настроек вызвали не вы", show_alert=True)

    @bot.callback_query_handler(func=lambda query: query.data.startswith("chmode"))
    def chmode(query):
        chat_id = str(query.message.chat.id)
        user_id = str(query.from_user.id)
        admin_id = str(query.message.reply_to_message.from_user.id)
        admins = [str(member.user.id) for member in bot.get_chat_administrators(chat_id)]
        mode_ch = int(query.data[6:])
        data = gdata.load()
        if user_id == admin_id:
            data[chat_id]["mode"] = mode_ch
            gdata.update(data)
            out_text_arr = [
                "Теперь бот не будет реагировать на агрессию (но он все еще учитывает сообщения для 'Топа токсиков')",
                "Теперь бот, если посчитает сообщение агрессивным, отправит предупрежение, \
                и пользователи смогут удалить сообщение (рекомендуется)",
                "Теперь бот будет втихую удалять сообщения с агрессией"
            ]
            bot.answer_callback_query(query.id, out_text_arr[mode_ch], show_alert=True)

            markup = telebot.types.InlineKeyboardMarkup()
            func = lambda mode: mode == data[chat_id]["mode"]
            mark1 = lambda mode: ">" if func(mode) else ""
            mark2 = lambda mode: "<" if func(mode) else ""
            btn1 = telebot.types.InlineKeyboardButton(f"{mark1(0)} Выключен {mark2(0)}", callback_data="chmode0")
            btn2 = telebot.types.InlineKeyboardButton(f"{mark1(1)} Обычный {mark2(1)}", callback_data="chmode1")
            btn3 = telebot.types.InlineKeyboardButton(f"{mark1(2)} Тихий {mark2(2)}", callback_data="chmode2")
            btn4 = telebot.types.InlineKeyboardButton(f"↩️", callback_data="back")
            markup.row(btn1)
            markup.row(btn2)
            markup.row(btn3)
            markup.row(btn4)

            bot.edit_message_text(chat_id=chat_id, message_id=query.message.message_id, text="*Изменение режима*", parse_mode="Markdown")
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=query.message.message_id, reply_markup=markup)
        else:
            bot.answer_callback_query(query.id, "Эту панель настроек вызвали не вы", show_alert=True)

    @bot.callback_query_handler(func=lambda query: query.data == "back")
    def back(query):
        chat_id = str(query.message.chat.id)
        user_id = str(query.from_user.id)
        admin_id = str(query.message.reply_to_message.from_user.id)
        admins = [str(member.user.id) for member in bot.get_chat_administrators(chat_id)]
        data = gdata.load()
        if user_id == admin_id:
            gdata.update(data)
            markup = telebot.types.InlineKeyboardMarkup()
            btn1 = telebot.types.InlineKeyboardButton(f"Все" if data[chat_id]["can_del"] else f"Только админы", callback_data="ch_c_all")
            btn2 = telebot.types.InlineKeyboardButton("Режим", callback_data="ch_r")
            btn3 = telebot.types.InlineKeyboardButton("Чувствительность", callback_data="h_c")
            markup.row(btn1)
            markup.row(btn2)
            markup.row(btn3)
            bot.edit_message_text(chat_id=chat_id, message_id=query.message.message_id, text="*Настройки бота:*\n\n_Кто может удалять токсичные сообщения?_", parse_mode="Markdown")
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=query.message.message_id, reply_markup=markup)
        else:
            bot.answer_callback_query(query.id, "Эту панель настроек вызвали не вы", show_alert=True)

    @bot.callback_query_handler(func=lambda query: query.data.startswith("c_c"))
    def c_c(query):
        chat_id = str(query.message.chat.id)
        user_id = str(query.from_user.id)
        admin_id = str(query.message.reply_to_message.from_user.id)
        admins = [str(member.user.id) for member in bot.get_chat_administrators(chat_id)]

        val = float(query.data[3:])
        data = gdata.load()
        if user_id == admin_id:
            data[chat_id]["value"] = val
            gdata.update(data)
            markup = telebot.types.InlineKeyboardMarkup()
            func = lambda mode: mode == data[chat_id]["value"]
            mark1 = lambda mode: ">" if func(mode) else ""
            mark2 = lambda mode: "<" if func(mode) else ""
            for i in range(0, 5):
                val = round(0.95 - i / 10, 2)
                btn = telebot.types.InlineKeyboardButton(f"{mark1(val)} {str(val)} {mark2(val)}",
                                                         callback_data=f"c_c{str(val)}")
                markup.row(btn)
            btn4 = telebot.types.InlineKeyboardButton(f"↩️", callback_data="back")
            markup.row(btn4)

            bot.edit_message_text(chat_id=chat_id, message_id=query.message.message_id, text="*Изменение чувствительности*\n\n_Чем больше чувствительность - тем на менее агрессивные сообщения будет реагировать бот_", parse_mode="Markdown")
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=query.message.message_id, reply_markup=markup)
        else:
            bot.answer_callback_query(query.id, "Эту панель настроек вызвали не вы", show_alert=True)

    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            bot.send_message(316490607, e)
            time.sleep(5)





if __name__ == '__main__':
    main()
