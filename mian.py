from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import Update, ReplyKeyboardMarkup
import sqlite3
import random
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
from config import TOKEN
table=sqlite3.connect('film.db')
otabek=table.cursor()
otabek.execute( """
Create Table if not exists film(
               id Integer Primary Key,
               Topic_name text ,
               name text,
               url text)


    """ )
table.commit()
text = [
    "😁", "😊", "😄", "😃", "😀", "😆", "🥰", "😍", "🤩", "😘",
    "😚", "😇", "😺", "😸", "😻", "👍", "👌", "👏", "🙌", "🙏",
    "💪", "🤝", "🫶", "💖", "💗", "💓", "💞", "💕", "❤️", "🧡",
    "💛", "💚", "💙", "💜", "🤍", "🤎", "💯", "🔥", "🌟", "✨",
    "🎉", "🎊", "🏆", "🥇", "🥈", "🥉", "🎖️", "🏅", "🌈", "☀️",
    "🌞", "🌸", "🌼", "🌻", "🌺", "🍀", "🍎", "🍉", "🍇", "🍓",
    "🍒", "🍩", "🍪", "🍰", "🧁", "🍫", "🥳", "😎", "🤗", "😇",
    "🤑", "🤓", "🫡", "💼", "📚", "📝", "🖊️", "✏️", "📖", "🧠",
    "🏡", "🚀", "🛸", "🎈", "🎂", "🎁", "🕺", "💃", "👑", "👼",
    "🦄", "🐱", "🐶", "🐣", "🐥", "🐢", "🦋", "🐞", "🌍", "🧳"
]

def start(update, context):
    table = sqlite3.connect('film.db')
    cursor = table.cursor()
    cursor.execute("SELECT DISTINCT Topic_name FROM film")
    topics = cursor.fetchall()
    table.close()

    topic_buttons = [[topic[0]] for topic in topics]  

    emoji1 = random.choice(text)
    emoji2 = random.choice(text)
    emoji3= random.choice(text)
    user = update.message.from_user
    username = user.username or user.first_name
    greeting = f"{emoji2} Xush kelibsiz, {username}! Bu yerda filmlarni topishingiz mumkin. {emoji3} Iltimos, zavqlaning va botimni {random.choice(text)} do'stlaringiz bilan ulashing {emoji1}"


    update.message.reply_text(
        greeting,
        reply_markup=ReplyKeyboardMarkup(topic_buttons, resize_keyboard=True)
    )

def show_names(update, context):
    selected_topic = update.message.text

    table = sqlite3.connect('film.db')
    cursor = table.cursor()
    cursor.execute("SELECT name FROM film WHERE Topic_name = ?", (selected_topic,))

    names = cursor.fetchall()
    
    table.close()
    emoji3= random.choice(text)
    if not names:
        update.message.reply_text("Bu mavzu uchun hech qanday nom topilmadi.")
        return

    name_buttons = [[name[0]] for name in names]

    update.message.reply_text(
        f"{emoji3} Mavzu ostidagi nomlar: {selected_topic}",
        reply_markup=ReplyKeyboardMarkup(name_buttons, resize_keyboard=True)
    )

def check_bot(update,context):
   user_text = update.message.text.lower().strip()
   text=update.message.text.lower().strip().split('/')
   table=sqlite3.connect('film.db')
   otabek=table.cursor()
   otabek.execute("SELECT url FROM film WHERE name = ?", (user_text,))
   result = otabek.fetchall()
   if result:
       otabek.execute("SELECT url FROM film WHERE name = ?", (user_text,))
       sardor = otabek.fetchone()
       update.message.reply_text(sardor[0])
   elif len(text)==3:
       
       


     
     topic=text[0]
     name=text[1]
     url=text[2]
     otabek.execute("INSERT INTO film (Topic_name, name, url) VALUES (?, ?, ?)", (topic, name, url))
     table.commit()
   else:
       show_names(update,context)




  









updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text,check_bot))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, show_names))




updater.start_polling()
updater.idle()
