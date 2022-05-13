import telebot
from environs import Env
import traceback
from model import UserController
import time
import math

env = Env()
env.read_env()

API_KEY = env("API_KEY")
print(API_KEY)
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=["Greet"])
def greet(message):
    print(message)
    bot.reply_to(message, "hey, how is it going")
    bot.send_message(message.chat.id, "hey, how is it going - no reply")


@bot.message_handler(commands=["start"])
def start(message):
    print(message)
    user = UserController(message.chat.id)

    if user.user.existing:
        bot.send_message(
            message.chat.id,
            "You already in our notification list\n\n"
            + user.user.subscription_str()
            + """\n
Thanks you for using Yhanl's DClone Bot

/me - to show what your subcribed to
/status - to show status relate to your subscription
/status all - to show all dclone status

Support single or multiple item in the sametime
/add xxx - to add subscription eg "/add NA EU progress 456 hardcore"
/remove xxx - to remove subscription eg "/remove NA EU progress 456 hardcore"

/unsubscribe - to remove yourself from notification list completely

Keep your notification active to not miss a walk. Enjoy!!
""",
        )
    else:
        user.subscribe_default()
        bot.send_message(
            message.chat.id,
            """Thanks you for using Yhanl's DClone Bot

/me - to show what your subcribed to
/status - to show status relate to your subscription
/status all - to show all dclone status

Support single or multiple item in the sametime
/add xxx - to add subscription eg "/add NA EU progress 456 hardcore"
/remove xxx - to remove subscription eg "/remove NA EU progress 456 hardcore"

/unsubscribe - to remove yourself from notification list completely

Keep your notification active to not miss a walk. Enjoy!!\n\n
"""
            + "You have defaulted to All region , Softcore, Ladder only, and Progress 4,5,6",
        )


@bot.message_handler(commands=["me"])
def me(message):
    print(message.chat.id, message.text)
    user = UserController(message.chat.id)
    if user.user.existing:
        bot.send_message(
            message.chat.id,
            "Your current subscription\n\n" + user.user.subscription_str(),
        )
    else:
        bot.send_message(
            message.chat.id,
            "You dont have any subscription with us, send /start to subscribe",
        )


@bot.message_handler(commands=["status"])
def status(message):
    print(message.chat.id, message.text)
    user = UserController(message.chat.id)
    if user.user.existing and "all" not in message.text:
        bot.send_message(
            message.chat.id,
            "base on your current subscription\n\n" + user.related_status(),
        )
    else:
        bot.send_message(
            message.chat.id,
            (
                "You dont have any subscription with us, showing all status\n\n"
                if not user.user.existing
                else "Showing all status\n\n"
            )
            + user.related_status(all=True),
        )


@bot.message_handler(commands=["unsubscribe"])
def unsub(message):
    print(message.chat.id, message.text)
    user = UserController(message.chat.id)
    user.unsub_user()
    bot.reply_to(
        message, "you have completely unsubscribed, /start to subscribe again."
    )


@bot.message_handler(commands=["add"])
def add(message):
    print(message.chat.id, message.text)
    user = UserController(message.chat.id)
    command = message.text
    reply = user.update_user(command)
    bot.reply_to(message, reply)


@bot.message_handler(commands=["remove"])
def remove(message):
    print(message.chat.id, message.text)
    user = UserController(message.chat.id)
    command = message.text
    reply = user.update_user(command)
    bot.reply_to(message, reply)


# bot.send_message("5320135248", "dclone")


def send_notification(status):
    users = status.get_users_subbed()
    status = status.status
    rounds = int(status.progress) - 4
    if rounds < 0:
        rounds = 1
    else:
        rounds = int(status.progress) - 3

    # print(rounds)
    for i in range(rounds):
        # print(i)
        print(status.print_json())
        message = f"""
{status.region_str} / {status.ladder_str} / {status.hc_str}
{status.progress_str}
"""
        bot.send_message("@DcloneWalkGroup", message)

        count = 0
        for user in users:
            bot.send_message(user, message)
            count += 1
            if count >= 30:
                time.sleep(1)
                count = 0


if __name__ == "__main__":
    try:
        bot.polling()
    except:
        traceback.print_exc()
