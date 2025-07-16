import asyncio

from src.bot.bot_main import main
# from src.app.services import chat_gpt_request
# from src.bot.serviсes.test import test_get_wictionary_word
# from src.bot.serviсes.wictionary import get_wictionary_word

# async def main():
#     data = await test_get_wictionary_word()
#     print(data)

if __name__ == '__main__':
    asyncio.run(main())

    # print(chat_gpt_request())
