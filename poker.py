from random import shuffle

class poker:

    cards = [
        "\u2663\U0000FE0F\U0001F170\U0000FE0F", "\u2663\U0000FE0F\U00000032\U0000FE0F\U000020E3", "\u2663\U0000FE0F\U00000033\U0000FE0F\U000020E3", "\u2663\U0000FE0F\U00000034\U0000FE0F\U000020E3", "\u2663\U0000FE0F\U00000035\U0000FE0F\U000020E3", "\u2663\U0000FE0F\U00000036\U0000FE0F\U000020E3", "\u2663\U0000FE0F\U00000037\U0000FE0F\U000020E3", "\u2663\U0000FE0F\U00000038\U0000FE0F\U000020E3", "\u2663\U0000FE0F\U00000039\U0000FE0F\U000020E3", "\u2663\U0000FE0F\U0001F51F", "\u2663\U0000FE0F\U0001F482", "\u2663\U0000FE0F\U0001F478", "\u2663\U0000FE0F\U0001F934",
        "\u2660\U0000FE0F\U0001F170\U0000FE0F", "\u2660\U0000FE0F\U00000032\U0000FE0F\U000020E3", "\u2660\U0000FE0F\U00000033\U0000FE0F\U000020E3", "\u2660\U0000FE0F\U00000034\U0000FE0F\U000020E3", "\u2660\U0000FE0F\U00000035\U0000FE0F\U000020E3", "\u2660\U0000FE0F\U00000036\U0000FE0F\U000020E3", "\u2660\U0000FE0F\U00000037\U0000FE0F\U000020E3", "\u2660\U0000FE0F\U00000038\U0000FE0F\U000020E3", "\u2660\U0000FE0F\U00000039\U0000FE0F\U000020E3", "\u2660\U0000FE0F\U0001F51F", "\u2660\U0000FE0F\U0001F482", "\u2660\U0000FE0F\U0001F478", "\u2660\U0000FE0F\U0001F934",
        "\u2665\U0000FE0F\U0001F170\U0000FE0F", "\u2665\U0000FE0F\U00000032\U0000FE0F\U000020E3", "\u2665\U0000FE0F\U00000033\U0000FE0F\U000020E3", "\u2665\U0000FE0F\U00000034\U0000FE0F\U000020E3", "\u2665\U0000FE0F\U00000035\U0000FE0F\U000020E3", "\u2665\U0000FE0F\U00000036\U0000FE0F\U000020E3", "\u2665\U0000FE0F\U00000037\U0000FE0F\U000020E3", "\u2665\U0000FE0F\U00000038\U0000FE0F\U000020E3", "\u2665\U0000FE0F\U00000039\U0000FE0F\U000020E3", "\u2665\U0000FE0F\U0001F51F", "\u2665\U0000FE0F\U0001F482", "\u2665\U0000FE0F\U0001F478", "\u2665\U0000FE0F\U0001F934",
        "\u2666\U0000FE0F\U0001F170\U0000FE0F", "\u2666\U0000FE0F\U00000032\U0000FE0F\U000020E3", "\u2666\U0000FE0F\U00000033\U0000FE0F\U000020E3", "\u2666\U0000FE0F\U00000034\U0000FE0F\U000020E3", "\u2666\U0000FE0F\U00000035\U0000FE0F\U000020E3", "\u2666\U0000FE0F\U00000036\U0000FE0F\U000020E3", "\u2666\U0000FE0F\U00000037\U0000FE0F\U000020E3", "\u2666\U0000FE0F\U00000038\U0000FE0F\U000020E3", "\u2666\U0000FE0F\U00000039\U0000FE0F\U000020E3", "\u2666\U0000FE0F\U0001F51F", "\u2666\U0000FE0F\U0001F482", "\u2666\U0000FE0F\U0001F478", "\u2666\U0000FE0F\U0001F934",
        ]

    current_cards = list()
    current_card_position = 0

    phase_list = ["Austeilen", "Flop", "Turn", "River"]
    current_phase = 0

    pot = 0
    start_stack = 30000
    
    number_of_players = 0
    player_ids = list()
    player_names = list()
    player_stacks = list()
    player_order_blinds = list()

    def place_a_bet(self, id, amount):
        player_number = self.player_ids.index(id)
        self.pot += amount
        self.player_stacks[player_number] -= amount
        print("{} (player {}) has bet {}.".format(self.player_names[player_number], player_number, amount))

    def set_the_stack(self, player, new_stack):
        player_number = self.player_names.index(player)
        self.player_stacks[player_number] = new_stack
        print("{} (player {}) stack updated to {}.".format(self.player_names[player_number], player_number, self.player_stacks[player_number]))

    def distribute_the_pot(self, player_share):
        for players_share in player_share:
            player_number = self.player_names.index(players_share[0])
            current_stack = self.player_stacks[player_number]
            pot_share = float(players_share[1]) * self.pot
            self.set_the_stack(players_share[0], current_stack + int(pot_share))
        old_pot = self.pot
        self.pot = 0
        return old_pot

    def join_player(self, id, name):
        self.player_ids.append(id)
        self.player_names.append(name)
        self.player_stacks.append(self.start_stack)
        self.number_of_players = len(self.player_ids)
        print("{} joined as player {}. ID: {}.".format(self.player_names[self.number_of_players-1], self.number_of_players-1, id))

    def remove_player(self,id):
        player_number = self.player_ids.index(id)
        player_name = self.player_names[player_number]
        del self.player_ids[player_number]
        del self.player_stacks[player_number]
        del self.player_names[player_number]
        self.current_cards.clear()
        #self.start_the_game()
        print("{} (player {}) left (id: {}).".format(player_name, player_number, id))

    def start_the_game(self):
        self.current_cards.append(list())
        self.number_of_players=len(self.player_ids)
        for i in range(self.number_of_players):
            self.current_cards.append(list())
        players_shuffled = self.player_names.copy()
        shuffle(players_shuffled)
        self.player_order_blinds = [[keys,""] for keys in players_shuffled]
        if self.number_of_players > 2:
            self.player_order_blinds[0][1] = "Dealer"
            self.player_order_blinds[1][1] = "Small Blind"
            self.player_order_blinds[2][1] = "Big Blind"
        elif self.number_of_players == 2:
            self.player_order_blinds[0][1] = "Dealer, Small Blind"
            self.player_order_blinds[1][1] = "Big Blind"
        else: #it's just a test!
            self.player_order_blinds[0][1] = "Dealer, Small Blind, Big Blind"
        print("Game started.")

    def distribute_cards(self):
        if self.current_phase == 0:
            self.pot = 0
            shuffle(self.cards)
            self.current_card_position = 0
            print(self.cards)
            for i in range(len(self.current_cards)):
                self.current_cards[i].clear()
            for i in range(self.number_of_players):
                self.current_cards[i+1].append(self.cards[self.current_card_position])
                self.current_cards[i+1].append(self.cards[self.current_card_position + self.number_of_players])
                self.current_card_position += 1
                print(self.current_cards)
            self.current_card_position += self.number_of_players
            self.current_phase = 1
        elif self.current_phase == 1:
            self.current_card_position += 1 #burn one
            for i in range(3):
                self.current_cards[0].append(self.cards[self.current_card_position+i])
                print(self.current_cards)
            self.current_card_position += 3
            self.current_phase = 2
        elif self.current_phase == 2:
            self.current_card_position += 1 #burn one
            self.current_cards[0].append(self.cards[self.current_card_position])
            self.current_card_position += 1
            self.current_phase = 3
            print(self.current_cards)
        elif self.current_phase == 3:
            self.current_card_position += 1 #burn one
            self.current_cards[0].append(self.cards[self.current_card_position])
            self.current_card_position += 1
            self.current_phase = 0
            print(self.current_cards)

    def end_the_hand(self):
        self.current_phase = 0
        print("Hand ended.")

    def end_the_game(self):
        self.current_cards.clear()
        self.current_card_position = 0
        self.current_phase = 0

        self.number_of_players = 0
        self.player_ids.clear()
        self.player_names.clear()
        self.player_stacks.clear()

        self.pot = 0
        print("Game ended.")
