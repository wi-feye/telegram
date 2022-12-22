from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from dotenv import dotenv_values
from requests import get, post


config = dotenv_values('env_file')
TOKEN = config["TOKEN"]
WIFEYE_DATA_MANAGER = config["WIFEYE_DATA_MANAGER"]
WIFEYE_USER_MANAGER = config["WIFEYE_USER_MANAGER"]


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def help(update, context):
    update.message.reply_text('Help!')


def send_message(update, context):
    body = {
        "chatid": update.effective_chat.id,
        "tmpcode": update.message.text
    }
    res = post(
        f"{WIFEYE_DATA_MANAGER}/api/user_telegram/add_chatid", json=body).json()
    if "status" in res and res["status"]:
        id_user = res["user_telegram"]["id_user"]
        res_user = get(
            f"{WIFEYE_USER_MANAGER}/user?id={id_user}")
        if res_user.ok:
            user = res_user.json()
            username = user["name"] + " " + user["surname"]
            update.message.reply_text(
                f"Congratulations {username}, now you are associated with telegram bot.")
    else:
        update.message.reply_text(f"Incorrect temporal code.")


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, send_message))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
