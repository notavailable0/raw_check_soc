import asyncio
from typing import Union

import telethon
from telethon.sessions import Session

# Макс. кол-во одновременно подключенных аккаунтов.
CONCURRENCY_LIMIT = 5
# Список путей до сесссий
ALL_SESSIONS_PATHS = [
    "+79995144039.session",
    "+79995119293.session",
    "+79295319093.session",
]
PROXY = None

semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)


async def start_accounts(sessions_paths):
    corors = [work_with_account(path) for path in sessions_paths]
    await asyncio.gather(*corors)


async def work_with_account(session_path: str):
    async with semaphore:
        client = make_client(session_path)
        # Если нужно отсеивать неавторизованные аккаунты, то требуется заменить start() на более подходящие методы.
        await client.start()
        print(f"Аккаунт {session_path} готов к работе.")

        entity = await client.get_entity("https://t.me/TelethonRussian")
        print(f"{session_path} -> {entity}")


def make_client(session: Union[str, Session]) -> telethon.TelegramClient:
    return telethon.TelegramClient(
            session,
            api_id=2040,
            api_hash="b18441a1ff607e10a989891a5462e627",
            device_model="PC 64bit",
            system_version="Windows 7",
            app_version="1.9.1",
            lang_code="en",
            system_lang_code="en-US",
            proxy=PROXY
    )


if __name__ == '__main__':
    asyncio.run(start_accounts(ALL_SESSIONS_PATHS))
