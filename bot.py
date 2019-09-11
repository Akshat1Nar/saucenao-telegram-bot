'''
Coded by Vincenzo Sabella
Licensed under GNU Affero GPL 3.0 License, you should have received a copy with the software, otherwise you can find a
copy here: https://www.gnu.org/licenses/agpl-3.0.en.html

version : 0.2.1
'''
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
from saucenao import SauceNao
import os
import pickle
path = os.getcwd()
def start(update, context):
    chat_id = update.message.chat_id
    bot = context.bot
    bot.sendMessage(chat_id=chat_id, text="Welcome to SauceNao Search Bot!\n"
                                          "if you like it please consider [donating](https://paypal.me/pools/c/8i8yRBYigc) and sharing the bot", parse_mode="Markdown")
def register(update, context):
    chat_id = update.message.chat_id
    bot = context.bot
    Users = pickle.load(open("UsersPers.data", "rb"))
    Users[chat_id] = {}
    pickle.dump(Users, open("UsersPers.data", "wb"))
    bot.sendMessage(chat_id = chat_id, text = "You registered your account or if you already had registered \nyou've just reset all personalizations")
def setapi_callback(update, context):
    chat_id = update.message.chat_id
    bot = context.bot
    user_says = " ".join(context.args)
    Users = pickle.load(open("UsersPers.data", "rb"))
    Users[chat_id]["api"] = user_says
    pickle.dump(Users, open("UsersPers.data", "wb"))
def showmeapi(update, context):
    chat_id = update.message.chat_id
    bot = context.bot
    Users = pickle.load(open("UsersAPIs.data", "rb"))
    bot.sendMessage(chat_id = chat_id, text ="This is the using saucenao api, use `/setapi <API>` to set up an api:\n\n" + "`" + Users[chat_id]["api"] + "`" , parse_mode="Markdown")
def setsimilarity_callback(update, context):
    chat_id = update.message.chat_id
    bot = context.bot
    user_says = " ".join(context.args)
    Users = pickle.load(open("UsersPers.data", "rb"))
    try:
        Users[chat_id]["similarity"] = int(user_says)
        if Users[chat_id]["similarity"] < 50:
            bot.sendMessage(chat_id=chat_id,
                        text="You choose: " + str(Users[chat_id]["similarity"]) + "\nand you shouldn't go under 50% to get good results, proceed at your own risk")
        else:
            bot.sendMessage(chat_id=chat_id, text="Congratulations, now your minimum similarity value is: `" + str(Users[chat_id]["similarity"]) +"`", parse_mode="Markdown")
    except KeyError:
        bot.sendMessage(chat_id=chat_id, text="You're not registered, please use `/register` to register your account", parse_mode="Markdown")
    except ValueError:
        bot.sendMessage(chat_id=chat_id, text="PLEASE ONLY NUMBER VALUES FROM 0-100\nYou shouldn't go under 50% to get good results")
    except:
        raise
    pickle.dump(Users, open("UsersPers.data", "wb"))
def image(update, context):
    chat_id = update.message.chat_id
    bot = context.bot
    m = bot.getFile(update.message.document.file_id)
    miao = requests.get(m["file_path"])
    with open("latestsearch.jpg", "wb") as file:
        file.write(miao.content)
    Users = pickle.load(open("UsersPers.data", "rb"))
    try:
        saucenao = SauceNao(directory='directory', databases=999, minimum_similarity=Users[chat_id]["similarity"], combine_api_types=False, api_key=Users[chat_id]["api"],
                    exclude_categories='', move_to_categories=False,  use_author_as_category=False,
                    output_type=SauceNao.API_HTML_TYPE, start_file='', log_level=logging.ERROR,
                    title_minimum_similarity=90)
    except KeyError:
        bot.sendMessage(chat_id=chat_id, text="Something bad happened with your personalization, \nuse `/register` to reset them and then redo the setup, "
                                              "\nfor this search I'll use base config "
                                              "\nremember setting up either api and similarity "
                                              "\nthe api is optiona so you can even launch a blank `/setapi` command", parse_mode="Markdown")
        saucenao = SauceNao(directory='directory', databases=999, minimum_similarity=65, combine_api_types=False, api_key="",
                    exclude_categories='', move_to_categories=False,  use_author_as_category=False,
                    output_type=SauceNao.API_HTML_TYPE, start_file='', log_level=logging.ERROR,
                    title_minimum_similarity=90)
    filtered_results = saucenao.check_file(file_name=(str(path) + "\\latestsearch.jpg"))
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
updater = Updater(token='<YOUR_TOKEN>', use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
img_handler = MessageHandler(Filters.photo | Filters.document, image)
setapi_handler = CommandHandler("setapi", setapi_callback)
showmeapi_handler = CommandHandler("showmeapi", showmeapi)
register_handler = CommandHandler("register", register)
setsimilarity_handler = CommandHandler("setsimilarity", setsimilarity_callback)
start_handler = CommandHandler("start", start)
dispatcher.add_handler(img_handler)
dispatcher.add_handler(setapi_handler)
dispatcher.add_handler(showmeapi_handler)
dispatcher.add_handler(register_handler)
dispatcher.add_handler(setsimilarity_handler)
dispatcher.add_handler(start_handler)
updater.start_polling()
print("Bot Running")
