import bj
import display
import os

if __name__ == "__main__":
    os.system('clear')
    print("Welcome to Black Jack Game!")
    # create a player and a dealer
    player = bj.Player()
    dealer = bj.Dealer()

    game_status = True
    while game_status:
        while player.account == 0 and game_status:
            if not player.deposit():
                print("You choose not to deposit.")
                if display.get_y_or_n("Quit the game? "):
                    game_status = False

        if not game_status:
            break

        player.start_new_game()
        dealer.start_new_game()

        # Shuffle cards - create a new deck
        deck = bj.Deck()
        game_result = ''
        player.place_bets()
        os.system('clear')

        # Deal 1st card to player and dealer
        player.get_a_card_from_deck(deck)
        dealer.get_a_card_from_deck(deck)
        # Deal 2nd card to player and dealer
        player.get_a_card_from_deck(deck)
        dealer.get_a_card_from_deck(deck)
        # display.display_play_cards(dealer, 'hide')
        # display.display_play_cards(player)
        display.display_game(dealer, player, 'hide')
        # TODO: auto stand if point reach 21
        player_continue_deal = display.get_player_decision(player)
        while player_continue_deal:
            player.get_a_card_from_deck(deck)
            # os.system('clear')
            # display.display_play_cards(dealer, 'hide')
            # display.display_play_cards(player)
            display.display_game(dealer, player, 'hide')
            player_busted = player.check_busted()
            if player_busted:
                print("You busted.")
                game_result = 'lose'
                break
            else:
                player_continue_deal = display.get_player_decision(player)
        if game_result != 'lose':
            dealer.draw_cards_against_player(deck, player)
            if dealer.check_busted():
                print("Dealer busted.  You win!")
                game_result = 'win'
            else:
                player_point = player.get_points()
                print("Your points: {}".format(player_point))
                dealer_point = dealer.get_points()
                print("Dealer points: {}".format(dealer_point))
                if player_point < dealer_point:
                    print("You lose.")
                    game_result = 'lose'
                elif player_point > dealer_point:
                    print("You win!")
                    game_result = 'win'
                else:
                    print("Tie.")
                    game_result = 'tie'
        player.check_out(game_result, player.bet)

        game_status = display.start_new_game()


