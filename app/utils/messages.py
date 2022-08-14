from vkbottle import API


async def send(vk_api: API, message: str, chat_id: int, *args):
    await vk_api.messages.send(message=message, peer_id=chat_id, random_id=0, *args)
