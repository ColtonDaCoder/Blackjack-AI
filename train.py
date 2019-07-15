import random
import neat

class Blackjack():

    def __init__(self):
        self.dealer = []
        self.player = []
        self.standing = False
        self.first_hand = True
        self.round_over = False
        self.cards = [
        '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
        '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
        '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
        '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
        ]
        self.outcomes = []
        self.fitness = 0
        self.game_over = False
        self.bot_input = 2
        self.discard = []
        random.shuffle(self.cards)
        self.deal_two_cards()

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
        card = self.cards.pop()
        to.append(card)
        self.discard.append(card)

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
        self.round_over = False

    def assign_card_number(self, card):
        if card == 'J' or card == 'Q' or card == 'K':
            return 10
        elif card == 'A':
            return 11
        else:
            return int(card)
            
    def check_deck(self):
        if len(self.cards) < 10:
            self.cards.extend(self.discard)
            random.shuffle(self.cards)

    def output_info(self):
        outputs = []
        dealer_card = self.assign_card_number(self.dealer[0])
        player_card_1 = self.assign_card_number(self.player[0])
        player_card_2 = self.assign_card_number(self.player[1])
        outputs.append(dealer_card)
        outputs.append(player_card_1)
        outputs.append(player_card_2)
        return outputs

    def play(self, bot_input):
        while not self.game_over:

            while not self.round_over:
                self.check_deck()
                player_score = self.calc_hand(self.player)
                dealer_score = self.calc_hand(self.dealer)

                if self.standing:
                    if dealer_score > 21:
                        self.outcomes.append("Dealer Busted")
                        self.fitness += 1
                        self.round_over = True
                    elif player_score == dealer_score:
                        self.outcomes.append("Push")
                        self.round_over = True
                    #if the player has stood, then they must have a valid hand
                    elif player_score > dealer_score:
                        self.outcomes.append("Win")
                        self.fitness += 1
                        self.round_over = True
                    else:
                        self.outcomes.append("Loss")
                        self.round_over = True
                        self.game_over = True
                    break
                
                if self.first_hand and player_score == 21:
                    self.outcomes.append("Blackjack")
                    self.round_over = True
                    break

                if player_score > 21:
                    self.outcomes.append("Player Bust")
                    self.round_over = True
                    self.game_over = True
                    break

                if bot_input == 0:
                    self.first_hand = False
                    self.deal_next_card(self.player)
                elif bot_input == 1:
                    self.standing = True
                    while self.calc_hand(self.dealer) <= 16:
                        self.deal_next_card(self.dealer)
                else:
                    pass

            if self.round_over:
                self.reset_hand()
        self.game_over = True


def eval_genomes(genomes,config):
    #Run the game for player of the population
    #And create a neural network for each player
    for genome_id, genome in genomes:
        genome.fitness = 0
        #Generate a neural network
        net = neat.nn.FeedForwardNetwork.create(genome,config)
        #Start a new game
        game = Blackjack()
        while (not game.game_over):
            nnInput = game.output_info()
            output = net.activate(nnInput)
            max_index = 0
            max = 0
            for d in range(len(output)):  
                if output[d] > max:
                    max = output[d]
                    max_index = d
            #Feed the highest output index to the game
            game.play(max_index)
        genome.fitness = game.fitness

if __name__ == "__main__":
    config = neat.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,'./BlackJackNEAT')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(False))
    stats = neat.StatisticsReporter()
    winner = p.run(eval_genomes, 100)
