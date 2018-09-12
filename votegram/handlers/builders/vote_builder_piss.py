from ...handlers import (
    ModuleHandler,
    CallbackDataBuilderV1,
    CallbackDataParserV1,
)

from ..modules import (
    VoteConversationTimerHandler,
    VoteConvesationAnswersHandler,
)

from .core import VoteBuilderHandler


class VoteBuilderPissHandler(VoteBuilderHandler):
    """Собирает голосование против нехорошего пользователя

    Этапы:
    1. выбор времени истечения
    2. ввод имени пользователя

    TODO:
        1. Работает только в чате тет-а-тет
        2. Сделать упрощенную версию для чатов (аля /piss @user)
    """

    def __init__(self,
                 dispatcher):
        self._query_builder = CallbackDataBuilderV1()
        self._query_builder.set_salt(self.__class__.__name__)

        self._query_parser = CallbackDataParserV1()
        self._query_parser.set_salt(self.__class__.__name__)

        self._timer_handler = VoteConversationTimerHandler(
            dispatcher=dispatcher,
            query_builder=self._query_builder,
            query_parser=self._query_parser,
        )

        self._answers_handler = VoteConvesationAnswersHandler(
            dispatcher=dispatcher,
            query_builder=self._query_builder,
            query_parser=self._query_parser,
        )

        super().__init__(dispatcher)

    def bind_handlers(self, dispatcher):
        self._timer_handler.add_done_callback(self.timer_done)
        self._answers_handler.add_done_callback(self.answers_done)

    def start(self, bot, update):
        self._timer_handler.start(bot, update)

    def timer_done(self, bot, update, data):
        query = update.callback_query

        # TODO: естественно это не выводить надо, а запоминать
        bot.send_message(chat_id=query.message.chat_id,
                         text="Вы выбрали время {}".format(data))

        # запускаем операцию получения вариантов ответа от пользователя
        self._answers_handler.start(bot, update)

    def answers_done(self, bot, update, data):
        # TODO: естественно это не выводить надо, а запоминать
        text = "Вы ввели фразы:"
        for answer in data:
            text = text + "\n" + answer
        bot.send_message(chat_id=update.message.chat_id,
                         text=text)
