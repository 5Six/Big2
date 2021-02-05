import random
import quicksort


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

    def pairs_in_hand(self,player):
        

    def valid_combos_in_hand(self, player):
        hand = player.hand
        combos = []
        if self.previous_combo == [] and (hand[0].rank != 13 or hand[0].suit != "Diamonds"):
            print(player.name, "has no valid combos.")

        elif self.previous_combo == [] and hand[0].rank == 13 and hand[0].suit == "Diamonds":
            counter = 0
            for card in hand:
                if card.rank == 13:
                    counter += 1

                else:
                    break

            if counter >= 1:
                combos.append([0])

            if counter >= 2:
                combos.append([0, 1])

            if counter >= 3:
                combos.append([0, 2], [1, 2], [0, 1, 2])
                for

            if counter >= 4:
                combos.append([0, 3], [1, 3], [2, 3], [0, 1, 3], [0, 2, 3], [1, 2, 3])

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

