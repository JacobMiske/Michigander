# python euchre game
import random
from itertools import permutations
from collections import Counter

# TODO: Organize! This code needs more structure, break down into separate files and put objects together into unique classes later on

# main variables
suits = ['H', 'S', 'C', 'D']
values = ['9', '10', 'J', 'Q', 'K', 'A']
values_dict = {'9': 1, '10': 2, 'J':3, 'Q':4, 'K':5, 'A':6}
# get each possible card from suits and values used
def get_deck(suits, values):
    # returns shuffled deck
    A = [[[x,y] for x in values] for y in suits]
    deck = [item for subl in A for item in subl]
    deck = [''.join(i) for i in deck]
    return deck

def deal_hand(deck):
    # select five cards from deck at random and return hand and remaining deck
    hand = []
    rem_deck = deck
    while len(hand) < 5:
        A = rem_deck[random.randint(0, len(rem_deck)-1)]
        hand.append(A)
        rem_deck.remove(A)
    return hand, rem_deck

def deal_four_hands(deck):
    # deals four hands, selects top kitty card, and sets aside three in kitty
    hands = []
    rem_deck = deck
    for _ in range(0, 4):
        a, rem_deck = deal_hand(deck=rem_deck)
        hands.append(a)
    top_kitty = rem_deck[random.randint(0, len(rem_deck)-1)]
    rem_deck.remove(top_kitty)
    rest_of_kitty = rem_deck
    return hands, top_kitty, rest_of_kitty

def get_cards_from_suit(suit, deck):
    # returns list of cards in a suit, given string suit (eg 'S') and deck
    suit_cards = []
    for i in deck:
        if suit in i:
            suit_cards.append(i)
    return suit_cards

def get_cards_not_from_suit(suit, deck):
    # returns list of cards not in a suit, given string suit (eg 'S') and deck
    suit_cards = []
    for i in deck:
        if suit not in i:
            suit_cards.append(i)
    return suit_cards

def get_hierarchy(t_suit, deck):
    # returns dict of hierachy key is card, value is int representing hierarchy (1 is best), given the trump suit and deck
    cards_not_trump = get_cards_not_from_suit(suit=t_suit, deck=deck)
    hierarchy = {}
    if t_suit == 'S':
        # declare bowers
        hierarchy['JS'] = 7
        hierarchy['AS'] = 5
        hierarchy['KS'] = 4
        hierarchy['QS'] = 3
        hierarchy['10S'] = 2
        hierarchy['9S'] = 1
        for i in cards_not_trump:
            hierarchy[i] = 0
        hierarchy['JC'] = 6
        return hierarchy
    if t_suit == 'D':
        hierarchy['JD'] = 7
        hierarchy['AD'] = 5
        hierarchy['KD'] = 4
        hierarchy['QD'] = 3
        hierarchy['10D'] = 2
        hierarchy['9D'] = 1
        for i in cards_not_trump:
            hierarchy[i] = 0
        hierarchy['JH'] = 6
        return hierarchy
    if t_suit == 'H':
        hierarchy['JH'] = 7
        hierarchy['AH'] = 5
        hierarchy['KH'] = 4
        hierarchy['QH'] = 3
        hierarchy['10H'] = 2
        hierarchy['9H'] = 1
        for i in cards_not_trump:
            hierarchy[i] = 0
        hierarchy['JD'] = 6
        return hierarchy
    if t_suit == 'C':
        hierarchy['JC'] = 7
        hierarchy['AC'] = 5
        hierarchy['KC'] = 4
        hierarchy['QC'] = 3
        hierarchy['10C'] = 2
        hierarchy['9C'] = 1
        for i in cards_not_trump:
            hierarchy[i] = 0
        hierarchy['JS'] = 6
        return hierarchy
    return -1

def get_options(hand, lead_suit):
    # given a hand (1 to 5 cards) and the lead_suit (eg 'S'), return subset of hand that can be played
    sub_hand = []
    # obviously if you only have one card, that's the only thing you can play
    if len(hand) == 1:
        return hand
    # check if hand contains lead suit
    has_lead_suit = False
    for card in hand:
        if card[-1:] == lead_suit:
            has_lead_suit = True
            sub_hand.append(card)
    if not has_lead_suit:
        for card in hand:
            sub_hand.append(card)
    return sub_hand

def replace_player_dealer_card(hand, kat):
    # given dealer's hand, the kat, returns the new hand
    print("Your current hand: {}".format(hand))
    print("The kat: {}".format(kat))
    while True:
        card_to_swap = input("Which card do you want to replace with kat? (write it out: eg 'KS')")
        try:
            hand.remove(card_to_swap)
            hand.insert(kat)
        except:
            pass
        return hand
    return -1

def replace_CPU_dealer_card(hand, kat):
    # given CPU's hand, the kat, returns the new hand and card set away
    new_hand = hand
    suits = [card[:-1] for card in hand]
    # TODO: dumb logic for now, replace first card in hand, come back later to improve

    return new_hand, lost_card

def play_trick(card1, card2, card3, card4, t_suit, deck):
    # given four cards and t_suit, card1 being the lead, determine the winner (returns int = card#)
    cards = [card1, card2, card3, card4]
    lead_suit = card1[-1]
    print(lead_suit)
    # first use hierarchy to find winner, if all zeros (no trump) then base of lead_suit
    hier = get_hierarchy(t_suit=t_suit, deck=deck)
    hierachies = []
    for card in cards:
        hierachies.append(hier[card])
    print(hierachies)
    if hierachies == [0, 0, 0, 0]:
        # no trump in trick
        winning_card = card1
        winning_card_value = card1[:-1]
        if card2[-1] == lead_suit:
            card2value = card2[:-1]
            if values_dict[card2value] > values_dict[winning_card_value]:
                winning_card = card2
                winning_card_value = card2[:-1]
        if card3[-1] == lead_suit:
            card3value = card3[:-1]
            if values_dict[card3value] > values_dict[winning_card_value]:
                winning_card = card3
                winning_card_value = card3[:-1]
        if card4[-1] == lead_suit:
            card4value = card4[:-1]
            if values_dict[card4value] > values_dict[winning_card_value]:
                winning_card = card4
                winning_card_value = card4[:-1]
        index_winner = cards.index(winning_card)
        print("winning card player: {}".format(index_winner+1))
        return -1
    else:
        # trump suit is involved in trick
        index_winner = hierachies.index(max(hierachies))
        print("winning card player: {}".format(index_winner+1))
        return index_winner+1
    return -1

def CPU_pass_or_pick_up(h, kat):
    # given a hand and the kat card, returns 0 for pass and 1 for 'pick it up'
    kat_suit = kat[-1]
    kat_suit_cards = 0
    for card in h:
        if card[-1] == kat_suit:
            kat_suit_cards += 1
    # CPU says 'pick it up' if they have 4 or 5 kat suit cards
    if kat_suit_cards > 3:
        return 1
    else:
        return 0

def CPU_pass_or_declare_trump(h, kat_suit):
    # given a hand, declare trump suit (return eg 'S') or pass 0
    suits = {'S': 0, 'C': 0, 'D': 0, 'H': 0}
    for card in h:
        card_suit = card[-1]
        suits[card_suit] += 1
    # CPU declares trump suit if they have 3, 4, or 5 of that suit cards
    for suit, number in suits.items():
        if number > 2:
            if suit != kat_suit:
                return suit
    return 0

def get_kat_decision(h1, h2, h3, h4, d, kat):
    # walks through the start of the round in which the trump suit is determined
    # starts with player left of dealer (d is int)
    # returns 0 if all passed, 1 is someone demanded it, also returns player who demanded it
    # also returns t_suit
    counter = 0
    hands = [h1, h2, h3, h4]
    if d == 0:
        # dealer is player
        if CPU_pass_or_pick_up(h2, kat=kat):
            print("player 2 says pick it up")
            replace_player_dealer_card(hand=h1, kat=kat)
            return 1
        if CPU_pass_or_pick_up(h3, kat=kat):
            print("player 3 (your partner) says pick it up")
            replace_player_dealer_card(hand=h1, kat=kat)
            return 1
        if CPU_pass_or_pick_up(h4, kat=kat):
            print("player 4 says pick it up")
            replace_player_dealer_card(hand=h1, kat=kat)
            return 1
        player_pass_or_pick = input("Back to you dealer: pass on kat or pick it up? (0 to pass, 1 to pick up)")
        if player_pass_or_pick:
            replace_player_dealer_card(hand=h1, kat=kat)
        return 0
    if d != 0:
        # dealer is not player
        while counter < 3: 
            player_pass_or_demand = input("What will you say: pass on kat or tell player {} to pick it up? (0 to pass, 1 to tell player {} to pick up)".format(d))

def get_trump_suit_declared(h1, h2, h3, h4, d, kat_suit):
    # kat has been rejected, given hands and current dealer, find the trump suit! 
    # return 0 if dealer forced, otherwise 1, error -1
    # also returns t_suit
    if d == 0:
        # dealer is player
        player_2_decision = CPU_pass_or_declare_trump(h2, kat=kat)
        if player_2_decision:
            print("player 2 declares ")
            return player_2_decision
        player_3_decision = CPU_pass_or_declare_trump(h3, kat=kat)
        if CPU_pass_or_pick_up(h3, kat=kat):
            print("player 3 (your partner) says pick it up")
            replace_dealers_card(hand=h1, kat=kat)
            return 1
        player_4_decision = CPU_pass_or_declare_trump(h4, kat=kat)
        if CPU_pass_or_pick_up(h4, kat=kat):
            print("player 4 says pick it up")
            replace_dealers_card(hand=h1, kat=kat)
            return 1
        player_pass_or_pick = input("Back to you dealer: you have to say something!")
        if player_pass_or_pick:
            replace_dealers_card(hand=h1, kat=kat)
            return 0
    if d == 1:
        # dealer is CPU left of player
        if CPU_pass_or_pick_up(h3, kat=kat):
            print("player 3 (your partner) says pick it up")
            replace_dealers_card(hand=h1, kat=kat)
            return 1
        if CPU_pass_or_pick_up(h4, kat=kat):
            print("player 4 says pick it up")
            replace_dealers_card(hand=h1, kat=kat)
            return 1
        player_pass_or_pick = input("Back to you dealer: you have to say something!")
        return 1
    if d == 2:
        # dealer is CPU parter of player
        return 1
    if d == 3:
        # dealer is CPU right of player
        return 1
    return 0

def show_table():
    # prints currently on table
    return -1

deck = get_deck(suits=suits, values=values)
a_deck = get_deck(suits=suits, values=values)
four_hands, kat, rest = deal_four_hands(deck=a_deck)

hand1 = four_hands[0] 
hand2 = four_hands[1]
hand3 = four_hands[2]
hand4 = four_hands[3]

def play_euchre():
    # main function, progresses game
    A = input("Welcome")
    B = input("press any key to deal out the hands (you start as dealer)")
    team_1_score = 0
    team_2_score = 0
    hand_counter = 0
    dealer = 0
    while team_1_score < 10 and team_2_score < 10:
        deck = get_deck(suits=suits, values=values)
        trump_suit = ''
        four_hands, kat, three_left = deal_four_hands(deck=deck)
        kat_suit = kat[-1:]
        print(kat_suit)
        quit()
        hand1 = four_hands[0]
        hand2 = four_hands[1]
        hand3 = four_hands[2]
        hand4 = four_hands[3]
        print("Your hand: {}".format(hand1))
        print("The top of the kitty: {}".format(kat))
        kat_picked_up = get_kat_decision(hand1, hand2, hand3, hand4, d=dealer, kat=kat)
        if not kat_picked_up:
            get_trump_suit_declared(hand1, hand2, hand3, hand4, d=dealer, kat_suit=kat_suit)

        quit()
        # hand is over, change dealer
        dealer += 1
        if dealer == 3:
            # reset dealer to player 1
            dealer = 0
        team_1_score += 1
    return -1

play_euchre()