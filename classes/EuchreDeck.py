from .Card import Card
import random

class EuchreDeck:
    
    def __init__(self):
        self.cards = []

    def get_new_deck(self):
        # Puts cards in self.cards
        suits = ['H', 'S', 'C', 'D']
        values = ['9', '10', 'J', 'Q', 'K', 'A']
        for suit in suits:
            for value in values:
                self.cards.append(Card(suit, value))

    def deal_cards(self, n):
        hand = []
        while len(hand) < n:
            deck_len = len(self.cards)
            random_card = random.randint(0, deck_len-1)
            A = self.cards[random_card]
            hand.append(A)
            self.cards.remove(A)
        return hand