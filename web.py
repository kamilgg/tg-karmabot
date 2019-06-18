import logging
import os
import sys
from time import sleep

import flask
import telebot
from flask import Flask

sys.path.append('./karmabot')

from config import token, botName, chatId, admins, database, host, user, password
from config import helpText, welcomeText, welcomeUser, dontWork, notUsername, shouldReply, thxToBot, botMinus, \
    masturbate, unmasturbate, karmaPlus, karmaMinus, banForKarma, cantBan, \
    cantUnban, banned, unbanned
from db_control import DB, UsersModel, KarmaModel

# connect to DB
connection = DB(database, host, user, password)
users_model = UsersModel(connection.get_connection())
users_model.init_table()
karma_model = KarmaModel(connection.get_connection())

bot = telebot.TeleBot(token)


@bot.message_handler(content_types=['new_chat_members'])
def welcome(w):
    if w.chat.id == chatId:
        if w.new_chat_member.username is None:
            username = str(w.new_chat_member.first_name) + " " + str(w.new_chat_member.last_name)
            bot.send_message(w.chat.id, text=welcomeUser % username)
        else:
            username = str(w.new_chat_member.username)
            id = int(w.new_chat_member.id)
            users_model.new_user(id, username)
            bot.send_message(w.chat.id, text=welcomeText % username)
    else:
        bot.send_message(w.chat.id, parse_mode='Markdown', text=dontWork)


@bot.message_handler(commands=['help'])
def help(h):
    if h.chat.id == chatId:
        bot.send_message(h.chat.id, parse_mode='Markdown', text=helpText)
    else:
        bot.send_message(h.chat.id, parse_mode='Markdown', text=dontWork)


@bot.message_handler(regexp="Thank you")
def karma_plus(kp):
    if kp.chat.id == chatId:
        username = kp.from_user.username
        if kp.reply_to_message is None:
            bot.send_message(kp.chat.id, parse_mode='Markdown', text=shouldReply % username)
        else:
            if (kp.reply_to_message.from_user.username is None) or ():
                bot.send_message(kp.chat.id, text=notUsername)
            else:
                to_user = kp.reply_to_message.from_user.username
                user_id = kp.reply_to_message.from_user.id
                if to_user == botName:
                    bot.send_message(kp.chat.id, text=thxToBot % username)
                elif to_user == username:
                    bot.send_message(kp.chat.id, text=masturbate % username)
                else:
                    karma_model.karma_plus(user_id, to_user)
                    karma = karma_model.current_karma(user_id)
                    bot.send_message(kp.chat.id, text=karmaPlus % (to_user, to_user, karma))
    else:
        bot.send_message(kp.chat.id, parse_mode='Markdown', text=dontWork)


@bot.message_handler(regexp="Minus")
def karma_minus(km):
    if km.chat.id == chatId:
        username = km.from_user.username
        if km.reply_to_message is None:
            bot.send_message(km.chat.id, parse_mode='Markdown', text=shouldReply % username)
        else:
            if km.reply_to_message.from_user.username is None:
                bot.send_message(km.chat.id, text=notUsername)
            else:
                to_user = km.reply_to_message.from_user.username
                user_id = km.reply_to_message.from_user.id
                if to_user == botName:
                    bot.send_message(km.chat.id, text=botMinus % username)
                elif to_user == username:
                    bot.send_message(km.chat.id, text=unmasturbate % username)
                else:
                    ans = karma_model.karma_minus(user_id, to_user)
                    karma = karma_model.current_karma(user_id)
                    if ans == 1:
                        bot.send_message(km.chat.id, text=karmaMinus % (to_user, to_user, karma))
                    elif ans == 2:
                        bot.restrict_chat_member(km.chat.id, user_id, can_send_messages=False,
                                                 can_send_media_messages=False, can_send_other_messages=False,
                                                 can_add_web_page_previews=False)
                        bot.send_message(km.chat.id, text=banForKarma)
    else:
        bot.send_message(km.chat.id, parse_mode='Markdown', text=dontWork)


@bot.message_handler(commands=['top20'])
def top20(t20):
    if t20.chat.id == chatId:
        bot.send_message(t20.chat.id, parse_mode='Markdown', text=karma_model.top20())
    else:
        bot.send_message(t20.chat.id, parse_mode='Markdown', text=dontWork)


@bot.message_handler(commands=['untop20'])
def untop20(ut20):
    if ut20.chat.id == chatId:
        bot.send_message(ut20.chat.id, parse_mode='Markdown', text=karma_model.untop20())
    else:
        bot.send_message(ut20.chat.id, parse_mode='Markdown', text=dontWork)


@bot.message_handler(commands=['ban'])
def ban(b):
    if b.chat.id == chatId:
        if b.from_user.id in admins:
            username = str(b.text)[6:]
            user_id = int(users_model.id_of_user(username))
            if user_id == 0:
                bot.send_message(b.chat.id, text=cantBan)
            else:
                bot.restrict_chat_member(b.chat.id, user_id, can_send_messages=False, can_send_media_messages=False,
                                         can_send_other_messages=False, can_add_web_page_previews=False)
                bot.send_message(b.chat.id, text=banned)
    else:
        bot.send_message(b.chat.id, parse_mode='Markdown', text=dontWork)


@bot.message_handler(commands=['unban'])
def unban(ub):
    if ub.chat.id == chatId:
        if ub.from_user.id in admins:
            username = str(ub.text)[8:]
            user_id = int(users_model.id_of_user(username))
            if user_id == 0:
                bot.send_message(ub.chat.id,
                                 text=cantUnban)
            else:
                bot.restrict_chat_member(ub.chat.id, user_id, can_send_messages=True, can_send_media_messages=True,
                                         can_send_other_messages=True, can_add_web_page_previews=True)
                bot.send_message(ub.chat.id, text=unbanned)
    else:
        bot.send_message(ub.chat.id, parse_mode='Markdown', text=dontWork)


# webhook

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

server = Flask(__name__)


@server.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


@server.route("/%s/" % token, methods=['POST'])
def getMessage():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


bot.remove_webhook()
sleep(1)
bot.set_webhook(url="https://karmabot.herokuapp.com/%s/" % token)

server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 80)), debug=True)
