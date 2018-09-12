from telegram.ext import CommandHandler

from ..handlers import Handler


class DefaultHandler(Handler):

    def bind_handlers(self, dispatcher):
        dispatcher.add_handler(CommandHandler("help", self.help))

    def help(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id,
                         text="Для создания голосования введите /start")
