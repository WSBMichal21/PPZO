import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def value(self):
        if self.rank in ["J", "Q", "K"]:
            return 10
        elif self.rank == "A":
            return 11
        return int(self.rank)

    def __str__(self):
        return f"{self.rank}{self.suit}"


class Deck:
    def __init__(self):
        suits = ["♠", "♥", "♦", "♣"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10",
                 "J", "Q", "K", "A"]

        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()


class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def calculate_value(self):
        value = sum(card.value() for card in self.cards)

        aces = sum(1 for card in self.cards if card.rank == "A")

        while value > 21 and aces:
            value -= 10
            aces -= 1

        return value

    def __str__(self):
        return ", ".join(str(card) for card in self.cards)


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()

    def hit(self, deck):
        self.hand.add_card(deck.deal_card())

    def stand(self):
        print(f"{self.name} kończy dobieranie kart.")


class Dealer(Player):
    def __init__(self):
        super().__init__("Dealer")

    def play(self, deck):
        while self.hand.calculate_value() < 17:
            self.hit(deck)


deck = Deck()
deck.shuffle()

player = Player("Gracz")
dealer = Dealer()

for _ in range(2):
    player.hit(deck)
    dealer.hit(deck)

while True:
    print("\nTwoje karty:", player.hand)
    print("Wartość:", player.hand.calculate_value())

    if player.hand.calculate_value() > 21:
        print("Przegrałeś! Przekroczyłeś 21.")
        exit()

    choice = input("Hit (h) czy Stand (s)? ").lower()

    if choice == "h":
        player.hit(deck)
    else:
        player.stand()
        break

dealer.play(deck)

print("\n=== Wyniki ===")
print("Gracz:", player.hand,
      "| Wartość:", player.hand.calculate_value())
print("Dealer:", dealer.hand,
      "| Wartość:", dealer.hand.calculate_value())

player_value = player.hand.calculate_value()
dealer_value = dealer.hand.calculate_value()

if dealer_value > 21:
    print("Dealer przekroczył 21. Wygrywasz!")
elif player_value > dealer_value:
    print("Wygrywasz!")
elif player_value < dealer_value:
    print("Przegrywasz!")
else:
    print("Remis!")