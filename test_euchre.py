from classes.Card import Card
from classes.EuchreDeck import EuchreDeck

def inc(x):
    return x + 1


def test_answer():
    assert inc(3) == 4

d = EuchreDeck()
d.get_new_deck()

hand = d.deal_cards(n=5)
for card in hand:
    card.get_card()
    print(len(d.cards))