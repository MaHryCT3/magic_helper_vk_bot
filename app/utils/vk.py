from vkbottle import API

from app import models


async def send_message(vk_api: API, message: str, chat_id: int, *args: str) -> None:
    await vk_api.messages.send(
        message=message, peer_id=chat_id, random_id=0, dont_parse_links=True, *args
    )


async def get_user(vk_api: API, user_id: int, *args: str) -> models.VKUser:
    user_data = await vk_api.users.get(user_id=user_id, *args)
    return models.VKUser(
        id_=user_id,
        name=user_data[0].first_name,
        surname=user_data[0].last_name,
    )
