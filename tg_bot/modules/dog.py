import asyncio, re, aiohttp

from telegram import Message, Update, Bot, User
from telegram.ext import Filters, MessageHandler, run_async
from tg_bot import dispatcher, DOG_API_KEY
from tg_bot.modules.disable import DisableAbleCommandHandler
from typing import List


DOG_URL = 'http://api.thedogapi.com/v1/images/search'


class dogapi():
    def __init__(self, loop):
        headers = {"x-api-key": DOG_API_KEY}
        self.params = {"mime_types": "jpg,png"}
        self.session = aiohttp.ClientSession(loop=loop, headers=headers)

    async def _get(self):
        async with self.session.get(DOG_URL, params=self.params) as response:
            if response.status == 200:
                response = await response.json()
            else:
                raise Exception

        return response

    async def getdog(self):
        dog = await self._get()
        return dog

    async def close(self):
        await self.session.close()


async def inuatsume(loop):
    doghouse = dogapi(loop)
    dog = await doghouse.getdog()
    await doghouse.close()
    return dog


@run_async
def dog(bot: Bot, update: Update):
    loop = asyncio.new_event_loop()
    dog = loop.run_until_complete(inuatsume(loop))
    loop.close()
    update.effective_message.reply_photo(dog[0]["url"])


@run_async
def doghd(bot: Bot, update: Update):
    loop = asyncio.new_event_loop()
    dog = loop.run_until_complete(inuatsume(loop))
    loop.close()
    update.effective_message.reply_document(dog[0]["url"])


__help__ = """
 Get Dog
"""

__mod_name__ = "Dog"

if (DOG_API_KEY != None):
    DOG_HANDLER = DisableAbleCommandHandler("dog", dog, admin_ok=True, pass_args=False)
    DOGHD_HANDLER = DisableAbleCommandHandler("doghd", doghd, admin_ok=True, pass_args=False)
    dispatcher.add_handler(DOG_HANDLER)
    dispatcher.add_handler(DOGHD_HANDLER)
