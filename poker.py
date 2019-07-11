from random import shuffle


class Card:

    def __init__(self, value, suit):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value} of {self.suit}"


class Hand:

    def __init__(self, cards):
        self.cards = cards

    def __repr__(self):
        return f"{self.cards[0]}, {self.cards[1]}, {self.cards[2]}, {self.cards[3]}, {self.cards[4]}"

    def __getitem__(self, key):
        return self.cards[key]

    def __add__(self, other):
        return Hand(self.cards + list(other))

    def __len__(self):
        return len(self.cards)

    def discard(self):
        while True:
            try:
                dis = input("Which cards would you like to discard? ")
                int(dis)
                dis = list(set(dis))
                if dis != ['0']:
                    discard_list = [self[int(i) - 1] for i in dis]
                    for i in discard_list:
                        self.cards.remove(i)
                return self
            except ValueError:
                print('Try again. Example: to discard first and third card enter 13\n')
                print(self)
            except IndexError:
                print('Try again. Valid numbers include 0, 1, 2, 3, 4, 5\n')
                print(self)

    def play_hand(self, d):
        print(self)
        self.discard()
        if len(self) < 5:
            self.cards += d.deal_hand(5 - len(self))
        return self

    def is_royal_flush(self):
        royal_list = ['A', 'K', 'Q', 'J', '10']
        values = [card.value for card in self.cards if card.value in royal_list]
        if len(values) == 5 and self.is_flush():
            return True
        return False

    def is_straight_flush(self):
        if self.is_straight() and self.is_flush():
            return True
        return False

    def is_four_of_a_kind(self):
        values = [card.value for card in self.cards]
        for value in values:
            if values.count(value) == 4:
                return True
        return False

    def is_full_house(self):
        values = [card.value for card in self.cards]
        for value in values:
            if values.count(value) == 3:
                pair_check = [v for v in values if v != value]
                if pair_check[0] == pair_check[1]:
                    return True
        return False

    def is_flush(self):
        suits = [card.suit for card in self.cards]
        if suits.count(suits[0]) == 5:
            return True
        return False

    def is_straight(self):
        values = [card.value for card in self.cards]
        values = [11 if x == 'J' else 12 if x == 'Q' else 13 if x == 'K' else 14 if x == 'A' else int(x) for x in
                  values]
        values.sort()
        if values == [2, 3, 4, 5, 14]:
            return True
        i = 0
        j = 1
        while i < 4:
            if values[j] - values[i] != 1:
                return False
            i += 1
            j += 1
        return True

    def is_three_of_a_kind(self):
        values = [card.value for card in self.cards]
        for value in values:
            if values.count(value) == 3:
                return True
        return False

    def is_two_pair(self):
        values = [card.value for card in self.cards]
        for value in values:
            if values.count(value) == 2:
                pair_check = [v for v in values if v != value]
                for p in pair_check:
                    if pair_check.count(p) == 2:
                        return True
                break
        return False

    def is_pair(self):
        values = [card.value for card in self.cards]
        for value in values:
            if values.count(value) == 2:
                return True
        return False

    def determine_value(self):
        if self.is_royal_flush():
            return 'Royal Flush', 9, self
        elif self.is_straight_flush():
            return 'Straight Flush', 8, self
        elif self.is_four_of_a_kind():
            return '4 of a kind', 7, self
        elif self.is_full_house():
            return 'Full House', 6, self
        elif self.is_flush():
            return 'Flush', 5, self
        elif self.is_straight():
            return 'Straight', 4, self
        elif self.is_three_of_a_kind():
            return '3 of a kind', 3, self
        elif self.is_two_pair():
            return '2 pair', 2, self
        elif self.is_pair():
            return 'Pair', 1, self
        return "You got nothin'", 0, self


class Deck:

    def __init__(self):
        suits = ('Diamonds', 'Hearts', 'Spades', 'Clubs')
        values = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
        self.cards = [Card(value, suit) for value in values for suit in suits]
        self.shuffle()

    def __repr__(self):
        return f"Deck of {self.count()} cards."

    def count(self):
        return len(self.cards)

    def _deal(self, num):
        count = self.count()
        if count < num:
            print("Deck is out of cards. Reshuffling deck and restarting game.")
            play_poker()
            return self
        cards = self.cards[-num:]
        self.cards = self.cards[:-num]
        return cards

    def deal_hand(self, hand_size):
        return self._deal(hand_size)

    def shuffle(self):
        if self.count() < 52:
            raise ValueError("Only full decks can be shuffled")
        shuffle(self.cards)
        return self


def determine_winner(hand1, hand2):
    if hand1[1] > hand2[1]:
        return "Player 1 Wins"
    elif hand2[1] > hand1[1]:
        return "Player 2 Wins"
    else:
        return tie_breaker(hand1, hand2)


def tie_breaker(hand1, hand2):
    h1_sort = [
        11 if x.value == 'J' else 12 if x.value == 'Q' else 13 if x.value == 'K' else 14 if x.value == 'A' else int(
            x.value) for x in hand1[2]]
    h1_sort.sort(reverse=True)
    h2_sort = [
        11 if x.value == 'J' else 12 if x.value == 'Q' else 13 if x.value == 'K' else 14 if x.value == 'A' else int(
            x.value) for x in hand2[2]]
    h2_sort.sort(reverse=True)

    if hand1[1] in [0, 4, 5, 8, 9]:
        for (i, j) in zip(h1_sort, h2_sort):
            if i != j:
                if i > j:
                    return 'Player 1 Wins'
                return 'Player 2 Wins'
        return "It's a tie"
    elif hand1[1] in [1, 2, 3, 7]:
        h1_dups = list({x for x in h1_sort if h1_sort.count(x) > 1})
        h1_dups.sort(reverse=True)
        h2_dups = list({x for x in h2_sort if h2_sort.count(x) > 1})
        h2_dups.sort(reverse=True)
        for (i, j) in zip(h1_dups, h2_dups):
            if i != j:
                if i > j:
                    return 'Player 1 Wins'
                return 'Player 2 Wins'
        h1_left_overs = [x for x in h1_sort if x not in h1_dups]
        h2_left_overs = [x for x in h2_sort if x not in h2_dups]
        for (i, j) in zip(h1_left_overs, h2_left_overs):
            if i != j:
                if i > j:
                    return 'Player 1 Wins'
                return 'Player 2 Wins'
        return "It's a tie"
    else:
        h1_trips = list({x for x in h1_sort if h1_sort.count(x) == 3})[0]
        h2_trips = list({x for x in h2_sort if h2_sort.count(x) == 3})[0]
        if h1_trips > h2_trips:
            return 'Player 1 Wins'
        elif h2_trips > h1_trips:
            return 'Player 2 Wins'
        else:
            h1_pair = list({x for x in h1_sort if x not in h1_trips})[0]
            h2_pair = list({x for x in h2_sort if x not in h2_trips})[0]
            if h1_pair > h2_pair:
                return 'Player 1 Wins'
            else:
                return 'Player 2 Wins'


def play_poker():
    d = Deck()
    while True:
        if d.count() > 10:
            h1 = Hand(d.deal_hand(5))
            h2 = Hand(d.deal_hand(5))
        else:
            print('Not enough cards to start new game. Reshuffling deck.')
            play_poker()
            break

        print('Player 1: ')
        h1 = h1.play_hand(d)

        print('\nPlayer 2:')
        h2 = h2.play_hand(d)

        print(f"\nPlayer 1:\n{h1}")
        h1_value = h1.determine_value()
        print(h1_value[0])

        print(f"\nPlayer 2:\n{h2}")
        h2_value = h2.determine_value()
        print(h2_value[0])

        print()
        print(determine_winner(h1_value, h2_value))
        print(d)
        play_again = input("Play again? (y/n) ").lower()
        if play_again == 'n':
            break


print("Tips:\nTo choose which cards to discard type their position."
      "\nExample: To discard the 3rd and 5th card type 35"
      "\n         To keep all cards type 0\n")
play_poker()
