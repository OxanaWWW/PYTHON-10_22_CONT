from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message
from random import shuffle, randint
from aiogram import executor
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from loguru import logger

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)
logger.add('log_info.log',
           format="{time} - {level} - {message}",
           level='DEBUG')

all_amount = 120
max_sweet = 28
players = ''
aktiv_player = ''


@dp.message_handler(Command('start'))
async def show_butten(message: Message):
    logger.debug('\ngame start')
    await message.answer('play with \n'
                         'b - bot-human \n'
                         'k - kid-human \n')


@dp.message_handler(Text(equals=['b', 'k']))
async def exo_funct(message: Message):
    global players
    global aktiv_player
    a = 1 if message.text == 'k' else 0  # logik ternar operator
    players = ['person', 'kid' if a else 'bot']
    shuffle(players)
    aktiv_player = players[0]
    await message.answer(f'fierst in game {players[0]},second in game {players[1]}')
    await message.answer('lets game \n'
                         'y - yes \n'
                         'n - no \n')


@dp.message_handler(Text(equals=['n']))
async def stope_game(message: Message):
    logger.debug('game finished')
    await message.answer(f'good bye ')
    dp.stop_polling()
    await dp.wait_closed()
    await bot.close_bot()


def game_bot():
    result = all_amount % 29
    if not result:
        result = randint(1, 28)
    return result


def all_game(s):
    f_1, f_2 = players
    return f_2 if s == f_1 else f_1


def step_game(sweets):
    global all_amount
    all_amount -= sweets


@dp.message_handler(Text(equals=[*range(1, 29), 'y']))
async def main_game(message: Message):
    global all_amount, aktiv_player

    if message.text.isdigit():
        x = int(message.text)
        logger.debug(f' take sweet  {x}')
        step_game(x)
    if all_amount > 0:
        await message.answer(f'all sweet {all_amount} and limit {max_sweet} ')

        if aktiv_player == 'bot':
            await message.answer(f' take sweet  {aktiv_player}')

            x = game_bot()
            logger.debug(f'move {aktiv_player} take sweet  {x}')
            all_amount -= x
            await message.answer(f'bot take {x} all sweet {all_amount}')
            if all_amount > 0:
                aktiv_player = all_game(aktiv_player)
                logger.debug(f'move {aktiv_player}')
                await message.answer(f' take sweet  {aktiv_player}')
                await message.answer(' how many sweets are you want')
                aktiv_player = all_game(aktiv_player)
            else:
                await message.answer(f' you winner {aktiv_player}')
                logger.debug(f'winner {aktiv_player}\n')
                all_amount = 120
        else:
            await message.answer(f' take sweet  {aktiv_player}')
            logger.debug(f'move {aktiv_player}')
            await message.answer(' how many sweets are you want')
            aktiv_player = all_game(aktiv_player)

    else:
        aktiv_player = all_game(aktiv_player)
        logger.debug(f'winner {aktiv_player}')
        await message.answer(f' you winner {aktiv_player}\n')
        all_amount = 120


@dp.message_handler()
async def choice_sweet(message: Message):
    logger.debug('incorrect data')
    await message.answer(f'{message.from_user.first_name} enter correct data')


executor.start_polling(dp)
