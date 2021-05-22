class Card:

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def get_card(self):
        # prints suit and value
        print(self.suit)
        print(self.value)