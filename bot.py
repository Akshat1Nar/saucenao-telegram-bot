'''
Coded by Vincenzo Sabella
Licensed under GNU Affero GPL 3.0 License, you should have received a copy with the software, otherwise you can find a
copy here: https://www.gnu.org/licenses/agpl-3.0.en.html

version : 0.1.2
'''
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
from saucenao import SauceNao
import os
import pickle
path = os.getcwd()
def setapi_callback(update, context):
    chat_id = update.message.chat_id
    bot = context.bot
    user_says = " ".join(context.args)
    Users = pickle.load(open("UsersAPIs.data", "rb"))
    Users[chat_id] = {}
    Users[chat_id]["api"] = user_says
    pickle.dump(Users, open("UsersAPIs.data", "wb"))

def image(update, context):
    chat_id = update.message.chat_id
    bot = context.bot
    m = bot.getFile(update.message.document.file_id)
    miao = requests.get(m["file_path"])
    with open("latestsearch.jpg", "wb") as file:
        file.write(miao.content)
    saucenao = SauceNao(directory='directory', databases=999, minimum_similarity=65, combine_api_types=False, api_key='<YOUR_SAUCENAO_API_KEY>',
                    exclude_categories='', move_to_categories=False,  use_author_as_category=False,
                    output_type=SauceNao.API_HTML_TYPE, start_file='', log_level=logging.ERROR,
                    title_minimum_similarity=90)
    filtered_results = saucenao.check_file(
        file_name=(str(path) + "\\latestsearch.jpg"))
    datanumber = len(filtered_results)
    pages = {}
    x = 0
    for i in range(0,datanumber):
        pages[str(x)] = filtered_results[x]["data"]
        pages[str(x)]["textstring"] = "Result Number: " + str(x +1) + "\n\n"
        # Adds title to the message
        pages[str(x)]["textstring"] += "Title:\n" + pages[str(x)]["title"] + "\n"

        # Adds content such like authors, ids, charachters etc... to the message
        contentnumber = len(pages[str(x)]["content"])
        y = 0
        for i in range(0,contentnumber):
            pages[str(x)]["textstring"] += "Contents:\n" + pages[str(x)]["content"][y] + "\n"
            y += 1

        # Adds urls to the message
        urlnumber = len(pages[str(x)]["ext_urls"])
        z = 0
        pages[str(x)]["textstring"] += "Urls:\n"
        for i in range(0,urlnumber):
            pages[str(x)]["textstring"] += pages[str(x)]["ext_urls"][z] + "\n"
            z += 1
        x += 1
    x = 0
    for i in range(0,len(pages)):
        bot.sendMessage(chat_id = chat_id, text = pages[str(x)]["textstring"])
        x += 1
updater = Updater(token='<BOT_TOKEN>', use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
img_handler = MessageHandler(Filters.photo | Filters.document, image)
setapi_handler = CommandHandler("setapi", setapi_callback)
dispatcher.add_handler(img_handler)
dispatcher.add_handler(setapi_handler)
updater.start_polling()
print("Bot Running")
