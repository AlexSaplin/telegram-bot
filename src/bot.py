import telebot

from src import stats_interface
from src.config import TELEGRAM_TOKEN

bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(func=lambda message: message.text.startswith('/player_'), content_types=['text'])
def get_player(message):
    player_id = int(message.text.split('_')[1])
    player_info = stats_interface.get_player(player_id)
    bot.reply_to(message, str(player_info))


@bot.message_handler(commands=['find_player'])
def find_player_by_name(message):
    bot.reply_to(message, 'Enter player name')
    bot.register_next_step_handler(message, process_enter_player_name)


def process_enter_player_name(message):
    try:
        player_name = message.text
        player_info = stats_interface.get_player_by_name(player_name)
        bot.reply_to(message, str(player_info))
    except Exception as e:
        bot.reply_to(message, 'There is no player with such name, try again')


@bot.message_handler(commands=['get_player_stats'])
def get_player_stats(message):
    bot.reply_to(message, 'Enter player name and season begging year')
    bot.register_next_step_handler(message, process_enter_info_for_stats)


def process_enter_info_for_stats(message):
    try:
        info = message.text.rsplit(' ', -1)
        player_name = info[0]
        season = int(info[1])
        bot.reply_to(message, stats_interface.get_player_stats(player_name, season))
    except Exception as e:
        bot.reply_to(message, 'I cannot understand you')


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.reply_to(message, 'Hello')


@bot.message_handler(func=lambda message: True)
def handle_trash_messages(message):
    bot.reply_to(message, 'I can\'t understand you')
