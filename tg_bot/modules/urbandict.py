import asyncio, re, aiohttp

from telegram import Message, Update, Bot, User
from telegram.ext import Filters, MessageHandler, run_async
from tg_bot import dispatcher
from tg_bot.modules.disable import DisableAbleCommandHandler
from typing import List


QUERY_URL = 'http://api.urbandictionary.com/v0/define'
RANDOM_URL = 'http://api.urbandictionary.com/v0/random'


@run_async
def urbandict(bot: Bot, update: Update, args: List[str]):
    if len(args) >= 1:
        udquery = ' '.join(args)
    else:
        udquery = None

    loop = asyncio.new_event_loop()
    definition = loop.run_until_complete(get_def(loop, udquery))
    loop.close()

    update.effective_message.reply_text(definition)


async def get_def(loop, udquery):
    if udquery:
        params = {'term': udquery}
        url = QUERY_URL
    else:
        params = None
        url = RANDOM_URL
    
    session = aiohttp.ClientSession(loop=loop)

    async with session.get(url, params=params) as response:
        if response.status == 200:
            response = await response.json()
        else:
            response = response.status
        
    await session.close()

    try:
        response = response['list'][0]
        wordinfo = [response['word'], response['definition']]
        if response['example'] != '':
            wordinfo.append(response['example'])
    except NameError:
        wordinfo = ["An error occurred, response code:", str(response)]
    except IndexError:
        wordinfo = ['No results for query', udquery]

    definition = '{0[0]}: {0[1]}'.format(wordinfo)

    try:
        definition += '\n\nExample: {0[2]}'.format(wordinfo)
    except IndexError:
        pass

    definition = re.sub(r'[[]', '', definition)
    definition = re.sub(r'[]]', '', definition)

    return definition


__help__ = """
 Heckin UD
"""

__mod_name__ = "Urban Dictionary"

URBANDICT_HANDLER = DisableAbleCommandHandler("ud", urbandict, admin_ok=True, pass_args=True)
dispatcher.add_handler(URBANDICT_HANDLER)
