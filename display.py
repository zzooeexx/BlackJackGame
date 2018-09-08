import os

def card_shape(*card):
    # Convert a card to a list of 3 strings representing the shape such as:
    # ˌ---ˌ
    # |♣ 8|
    # ˈ---ˈ
    line1 = (u'\u02CC' + "---" + u'\u02CC')
    line3 = (u'\u02C8' + "---" + u'\u02C8')
    if card != ():
        card = card[0]
        if card.suite == 0:
            # club
            line2 = ("|" + u'\u2663' + card.rank + '|')
        elif card.suite == 1:
            # diamonds
            line2 = ("|" + u'\u2666' + card.rank + '|')
        elif card.suite == 2:
            # hearts
            line2 = ("|" + u'\u2665' + card.rank + '|')
        elif card.suite == 3:
            # spades
            line2 = ("|" + u'\u2660' + card.rank + '|')
    else:
        line2 = ("|" + "   " + '|')
    return [line1, line2, line3]


def display_play_cards(player, *hide_first_card):
    '''
    :param player:
    :param hide_first_card: if not empty, first card will not display
    :return:
    '''
    card_line1 = '        '
    card_line2 = player.name
    card_line3 = '        '
    for card_idx in range(len(player.cards)):
        if hide_first_card and card_idx == 0:
            cardlines = card_shape()
        else:
            cardlines = card_shape(player.cards[card_idx])
        card_line1 += cardlines[0]
        card_line2 += cardlines[1]
        card_line3 += cardlines[2]
    print(card_line1)
    print(card_line2)
    print(card_line3)


def display_game(dealer, player, *hide_first_card):
    os.system('clear')
    print("Your accout: {}; Your bet: {}".format(player.account,player.bet))
    if hide_first_card:
        display_play_cards(dealer, hide_first_card)
    else:
        display_play_cards(dealer)
    display_play_cards(player)


def get_player_decision(player):
    if player.get_points() == 21:
        continue_deal = False
    else:
        player_decision = input("Hit or Stand? (h/s) ")
        player_decision = player_decision.lower()
        incorrect_input = (player_decision != 'h') and (player_decision != 's')
        while incorrect_input:
            print("Wrong input!  Please enter 'h' or 's' ")
            player_decision = input("Hit or Stand? (h/s) ")
            player_decision = player_decision.lower()
            incorrect_input = (player_decision != 'h') and (player_decision != 's')
        if player_decision.lower() == 'h':
            continue_deal = True
        elif player_decision.lower() == 's':
            continue_deal = False

    return continue_deal


def get_y_or_n(string):
    s = input(string + " (y/n) ")
    if s.lower() == 'y' or s == "":
        return True
    elif s.lower() == 'n':
        return False
    else:
        print("Please input 'y' or 'n'.")
        return get_y_or_n(string)


def start_new_game():
    return get_y_or_n("Start a new game?")

