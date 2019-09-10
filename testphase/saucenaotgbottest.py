import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
from saucenao import SauceNao

def image(update, context):
    print("accepted file")
    chat_id = update.message.chat_id
    print("mistake here?")
    bot = context.bot
    print("mistake here??")
    m = bot.getFile(update.message.document.file_id)
    print(m)
    print(m["file_path"])
    print("seems like no mistakes")
    miao = requests.get(m["file_path"])
    print("requests work")
    with open("latestsearch.jpg", "wb") as file:
        file.write(miao.content)
    saucenao = SauceNao(directory='directory', databases=999, minimum_similarity=65, combine_api_types=False, api_key='<YOUR_API_KEY>',
                    exclude_categories='', move_to_categories=False,  use_author_as_category=False,
                    output_type=SauceNao.API_HTML_TYPE, start_file='', log_level=logging.ERROR,
                    title_minimum_similarity=90)
    print("GOT HERE FINALLY")
    filtered_results = saucenao.check_file(
        file_name="<PATH>" + "\\latestsearch.jpg")
    print("HYPE INTENSIFIES")
    bot.sendMessage(chat_id=chat_id, text="Result Number 1\n" + "Title:\n" + str(filtered_results[0]["data"]["title"]) +"\n" + "Urls:\n" + filtered_results[0]["data"]["ext_urls"][0] + "\n" + filtered_results[0]["data"]["ext_urls"][1] + "\n" + "Contents:\n" + filtered_results[0]["data"]["content"][0] + "\n" + filtered_results[0]["data"]["content"][0] + "\n" + "Similarity Value: " + filtered_results[0]["header"]["similarity"] + "%")
print("got here")
updater = Updater(token='<BOT_TOKEN>', use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
print("still here")
img_handler = MessageHandler(Filters.photo | Filters.document | Filters.video , image)
dispatcher.add_handler(img_handler)
print("added handlyboy")
updater.start_polling()
print("running boye")
