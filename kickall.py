from .. import loader, utils 


def register(cb):
	cb(KickAllMod())

class KickAllMod(loader.Module):
	"""Ломает чаты."""
	strings = {'name': 'KickAll'}

	async def kickallcmd(self, message):
		"""Что блять не понятного? Используй .kickall <s>, чтобы кикнуть всех с чата."""
		args = utils.get_args_raw(message) 
		silent = False
		if 's' in args: 
			silent = True
			await message.delete()
		else: await message.edit('Молитесь за чат')
		users = await message.client.get_participants(message.chat_id,aggressive=True)
		count = 0
		for user in users:
			try:
				if user.id != message.from_id:
					await message.client.kick_participant(message.chat_id, user.id)
					count += 1
			except: pass
		if silent == True:
			chat = await message.client.get_entity(message.to_id) 
			await message.client.send_message('me', f'<b>В чате "{chat.title}" кикнуто {count} пользователей.</b>')
		else: await message.edit(f'<b>Кикнуто {count} пользователей.</b>') 