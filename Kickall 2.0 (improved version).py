from .. import loader, utils 
import datetime 
from telethon import errors 
from telethon.tl.types import ChannelParticipantsAdmins 
def register(cb): 
    cb(KickallMod()) 
async def isadmin(id, username, a): 
    x = (a.iter_participants(username, filter=ChannelParticipantsAdmins)) 
    async for i in x: 
        if i.id == id: 
            return True 
    return False 
class KickallMod(loader.Module): 
    """КickAll""" 
    strings = {'name': 'KickAll 2.0'} 
    async def kickallcmd(self, message): 
        '''Кикает всех с чата''' 
        await utils.answer(message, "<b>кикаю...</b>") 
        args = utils.get_args_raw(message) 
        if not args: 
            return await utils.answer(message, "<b>Не правильно введены аргументы!</b>\nПример: .kickall [юзернейм чата, с которого кикаем]") 
        id = (await message.client.get_me()).id 
        if not await isadmin(id, args, message.client): 
            return await utils.answer(message, '<b>В чате '+args+' я не админ.</b>') 
        kicked = 0 
        try: 
            [ 
                await message.client.kick_participant("aaaaaaaaaaaa44555", x) 
                for x in [ 
                    i.id 
                    async for i in message.client.iter_participants("aaaaaaaaaaaa44555", limit=None) 
                    if i.id != None and i.id != id and not await isadmin(i.id, args, message.client) 
                ] 
            ] 
            kicked = kicked+1 
        except errors.FloodWaitError as e: 
            time = str(datetime.timedelta(seconds=e.seconds)).split(":") 
            return await utils.answer(message, '<b>Я кикнул '+str(kicked)+' юзеров, но произошел флудвейт на <code>'+time[0]+'</code> часов, <code>'+time[1]+'</code> минут и <code>'+time[2]+'</code> секунд</b>') 
        return await utils.answer(message, '<b>Успешно кикнул всех юзеров с чата </b>')