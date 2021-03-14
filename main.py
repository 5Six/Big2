import random
import quicksort
import itertools


class Card:
    def __init__(self, name, suit):
        self.name = name
        self.suit = suit

        if self.name == 2:
            self.rank = 1

        elif self.name == "A":
            self.rank = 2

        elif self.name == "K":
            self.rank = 3

        elif self.name == "Q":
            self.rank = 4

        elif self.name == "J":
            self.rank = 5

        else:
            self.rank = 16 - self.name

    def __eq__(self, other):
        if self.rank == other.rank and self.suit == other.suit:
            return True

        else:
            return False

    def __gt__(self, other):
        if self.rank < other.rank:
            return True

        elif self.rank == other.rank:
            if self.suit == "Spades" and other.suit != "Spades":
                return True

            if self.suit == "Hearts" and other.suit not in ("Spades", "Hearts"):
                return True

            if self.suit == "Clubs" and other.suit == "Diamonds":
                return True

            else:
                return False

        else:
            return False

    def __ge__(self, other):
        if self == other or self > other:
            return True

        else:
            return False

    def __lt__(self, other):
        if self >= other:
            return False

        else:
            return True

    def __le__(self, other):
        if self > other:
            return False

        else:
            return True


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def lowest(self):
        lowest = self.hand[0]

        for card in self.hand:
            if card < lowest:
                lowest = card

        print(self.name + "'s lowest card is", lowest.name, "of " + lowest.suit)

        return lowest

    def print_hand(self):
        for card in self.hand:
            print(card.name, card.suit)

    def sort_hand(self):
        quicksort.quick_sort(self.hand, 0, len(self.hand)-1)


class Deck:
    def __init__(self):
        self.deck = []
        for suit in ["Spades", "Hearts", "Clubs", "Diamonds"]:
            for name in ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]:
                self.deck.append(Card(name, suit))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self, players):
        n = 0
        for i in range(13):
            for player in players:
                player.hand.append(self.deck[n])
                n += 1

    def print_deck(self):
        for card in self.deck:
            print(card.name, card.suit)


class Game:
    def __init__(self, players, deck):
        self.deck = deck
        self.players = players
        self.pile = []
        self.previous_type = ""
        self.previous_combo = []
        self.turn = None
        self.passed = 0
        self.score = [0, 0, 0, 0]

    def start(self):
        self.pile = []
        self.previous_type = ""
        self.previous_combo = []
        self.turn = None
        self.passed = 0

        for player in self.players:
            player.hand = []

        self.deck.shuffle()
        self.deck.deal(self.players)
        player_with_lowest = self.players[0]
        lowest = self.players[0].lowest()

        for player in self.players:
            temp_lowest = player.lowest()
            player.sort_hand()
            if temp_lowest < lowest:
                lowest = temp_lowest
                player_with_lowest = player

        self.turn = player_with_lowest
        print(self.turn.name + "'s turn to play.")

    def combo_type(self, combo):
        if len(combo) == 1:
            return "Single"

        elif len(combo) == 2:
            if len({card.name for card in combo}) == 1:
                return "Pair"

            return False

        elif len(combo) == 3:
            if len({card.name for card in combo}) == 1:
                return "Triple"

            return False

        elif len(combo) == 5:
            quicksort.quick_sort(combo, 0, 4)

            if combo[0].name not in ("J", "Q", "K") and all((card_x.rank - 1) % 13 == card_y.rank % 13 for card_x, card_y in zip(combo, combo[1:])) and all(card.suit == combo[0].suit for card in combo):
                return "Straight Flush"

            if combo[0].name not in ("J", "Q", "K") and all((card_x.rank - 1) % 13 == card_y.rank % 13 for card_x, card_y in zip(combo, combo[1:])):
                return "Straight"

            if all(card.suit == combo[0].suit for card in combo):
                return "Flush"

            if len({card.name for card in combo}) == 2:
                if [card.name for card in combo].count(combo[0].name) == 2 or 3:
                    return "Full House"

                else:
                    return "Quad"

            return False

        else:
            return False

    def play_combo(self, player, combo_index):
        combo = [player.hand[i] for i in combo_index]

        if self.turn == player:
            if combo_index == [] and self.previous_combo == []:
                print("You cannot pass.")

            elif combo_index == [] and self.previous_combo != []:
                self.passed += 1
                print(player.name, " passed.")
                self.turn = self.players[(self.players.index(self.turn) + 1) % len(self.players)]
                print(self.turn.name + "'s turn to play.")

                if self.passed == len(self.players) - 1:
                    self.passed = 0
                    self.previous_type = ""
                    self.previous_combo = []

            elif self.combo_type(combo) != False and self.combo_valid(combo):
                for i in reversed(combo_index):
                    del player.hand[i]

                for card in combo:
                    self.pile.append(card)

                self.previous_type = self.combo_type(combo)
                self.previous_combo = combo

                if player.hand == []:
                    self.score[self.players.index(self.turn)] += 1
                    print(player.name, " has won. The score is ", self.score, ".")
                    self.start()

                else:
                    self.turn = self.players[(self.players.index(self.turn) + 1) % len(self.players)]
                    print(self.turn.name + "'s turn to play.")

            else:
                print("Combo is not valid.")

        else:
            print("It's not ", player.name, "'s turn to play.")

    def combo_valid(self, combo):
        if self.previous_type == "":
            return True

        elif self.previous_type in ["Single", "Pair", "Triple"] and self.previous_type == self.combo_type(combo):

            if self.previous_type == "Single":
                if combo[0] > self.previous_combo[0]:
                    return True

            elif self.previous_type == "Pair":
                if combo[1] > self.previous_combo[1]:
                    return True

            elif self.previous_type == "Triple":
                if combo[0] > self.previous_combo[0]:
                    return True

            return False

        elif self.previous_type == "Straight":
            if self.combo_type(combo) == "Straight" and combo[4] > self.previous_combo[4]:
                return True

            elif self.combo_type(combo) in ["Flush", "Full House", "Quad", "Straight Flush"]:
                return True

            return False

        elif self.previous_type == "Flush":
            if self.combo_type(combo) == "Flush" and combo[4] > self.previous_combo[4]:
                return True

            elif self.combo_type(combo) in ["Full House", "Quad", "Straight Flush"]:
                return True

            return False

        elif self.previous_type == "Full House":
            if self.combo_type(combo) == "Full House" and combo[2] > self.previous_combo[2]:
                return True

            elif self.combo_type(combo) in ["Quad", "Straight Flush"]:
                return True

            return False

        elif self.previous_type == "Quad":
            if self.combo_type(combo) == "Quad" and combo[1] > self.previous_combo[1]:
                return True

            elif self.combo_type(combo) in ["Straight Flush"]:
                return True

            return False

        elif self.previous_type == "Straight Flush":
            if self.combo_type(combo) == "Straight Flush" and combo[4] > self.previous_combo[4]:
                return True

            return False

    def pairs_in_hand(self, player):
        hand = player.hand
        current_rank = hand[0].rank
        rank_counter = 0
        rank_array = []
        pairs = []
        for i in range(len(hand)):
            if hand[i].rank == current_rank:
                rank_counter += 1
                rank_array.append(i)

            else:
                if rank_counter > 1:
                    for pair in itertools.combinations(rank_array, 2):
                        pairs.append(list(pair))

                current_rank = hand[i].rank
                rank_counter = 1
                rank_array = [i]

        for pair in itertools.combinations(rank_array, 2):
            pairs.append(list(pair))

        return pairs

    def triples_in_hand(self, player):
        hand = player.hand
        current_rank = hand[0].rank
        rank_counter = 0
        rank_array = []
        triples = []
        for i in range(len(hand)):
            if hand[i].rank == current_rank:
                rank_counter += 1
                rank_array.append(i)

            else:
                if rank_counter > 2:
                    for triple in itertools.combinations(rank_array, 3):
                        triples.append(list(triple))

                current_rank = hand[i].rank
                rank_counter = 1
                rank_array = [i]

        for triple in itertools.combinations(rank_array, 3):
            triples.append(list(triple))

        return triples

    def quads_in_hand(self, player):
        hand = player.hand
        current_rank = hand[0].rank
        rank_counter = 0
        rank_array = []
        quads = []
        for i in range(len(hand)):
            if hand[i].rank == current_rank:
                rank_counter += 1
                rank_array.append(i)

            else:
                if rank_counter > 3:
                    for quad in itertools.combinations(rank_array, 4):
                        quads.append(list(quad))

                current_rank = hand[i].rank
                rank_counter = 1
                rank_array = [i]

        for quad in itertools.combinations(rank_array, 4):
            quads.append(list(quad))

        return quads

    def straights_in_hand(self, player):
        rank_list = []
        for card in player.hand:
            rank_list.append(card.rank)

        rank_list_no_dupe = list(reversed(list(set(rank_list))))
        straights =[]
        for rank in rank_list_no_dupe:
            if (rank + 1) % 13 in rank_list_no_dupe and\
               (rank + 2) % 13 in rank_list_no_dupe and\
               (rank + 3) % 13 in rank_list_no_dupe and\
               (rank + 4) % 13 in rank_list_no_dupe and\
               not (1 in rank_list_no_dupe and 2 in rank_list_no_dupe and 3 in rank_list_no_dupe):
                straight_comb = []
                for rank2 in [rank, (rank + 1) % 13, (rank + 2) % 13, (rank + 3) % 13, (rank + 4) % 13]:
                    indexes = [index for index, elem in enumerate(rank_list) if elem == rank2]
                    straight_comb.append(indexes)

                for straight in list(itertools.product(*straight_comb)):
                    straights.append(reversed(list(straight)))

        return straights

    def valid_combos_in_hand(self, player):
        combos = []
        if self.previous_combo == [] and self.turn != player:
            print(player.name, "has no valid combos.")

        elif self.previous_combo == [] and self.turn == player:
            hand = player.hand

            counter = 0
            for card in hand:
                if card.rank != hand[0].rank:
                    break
                counter += 1

            if counter >= 1:
                combos.append([0])
                for quad in self.quads_in_hand(player):
                    if len(set([0] + quad)) == 5:
                        combos.append([0] + quad)

            if counter >= 2:
                combos.append([0, 1])

                for triple in self.triples_in_hand(player):
                    if len(set([0, 1] + triple)) == 5:
                        combos.append([0, 1] + triple)

            if counter >= 3:
                combos.extend([[0, 2], [0, 1, 2]])

                for triple in self.triples_in_hand(player):
                    if len(set(triple + [0, 2])) == 5:
                        combos.append(triple + [0, 2])

                for pair in self.pairs_in_hand(player):
                    if len(set([0, 1, 2] + pair)) == 5:
                        combos.append([0, 1, 2] + pair)

            if counter >= 4:
                combos.extend([[0, 3], [0, 1, 3], [0, 2, 3]])

                for triple in self.triples_in_hand(player):
                    if len(set(triple + [0, 3])) == 5:
                        combos.append(triple + [0, 3])

                for pair in self.pairs_in_hand(player):
                    for triple in [[0, 1, 3], [0, 2, 3]]:
                        if len(set(triple + pair)) == 5:
                            combos.append(triple + pair)

                if len(hand) != 4:
                    for i in range(4, len(hand)):
                        combos.append([0, 1, 2, 3, i])

        return combos



Warren = Player("Warren")
Justin = Player("Justin")
Isaac = Player("Isaac")

stdDeck = Deck()
#stdDeck.print_deck()

game = Game([Warren, Justin, Isaac], stdDeck)
game.start()

