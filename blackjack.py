import random
import os
#TODO: Make deal card a function
class Blackjack():

    def __init__(self):
        self.dealer = []
        self.player = []
        self.standing = False
        self.first_hand = True
        self.game_over = False
        self.cards = [
        '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
        '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
        '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
        '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
        ]

    def calc_hand(self, hand):
        sum = 0
        non_aces = [card for card in hand if card != 'A']
        aces = [card for card in hand if card == 'A']
        for card in non_aces:
            if card in 'JQK':
                sum += 10
            else:
                sum += int(card)
        for card in aces:
            if sum <= 10:
                sum += 11
            else:
                sum += 1
        return sum

    def deal_next_card(self, to):
        to.append(self.cards.pop())

    def deal_two_cards(self):
        for iterations in range(2):
            self.deal_next_card(self.player)
            self.deal_next_card(self.dealer)

    def reset_hand(self):
        self.player.clear()
        self.dealer.clear()
        self.deal_two_cards()
        self.first_hand = True
        self.standing = False
        self.game_over = False
    
    def play(self):
        random.shuffle(self.cards)
        self.deal_two_cards()
        for iterations in range(5):

            while not self.game_over:
                os.system('cls')
                player_score = self.calc_hand(self.player)
                dealer_score = self.calc_hand(self.dealer)

                #If player stands, show all dealer cards
                if self.standing:
                    print('Dealer Cards: [{}]({})'.format(']['.join(self.dealer), dealer_score))
                #else, show just the dealer's first card
                else:
                    print('Dealer Cards: [{}][?]'.format(self.dealer[0]))

                print('Your Cards: [{}]({})'.format(']['.join(self.player), player_score))
                print('')

                if self.standing:
                    if dealer_score > 21:
                        print('Dealer Busted; You win')
                        print('')
                        if iterations < 4:
                            input("Start a new game")
                        self.game_over = True
                    elif player_score == dealer_score:
                        print('Push')
                        print('')
                        if iterations < 4:
                            input("Start a new game")
                        self.game_over = True
                    #if the player has stood, then they must have a valid hand
                    elif player_score > dealer_score:
                        print('You win')
                        print('')
                        if iterations < 4:
                            input("Start a new game")
                        self.game_over = True
                    else:
                        print('You lost')
                        print('')
                        if iterations < 4:
                            input("Start a new game")
                        self.game_over = True
                    break
                
                if self.first_hand and player_score == 21:
                    print('Blackjack; You win')
                    print('')
                    if iterations < 4:
                        input("Start a new game")
                    self.game_over = True
                    break

                if player_score > 21:
                    print('You bust; You lose')
                    print('')
                    if iterations < 4:
                        input("Start a new game")
                    self.game_over = True
                    break

                print('What would you like to do?')
                print(' [1] Hit')
                print(' [2] Stand')
                print('')

                choice = input('Your Choice: ')
                print('')

                if choice == '1':
                    self.first_hand = False
                    self.deal_next_card(self.player)
                elif choice == '2':
                    # os.system('cls')
                    self.standing = True
                    while self.calc_hand(self.dealer) <= 16:
                        self.deal_next_card(self.dealer)
                else:
                    pass

            if self.game_over:
                self.reset_hand()

def main():
    game = Blackjack()
    game.play()

if __name__ == "__main__":
    main()
