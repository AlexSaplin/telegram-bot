import telebot

from src import stats_interface

bot = telebot.TeleBot("870911582:AAHW2BU6RPCdjw-llq7kzit7Tn6RAndLoGY")


@bot.message_handler(func=lambda message: message.text.startswith('/player_'), content_types=['text'])
def get_player(message):
    player_id = int(message.text.split('_')[1])
    player_info = stats_interface.get_player(player_id)['people'][0]
    result = "Full Name: {}\n" \
             "Jersey number : {}\n" \
             "Birth date: {}\n" \
             "Age: {}\n" \
             "Birth country: {}\n" \
             "Birth city: {}\n" \
             "Nationality: {}\n" \
             "Height: {}\n" \
             "Weight: {} lbs\n" \
             "Hand: {}\n" \
             "Team: {}\n" \
             "Position: {}\n".format(player_info.get('fullName'),
                                     player_info.get('primaryNumber'),
                                     player_info.get('birthDate'),
                                     player_info.get('currentAge'),
                                     player_info.get('birthCity'),
                                     player_info.get('birthCountry'),
                                     player_info.get('nationality'),
                                     player_info.get('height'),
                                     player_info.get('weight'),
                                     player_info.get('shootsCatches'),
                                     player_info.get('currentTeam', {}).get('name'),
                                     player_info.get('primaryPosition', {}).get('abbreviation'))
    bot.reply_to(message, result)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.reply_to(message, 'Hello')
