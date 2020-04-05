from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler
from telegram.ext import Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging
from fractions import Fraction

from poker import poker

pkr = poker()

# create and set the logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

# define the bot updater
my_token = '1129053883:AAH0i7EPiUsC90LeIKa_exii1df8hak_-VI'
updater = Updater(token=my_token, use_context=True)

# create the dispatcher locally
dispatcher = updater.dispatcher

def print_help(update, context):
    help_text = "Here is the list of possible commands.\n\
The structure is: /<command_name> - What the command does (who should invoke the command).\n\
        /help - Print this help.\n\
        /join - Join the game (player). Expects a player name (string).\n\
        /leave - Leave the game (player).\n\
        /startgame - Start the game once everyone joined (admin)\n\
        /givecards - Give next cards (dealer / admin)\n\
        /mycards - Reprint your cards (player).\n\
        /communitycards - Reprint community cards (player).\n\
        /bet - Place a bet (player). Expects a number (integer).\n\
        /getpot - Print the current pot.\n\
        /showdown - Print the showdown (dealer / admin). Expects the names (string) of players to participate.\n\
        /distributepot - Distribute the current pot to winners (dealer / admin). Expects player name (string) and player share (float, ratio).\n\
        /setstack - Set a players stack (dealer / admin). Expects a player name (string) and a new stack (integer).\n\
        /endhand - End the hand (dealer / admin).\n\
        /endgame - End the game (admin).\n\
        /start - Reprint startup message.\n\
        /getplayers - Print the player numbers, names, stacks.\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_text) #TODO: For a detailed explanation, please send /helpdetails.

help_handler = CommandHandler('help', print_help)
dispatcher.add_handler(help_handler)

# define the startup of the bot
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi, I'm the RTL+N Pokerstars poker bot!")
    print_help(update, context)
    context.bot.send_message(chat_id=update.effective_chat.id, text="If you are ever lost or searching for commands, send /help in the chat to reprint this command list!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def send_to_all(context, message):
    message_str = ""
    if isinstance(message, list):
        message_str = "".join(message)
    else:
        message_str = message
    for id in pkr.player_ids:
        context.bot.send_message(chat_id=id, text=message_str)

# joining and leaving
def join_game(update, context):
    # enhance player count by one, return player number
    context.bot.send_message(chat_id=update.effective_chat.id, text="Joining game...")
    if len(context.args) != 1:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Failed. Please provice a name without spaces.")
        return
    pkr.join_player(update.effective_chat.id, context.args[0])
    send_to_all(context, "{} has succesfully joined the game as player {}.".format(pkr.player_names[pkr.number_of_players-1], pkr.number_of_players-1))
    get_players(update, context, stack=False)

join_game_handler = CommandHandler('join', join_game)
dispatcher.add_handler(join_game_handler)

def leave_game(update, context):
    # decrease player count by one
    context.bot.send_message(chat_id=update.effective_chat.id, text="Leaving game...")
    pkr.remove_player(update.effective_chat.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Succesfully left game.")

leave_game_handler = CommandHandler('leave', leave_game)
dispatcher.add_handler(leave_game_handler)

def start_game(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Starting the game...")
    pkr.start_the_game()
    message = ["Game started with {} players.\n".format(pkr.number_of_players)]
    for player_order in pkr.player_order_blinds:
        message.append("{}: {}\n".format(player_order[0], player_order[1]))
    send_to_all(context, message)

start_game_handler = CommandHandler('startgame', start_game)
dispatcher.add_handler(start_game_handler)

def give_cards(update, context):
    # give cards according to at which state we are
    pkr.distribute_cards()
    for id in pkr.player_ids:
        message = ["Playing phase: {}.\n".format(pkr.phase_list[pkr.current_phase-1])]
        player_number = pkr.player_ids.index(id)
        message.append("The current pot is {}.\n".format(pkr.pot))
        message.append("The current stacks are as follows:\n")
        for player in range(pkr.number_of_players):
            message.append("    {}: {}\n".format(pkr.player_names[player], pkr.player_stacks[player]))
        the_cards = pkr.current_cards[player_number+1]
        card_string = " ".join(the_cards)
        message.append("Your cards are: {}".format(card_string))
        if pkr.current_phase != 1:
            the_cards = pkr.current_cards[0]
            card_string = " ".join(the_cards)
            message.append("\nCommunity cards are: {}".format(card_string))
        context.bot.send_message(chat_id=id, text="".join(message))
    context.bot.send_message(chat_id=update.effective_chat.id, text="Updated cards.")

give_cards_handler = CommandHandler('givecards', give_cards)
dispatcher.add_handler(give_cards_handler)

def getmycards(update, context):
    #give player cards according to player number
    player_number = pkr.player_ids.index(update.effective_chat.id)
    the_cards = pkr.current_cards[player_number+1]
    card_string = " ".join(the_cards)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Your cards are: {}".format(card_string))

get_my_cards_handler = CommandHandler('mycards', getmycards)
dispatcher.add_handler(get_my_cards_handler)

def get_community_cards(update, context):
    #give player cards according to player number
    the_cards = pkr.current_cards[0]
    card_string = " ".join(the_cards)
    if card_string == "":
        card_string = "No community cards yet."
    context.bot.send_message(chat_id=update.effective_chat.id, text="Community cards are: {}".format(card_string))

get_community_cards_handler = CommandHandler('communitycards', get_community_cards)
dispatcher.add_handler(get_community_cards_handler)

def place_bet(update, context):
    # bet a sum into the pot
    better_number = pkr.player_ids.index(update.effective_chat.id)
    amount = int(context.args[0])
    if amount > pkr.player_stacks[better_number]:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You cannot bet more than your total stack! Bet was: {}, but stack is only {}.".format(amount, pkr.player_stacks[better_number]))
        return
    pkr.place_a_bet(update.effective_chat.id, amount)
    send_to_all(context, "{} (Player {}) has bet {}.".format(pkr.player_names[better_number], better_number, amount))

place_bet_handler = CommandHandler('bet', place_bet)
dispatcher.add_handler(place_bet_handler)

def showdown(update, context):
    message = list()
    players = context.args
    if "all" in players or "All" in players:
        players = pkr.player_names
    if len(players) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please specify players to participate in the showdown!")
        return
    for player in players:
        message.append("{}: {}\n".format(player, "".join(pkr.current_cards[pkr.player_names.index(player)+1])))
    message.append("Community cards: {}".format("".join(pkr.current_cards[0])))
    send_to_all(context, message)

showdown_handler = CommandHandler('showdown', showdown)
dispatcher.add_handler(showdown_handler)

def end_hand(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Resetting phase to \"Austeilen\".")
    pkr.end_the_hand()
    context.bot.send_message(chat_id=update.effective_chat.id, text="Done.")

end_hand_handler = CommandHandler('endhand', end_hand)
dispatcher.add_handler(end_hand_handler)

def end_game(update, context):
    send_to_all(context, "Ending the game. Thanks for playing!")
    pkr.end_the_game()
    context.bot.send_message(chat_id=update.effective_chat.id, text="Done.")

end_game_handler = CommandHandler('endgame', end_game)
dispatcher.add_handler(end_game_handler)

def get_players(update, context, stack=True):
    message = list()
    if not stack:
        message.append("Currently connected:\n")
    for player in range(pkr.number_of_players):
        if stack:
            message.append("Player {}: {}, stack {}\n".format(player, pkr.player_names[player], pkr.player_stacks[player]))
        else:
            message.append("Player {}: {}\n".format(player, pkr.player_names[player]))
    context.bot.send_message(chat_id=update.effective_chat.id, text="".join(message))

get_players_handler = CommandHandler('getplayers', get_players)
dispatcher.add_handler(get_players_handler)

def get_pot(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Current pot is {}.".format(pkr.pot))

get_pot_handler = CommandHandler('getpot', get_pot)
dispatcher.add_handler(get_pot_handler)

def distribute_pot(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Distributing pot of {}...".format(pkr.pot))
    if len(context.args) % 2 != 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Odd number of arguments. #arguments should be even! Please adapt input.")
        return
    names = context.args[::2]
    shares = [float(Fraction(frac)) for frac in context.args[1::2]]
    player_shares = [(names[i], shares[i]) for i,tmp in enumerate(names)]
    pot = pkr.distribute_the_pot(player_shares)
    message = ["Pot of {} distributed. New stacks are as follows:\n".format(pot)]
    for player_number, player in enumerate(pkr.player_names):
        message.append("Player {}: {}, stack {}\n".format(player_number, player, pkr.player_stacks[player_number]))
    send_to_all(context, message)

distribute_pot_handler = CommandHandler('distributepot', distribute_pot)
dispatcher.add_handler(distribute_pot_handler)

def set_stack(update, context):
    player, new_stack = context.args
    pkr.set_the_stack(player, new_stack)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Set stack of {} to {}.".format(player, new_stack))

set_stack_handler = CommandHandler('setstack', set_stack)
dispatcher.add_handler(set_stack_handler)

print("Succesfully started bot. Waiting for updates.")

updater.start_polling()
updater.idle()
