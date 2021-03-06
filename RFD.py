from .. import loader, utils

import logging, time

from telethon import types

logger = logging.getLogger(__name__)

@loader.tds
class rretMod(loader.Module):
    """Отправляет ответное сообщение при отправки сообщения Вам."""
    strings = {"name": "RFD",
               "gone": "Режим автоответчика включён",
               "back": "Режим автоответчика включён",
               "rret": "<b>Не стоит мне писать.</b>",
               "rret_reason": "{}"}

    async def client_ready(self, client, db):
        self._db = db
        self._me = await client.get_me()
        self.client = client

    async def rfdcmd(self, message):
        """.rfd [текст]"""
        reply = await message.get_reply_message()
        if reply:
            self._db.set(__name__, "rret", f"{reply.chat_id}|{reply.id}")
        else:
            await utils.answer(message, "Нет реплая")
            return
        self._db.set(__name__, "gone", time.time())
        await self.allmodules.log("rret", data=utils.get_args_raw(message) or None)
        await message.edit(self.strings("gone", message))

    async def unrfdcmd(self, message):
        """Перестаёт отвечать на чужие сообщении, при Вашем упоминании"""
        self._db.set(__name__, "rret", False)
        self._db.set(__name__, "gone", None)
        await self.allmodules.log("unrret")
        await message.edit(self.strings("back", message))

    async def watcher(self, message):
        if not isinstance(message, types.Message):
            return
        if message.mentioned or getattr(message.to_id, "user_id", None) == self._me.id:
            if self.get_rret() != False:
                rret_state = self.get_rret()
                chat = int(rret_state.split("|")[0])
                id = int(rret_state.split("|")[1])
                rret = await self.client.get_messages(chat, ids=id)
                await self.client.send_message(message.to_id, rret, reply_to=message)


    def get_rret(self):
        return self._db.get(__name__, "rret", False)
