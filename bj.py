import display
import os
import time


class Card():
    # Class Card: one card with rank, suite, number and point
    def __init__(self, suite, number):
        """
        :param self: one card with rank, suite and point
        :param suite: int num 0-3
        :param number: int num [0, 1, ..., 9, 10, 11, 12], representing
                             [A, 2, ..., 10, J, Q, K]
        :return: 
        self.number: int num, input rank number
        self.rank: str in [A, 2, ..., 10, J, Q, K]
        self.suite: int in 0-3 representing [club, diamonds, hearts, spades]
        self.point: int num, points represented by the card
        """
        self.number = number
        self.suite = suite

        if number in range(1, 9):
            self.rank = ' ' + str(number + 1)
            self.point = number + 1
        elif number == 9:
            self.rank = str(number + 1)
            self.point = number + 1
        elif number == 0:
            self.rank = ' ' + 'A'
            self.point = 11  # could be 1 or 11 points, set default as 11 point
        elif number == 10:
            self.rank = ' ' + 'J'
            self.point = 10
        elif number == 11:
            self.rank = ' ' + 'Q'
            self.point = 10
        elif number == 12:
            self.rank = ' ' + 'K'
            self.point = 10

    def __str__(self):
        if self.suite == 0:
            print_suite = 'club'
        elif self.suite == 1:
            print_suite = 'diamonds'
        elif self.suite == 2:
            print_suite = 'hearts'
        elif self.suite == 3:
            print_suite = 'spades'
        return '{}_{}'.format(print_suite, self.rank)


class Deck():
    # Class Deck: cards available to be drawn from
    def __init__(self):
        """        
        :param self: cards available to be drawn from
        :return: 
        self.available_cards: list of int (value between 0-51)
        # The number in the list represents the card as below:
        #  0-12 club
        # 13-25 diamonds
        # 26-38 hearts
        # 39-51 spades
        # Each suite consists of 13 ranks:
        # A, 2, ..., 10, J, Q, K       
        """
        self.available_cards = list(range(52))

    def __str__(self):
        club = ['club   ']
        diamonds = ['diamond']
        hearts = ['hearts ']
        spades = ['spades ']
        for index in range(0, len(self.available_cards)):
            card_number = self.available_cards[index]
            card = self.convert_number_to_card(card_number)
            if card.suite == 0:
                club.append(card.rank)
            elif card.suite == 1:
                diamonds.append(card.rank)
            elif card.suite == 2:
                hearts.append(card.rank)
            else:
                spades.append(card.rank)
        return 'Current Deck: \n' + \
               str(club) + '\n' + \
               str(diamonds) + '\n' + \
               str(hearts) + '\n' + \
               str(spades)

    def convert_number_to_card(self, number_in_deck):
        suite = number_in_deck // 13
        number = number_in_deck % 13
        return Card(suite, number)

    def convert_card_to_number(self, card):
        return card.suite * 13 + card.number

    def deal_new_card(self, *num):
        # Draw a new card from the deck
        # Output: card object
        import random
        # generate a random value between 0 to (number of cards in the deck -1)
        draw_index = random.randint(0, len(self.available_cards) - 1)
        if num != ():
            number_in_deck = num  # for debug
        else:
            number_in_deck = self.available_cards.pop(draw_index)
        # print('number_in_deck: {}'.format(number_in_deck))  # for debug
        return self.convert_number_to_card(number_in_deck)

    def show_one_card(self, onecard):
        # Input: int between 0-51 representing a card
        suite = (onecard) // 13
        rank = onecard % 13
        print(Card(rank, suite))
        return Card(rank, suite)


class Player():
    # Class Player: player's info
    def __init__(self):
        '''
        create a player class, with a bankroll of $1000.
        '''
        self.name = 'Player: '
        self.cards = list()
        self.point = 0
        self.account = 1000
        self.bet = 50

    def __str__(self):
        return 'You have ${} in your account'.format(self.bankrool)

    def start_new_game(self):
        self.cards = list()
        self.point = 0

    def get_a_card_from_deck(self, deck, *num):
        # print(deck)
        if num != ():
            card = deck.deal_new_card(num)  # for debug
        else:
            card = deck.deal_new_card()
        self.cards.append(card)
        # print(deck)

    def check_cards(self):
        numofcards = len(self.cards)
        if numofcards == 0:
            print("You don't have any card")
        else:
            print('{} have {} cards:'.format(self.name, numofcards))
            for idx in range(numofcards):
                print('    {}'.format(self.cards[idx]))

    def get_points(self):
        self.point = 0
        num_of_A_substracted = 0
        for idx in range(len(self.cards)):
            self.point += self.cards[idx].point
            if self.cards[idx].rank == ' A':
                num_of_A_substracted += 1
            while self.point > 21 and num_of_A_substracted > 0:
                self.point -= 10
                num_of_A_substracted -= 1

        # print(self.point)
        return self.point

    def check_busted(self):
        points = self.get_points()
        if points > 21:
            return True
        else:
            return False

    def check_out(self, game_result, bet):
        if game_result == 'win':
            self.account += 2*bet
        elif game_result == 'lose':
            pass
        else: # game_result == 'tie'
            self.account += bet
        print("Your account: ${}".format(self.account))

    def place_bets(self):
        print("Your account balance is: ${}".format(self.account))
        try:
            bet = int(input("Please place your bet (default $50): "))
        except ValueError:
            bet = 50

        while bet > self.account or bet == 0:
            if bet > self.account:
                print("You don't have enough balance.")
            elif bet == 0:
                print("Please enter a valid bet.")
            print("Your account balance is: ${}".format(self.account))
            try:
                bet = int(input("Please place your bet (default $50): "))
            except ValueError:
                bet = 50

        self.bet = bet
        self.account -= bet

    def deposit(self):
        if not display.get_y_or_n("You have ZERO balance.  Deposit money to your account?"):
            return False
        else:
            # TODO: need to check input type
            deposit_amount = int(input("Input the amount to deposit: $"))
            self.account += deposit_amount
            return True



class Dealer(Player):
    # Class Dealer: an class inherited from class Player.
    def __init__(self):
        Player.__init__(self)
        self.name = 'Dealer: '

    def draw_cards_against_player(self, drawing_deck, one_player):
        display.display_game(self, one_player)
        # os.system('clear')
        # display.display_play_cards(self)
        # display.display_play_cards(one_player)
        dealer_points = self.get_points()
        while dealer_points < 17:
            self.get_a_card_from_deck(drawing_deck)
            time.sleep(1)
            display.display_game(self, one_player)
            # os.system('clear')
            # display.display_play_cards(self)
            # display.display_play_cards(one_player)
            dealer_points = self.get_points()


if __name__ == "__main__":
    deck = Deck()
    # for i in range(5):
    #     print('draw card {}'.format(i+1))
    #     first_card = deck.deal_new_card()
    #     print(first_card)
    #     print(deck.convert_card_to_number(first_card))
    #     print(deck)
    #     print(deck.available_cards)
    player = Player()
    dealer = Dealer()

    print('Deal 1st card for player')
    num = int(input("draw card number: "))
    player.get_a_card_from_deck(deck, num)
    player.check_cards()
    display.display_play_cards(player)
    print(player.get_points())
    # print('Deal 1st card for dealer')
    # dealer.get_a_card_from_deck(deck)
    # dealer.check_cards()

    print('Deal 2nd card for player')
    num = int(input("draw card number: "))
    player.get_a_card_from_deck(deck, num)
    player.check_cards()
    display.display_play_cards(player)
    print(player.get_points())
    # print('Deal 2nd card for dealer')
    # dealer.get_a_card_from_deck(deck)
    # dealer.check_cards()

    print('Deal 3rd card for player')
    num = int(input("draw card number: "))
    player.get_a_card_from_deck(deck, num)
    player.check_cards()
    display.display_play_cards(player)
    print(player.get_points())

    print('Deal 4th card for player')
    num = int(input("draw card number: "))
    player.get_a_card_from_deck(deck, num)
    player.check_cards()
    display.display_play_cards(player)
    print(player.get_points())

    print('Deal 4th card for player')
    num = int(input("draw card number: "))
    player.get_a_card_from_deck(deck, num)
    player.check_cards()
    display.display_play_cards(player)
    print(player.get_points())
