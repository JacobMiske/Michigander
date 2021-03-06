# python euchre game
# Jacob Miske MIT License
import random
from itertools import permutations
from collections import Counter
from terminal_playing_cards import Deck, View

# TODO: Organize! This code needs more structure, break down into separate files and put objects together into unique classes later on

# main variables
suits = ['H', 'S', 'C', 'D']
values = ['9', '10', 'J', 'Q', 'K', 'A']
values_dict = {'9': 1, '10': 2, 'J':3, 'Q':4, 'K':5, 'A':6}
card_dict = {'AC': 0, 'AD': 1, 'AS': 2, 'AH': 3, '2C': 4, '2D': 5, '2S': 6, '2H': 7, '3C': 8, '3D': 9, '3S': 10, '3H': 11,
            '4C': 12, '4D': 13, '4S': 14, '4H': 15, '5C': 16, '5D': 17, '5S': 18, '5H': 19, '6C': 20, '6D': 21, '6S': 22, '6H': 23,
            '7C': 24, '7D': 25, '7S': 26, '7H': 27, '8C': 28, '8D': 29, '8S': 30, '8H': 31, '9C': 32, '9D': 33, '9S': 34, '9H': 35,
            '10C': 36, '10D': 37, '10S': 38, '10H': 39, 'JC': 40, 'JD': 41, 'JS': 42, 'JH': 43, 'QC': 44, 'QD': 45, 'QS': 46, 'QH': 47,
            'KC': 48, 'KD': 49, 'KS': 50, 'KH': 51}

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
    not_suit_cards = []
    for i in deck:
        i_suit = i[-1:]
        if i_suit != suit:
            not_suit_cards.append(i)
    return not_suit_cards

def print_hand(hand):
    # Using terminal-playing-cards library, print hand to terminal
    deck = Deck()
    card_values = [card_dict[i] for i in hand]
    card_images = View([deck.__getitem__(i) for i in card_values])
    print(card_images)
    return -1

def print_table():
    # prints currently on table
    return -1

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

def get_options(hand, lead_suit, t_suit):
    # given a hand (1 to 5 cards) and the lead_suit (eg 'S'), return subset of hand that can be played
    sub_hand = []
    # obviously if you only have one card, that's the only thing you can play
    if len(hand) == 1:
        return hand
    # check if hand contains lead suit, if so, only those cards can be played
    has_lead_suit = False
    for card in hand:
        if card[-1:] == lead_suit:
            has_lead_suit = True
            sub_hand.append(card)
        # if hand has a jack, see if it's suit is left bower suit, if so, it's t_suit
        if t_suit == 'D':
            if lead_suit == t_suit:
                if card == 'JH':
                    has_lead_suit = True
                    sub_hand.append(card)
        if t_suit == 'H':
            if lead_suit == t_suit:
                if card == 'JD':
                    has_lead_suit = True
                    sub_hand.append(card)
        if t_suit == 'C':
            if lead_suit == t_suit:
                if card == 'JS':
                    has_lead_suit = True
                    sub_hand.append(card)
        if t_suit == 'S':
            if lead_suit == t_suit:
                if card == 'JC':
                    has_lead_suit = True
                    sub_hand.append(card)
    if not has_lead_suit:
        for card in hand:
            sub_hand.append(card)
    return sub_hand

def player_replace_dealer_card(hand, kat):
    # given dealer's hand, the kat, returns the new hand
    # print("Your current hand: {}".format(hand))
    print("The kat: {}".format(kat))
    while True:
        card_to_swap = input("Which card do you want to replace with kat? (write it out: eg 'KS'): ")
        try:
            hand.remove(card_to_swap)
            hand.append(kat)
        except:
            pass
        return hand
    return -1

def CPU_replace_dealer_card(hand, kat):
    # given CPU's hand, the kat, returns the new hand and card set away
    new_hand = hand
    suits = [card[:-1] for card in hand]
    # TODO: dumb logic for now, replace first card in hand, come back later to improve
    lost_card = new_hand[0]
    new_hand[0] = kat
    return new_hand, lost_card

def play_trick(cards_played, t_suit, l_suit, deck):
    # given four cards and t_suit, card1 being the lead, determine the winner (returns int = card#)
    cards = cards_played
    card1 = cards_played[1]
    card2 = cards_played[2]
    card3 = cards_played[3]
    card4 = cards_played[4]
    lead_suit = l_suit
    # first use hierarchy to find winner, if all zeros (no trump) then base of lead_suit
    hier = get_hierarchy(t_suit=t_suit, deck=deck)
    hierachies = []
    for card in cards.values():
        hierachies.append(hier[card])
    if hierachies == [0, 0, 0, 0]:
        # no trump in trick
        # TODO: placeholder variable
        winning_card_value = "9"
        if card1[-1] == lead_suit:
            card1value = card1[:-1]
            if values_dict[card1value] > values_dict[winning_card_value]:
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
        players = list(cards_played.keys())
        played = list(cards_played.values())
        played_winning_number = played.index(winning_card)
        winner = players[played_winning_number]
        print("Winning player: {}".format(winner))
        return winner
    else:
        # trump suit is involved in trick
        index_winner = hierachies.index(max(hierachies))
        print("index winner: {}".format(index_winner))
        players = list(cards_played.keys())
        print("players: {}".format(players))
        winner = players[index_winner]
        print("Winning player: {}".format(winner))
        return winner
    return -1

def CPU_pass_or_pick_up(h, kat):
    # given a hand and the kat card, returns 0 for pass and 1 for 'pick it up', 2 for 'picked up and alone'
    kat_suit = kat[-1]
    kat_suit_cards = 0
    for card in h:
        if card[-1] == kat_suit:
            kat_suit_cards += 1
    # CPU says 'pick it up' if they have 4 kat suit cards
    if kat_suit_cards > 3:
        return 1
    # CPU says 'pick it up and going alone' if they have 5 kat suit cards
    if kat_suit_cards > 4:
        return 2
    return 0

def CPU_pass_or_declare_trump(h, kat, kat_suit):
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
    # returns 0 if all passed, 1 is someone demanded it, also returns team who demanded it (0 or 1) and the kat_suit
    decision = 0 # player that called it up
    calling_team = 0 # 0 or 1 for team 1 or team 2
    kat_suit = kat[-1:]
    hands = [h1, h2, h3, h4]
    if d == 0:
        # dealer is player
        if CPU_pass_or_pick_up(h2, kat=kat):
            print("player 2 says pick it up to you")
            new_hand = player_replace_dealer_card(hand=h1, kat=kat)
            return 1, 0, kat_suit, new_hand
        print("player 2 says pass")
        if CPU_pass_or_pick_up(h3, kat=kat):
            print("player 3 (your partner) says pick it up to you")
            new_hand = player_replace_dealer_card(hand=h1, kat=kat)
            return 1, 1, kat_suit, new_hand
        print("player 3 says pass")
        if CPU_pass_or_pick_up(h4, kat=kat):
            print("player 4 says pick it up to you")
            new_hand = player_replace_dealer_card(hand=h1, kat=kat)
            return 1, 0, kat_suit, new_hand
        print("player 4 says pass")
        player_pass_or_pick = input("Back to you dealer: pass on kat or pick it up? (0 to pass, 1 to pick up): ")
        print("Your hand: {}".format(h1))
        if player_pass_or_pick == "1":
            new_hand = player_replace_dealer_card(hand=h1, kat=kat)
            return 1, 0, kat_suit, new_hand
        print("You turned it down, now to determine trump...")
        return 0, -1, -1, 0
    if d == 1:
        # dealer is CPU to left, player 2
        if CPU_pass_or_pick_up(h3, kat=kat):
            print("player 3 says pick it up to player 2")
            new_hand, lost_card = CPU_replace_dealer_card(hand=h2, kat=kat)
            return 1, 0, kat_suit, new_hand
        print("player 3 says pass")
        if CPU_pass_or_pick_up(h4, kat=kat):
            print("player 4 says pick it up to player 2")
            new_hand, lost_card = CPU_replace_dealer_card(hand=h2, kat=kat)
            return 1, 0, kat_suit, new_hand
        print("player 4 says pass")
        
        player_pass_or_pick = input("To you player: pass on kat or demand it up? (0 to pass, 1 to demand up): ")
        if player_pass_or_pick:
            new_hand, lost_card = CPU_replace_dealer_card(hand=h2, kat=kat)
            return 1, 0, kat_suit, new_hand
        if CPU_pass_or_pick_up(h2, kat=kat):
            print("player 2 as dealer picks it up")
            new_hand, lost_card = CPU_replace_dealer_card(hand=h2, kat=kat)
            return 1, 0, kat_suit, new_hand
        return 0, 0, kat_suit
        print("player 2 as dealer, turns it down... now to determine trump!")
        

    if d == 2:
        # dealer is CPU partner across from player
        if CPU_pass_or_pick_up(h4, kat=kat):
            print("player 4 says pick it up to player 3")
            new_hand, lost_card = CPU_replace_dealer_card(hand=h3, kat=kat)
            return 1, 0, kat_suit, new_hand
        player_pass_or_pick = input("To you player: pass on kat or demand it up? (0 to pass, 1 to demand up): ")
        if CPU_pass_or_pick_up(h2, kat=kat):
            print("player 2 says pick it up to player 3")
            new_hand, lost_card = CPU_replace_dealer_card(hand=h3, kat=kat)
            return 1, 0, kat_suit, new_hand
        if CPU_pass_or_pick_up(h3, kat=kat):
            print("player 3 as dealer picks it up")
            new_hand, lost_card = CPU_replace_dealer_card(hand=h3, kat=kat)
            return 1, 0, kat_suit, new_hand
        print("player 3 as dealer, turns it down... now to determine trump!")
    if d == 3:
        # dealer is CPU to right
        player_pass_or_pick = input("To you player: pass on kat or demand it up? (0 to pass, 1 to demand up): ")
        if CPU_pass_or_pick_up(h2, kat=kat):
            print("player 2 says pick it up to player 4")
            new_hand, lost_card = CPU_replace_dealer_card(hand=h4, kat=kat)
            return 1, 0, kat_suit, new_hand
        if CPU_pass_or_pick_up(h3, kat=kat):
            print("player 3 says pick it up to player 4")
            new_hand, lost_card = CPU_replace_dealer_card(hand=h4, kat=kat)
            return 1, 0, kat_suit, new_hand
        if CPU_pass_or_pick_up(h4, kat=kat):
            print("player 4 as dealer picks it up")
            new_hand, lost_card = CPU_replace_dealer_card(hand=h4, kat=kat)
            return 1, 0, kat_suit, new_hand
        print("player 4 as dealer, turns it down... now to determine trump!")
    return 0

def get_trump_suit_declared(h1, h2, h3, h4, d, kat, kat_suit):
    # kat has been rejected, given hands and current dealer, find the trump suit! 
    # error returns -1
    # returns t_suit and calling_team
    calling_team = -1
    if d == 0:
        # dealer is player
        player_2_decision = CPU_pass_or_declare_trump(h2, kat=kat, kat_suit=kat_suit)
        if player_2_decision:
            print("player 2 declares {}".format(player_2_decision))
            calling_team = 1
            return player_2_decision, calling_team
        print("player 2 passes")

        player_3_decision = CPU_pass_or_declare_trump(h3, kat=kat, kat_suit=kat_suit)
        if player_3_decision:
            print("player 3 (your partner) declares {}".format(player_3_decision))
            calling_team = 0
            return player_3_decision, calling_team
        print("player 3 passes")

        player_4_decision = CPU_pass_or_declare_trump(h4, kat=kat, kat_suit=kat_suit)
        if player_4_decision:
            print("player 4 declares {}".format(player_4_decision))
            calling_team = 1
            return player_4_decision, calling_team
        print("player 4 passes")

        forced_dealer = input("Back to you dealer: you have to declare a suit! (S, D, H, C): ")
        calling_team = 0
        return forced_dealer, calling_team

    if d == 1:
        # dealer is CPU left of player (player 2)
        player_3_decision = CPU_pass_or_declare_trump(h3, kat=kat, kat_suit=kat_suit)
        if player_3_decision:
            print("player 3 (your partner) declares {}".format(player_3_decision))
            calling_team = 0
            return player_3_decision, calling_team
        print("player 3 passes")

        player_4_decision = CPU_pass_or_declare_trump(h4, kat=kat, kat_suit=kat_suit)
        if player_4_decision:
            print("player 4 declares {}".format(player_4_decision))
            calling_team = 1
            return player_4_decision, calling_team
        print("player 4 passes")

        player_pass_or_pick = input("On to you player 1, want to call it? (0 for pass; S, D, H, C to declare trump): ")
        if player_pass_or_pick:
            calling_team = 0
            return player_pass_or_pick, calling_team
        print("player 1 passes")

        print("Player 2 as dealer is forced to declare the trump suit!")
        player_2_decision = CPU_pass_or_declare_trump(h2, kat=kat, kat_suit=kat_suit)
        if player_2_decision:
            calling_team = 1
            return player_2_decision, calling_team
        print("player 2 arbitrary calls Spades")
        calling_team = 1
        return "S", calling_team

    if d == 2:
        # dealer is CPU parter of player
        player_4_decision = CPU_pass_or_declare_trump(h4, kat=kat, kat_suit=kat_suit)
        if player_4_decision:
            print("player 4 declares {}".format(player_4_decision))
            calling_team = 1
            return player_4_decision, calling_team
        print("player 4 passes")

        player_pass_or_pick = input("On to you player 1, want to call it? (0 for pass; S, D, H, C to declare trump): ")
        if player_pass_or_pick:
            calling_team = 0
            return player_pass_or_pick, calling_team
        print("player 1 passes")

        player_2_decision = CPU_pass_or_declare_trump(h2, kat=kat, kat_suit=kat_suit)
        if player_2_decision:
            print("player 2 declares {}".format(player_2_decision))
            calling_team = 1
            return player_2_decision, calling_team
        print("player 2 passes")

        print("Player 3 as dealer is forced to declare the trump suit!")
        player_3_decision = CPU_pass_or_declare_trump(h3, kat=kat, kat_suit=kat_suit)
        if player_3_decision:
            print("player 3 declares {}".format(player_3_decision))
            calling_team = 0
            return player_3_decision, calling_team
        print("player 3 arbitrary calls Spades")
        calling_team = 0
        return "S", calling_team

    if d == 3:
        # dealer is CPU right of player
        player_pass_or_pick = input("On to you dealer, want to call it? (0 for pass; S, D, H, C to declare trump): ")
        if player_pass_or_pick:
            calling_team = 0
            return player_pass_or_pick, calling_team
        print("player 1 passes")
        
        player_2_decision = CPU_pass_or_declare_trump(h2, kat=kat, kat_suit=kat_suit)
        if player_2_decision:
            print("player 2 declares {}".format(player_2_decision))
            calling_team = 1
            return player_2_decision, calling_team
        print("player 2 passes")

        player_3_decision = CPU_pass_or_declare_trump(h3, kat=kat, kat_suit=kat_suit)
        if player_3_decision:
            print("player 3 (your partner) declares {}".format(player_3_decision))
            calling_team = 0
            return player_3_decision, calling_team
        print("player 3 passes")

        print("Player 4 as dealer is forced to declare the trump suit!")
        player_4_decision = CPU_pass_or_declare_trump(h4, kat=kat, kat_suit=kat_suit)
        if player_4_decision:
            print("player 4 declares {}".format(player_4_decision))
            calling_team = 0
            return player_4_decision, calling_team
        print("player 4 arbitrary calls Spades")
        calling_team = 1
        return "S", calling_team

    return -1

def score_round(t1_score, t2_score, t1_tricks, t2_tricks, calling_team, alone):
    # given the current scores, the tricks each side took, the calling team, and if alone
    # returns the two scores
    team_1_score = t1_score
    team_2_score = t2_score
    # calling team is 0 or 1
    # alone is 0 (False) or 1 (True)
    if t1_tricks > t2_tricks:
        # team one won this round

        if calling_team == 1:
            return team_1_score+2, team_2_score
        if t1_tricks == 3:
            return team_1_score+1, team_2_score
        if t1_tricks == 4:
            return team_1_score+1, team_2_score
        if t1_tricks == 5:
            if alone:
                return team_1_score+4, team_2_score
            return team_1_score+2, team_2_score
    if t2_tricks > t1_tricks:
        # team two won this round

        if calling_team == 0:
            return team_1_score, team_2_score+2
        if t2_tricks == 3:
            return team_1_score, team_2_score+1
        if t2_tricks == 4:
            return team_1_score, team_2_score+1
        if t2_tricks == 5:
            if alone:
                return team_1_score, team_2_score+4
            return team_1_score, team_2_score+2
    # if error occured
    return -1, -1

def player_play_card(hand, l_suit, t_suit):
    # given player's hand and lead's suit, asks for which card to play, returns card chosen
    print("Your hand: {}".format(hand))
    options = get_options(hand=hand, lead_suit=l_suit, t_suit=t_suit)
    print("Your options: {}".format(options))
    choice = input("pick a card (0 to {} integer): ".format(len(options) - 1))
    card_chosen = options[int(choice)]
    return card_chosen

def CPU_play_card(hand, l_suit, t_suit, cards_played):
    # CPU considers hand, lead suit, trump suit, and list of other cards played so far
    # figures out what they can play and returns that card
    print("CPU hand: {}".format(hand))
    # if first to play in a trick, YOU CAN PLAY WHATEVER YOU WANT
    if l_suit == None:
        options = hand
    else:
        options = get_options(hand=hand, lead_suit=l_suit, t_suit=t_suit)
    print("CPU options: {}".format(options))
    # TODO: fix line below, its hardcoded for the first available option, need some intelligence here...
    card_chosen = options[0]
    return card_chosen

def play_round(h1, h2, h3, h4, t_suit, starting_player, deck):
    # walks through the process, given the starting hands (0, 1, 2, 3), t_suit, and starting player
    # returns winning team and number of tricks each team took
    t1_tricks = 0
    t2_tricks = 0
    winning_team = None
    print("player {} starts".format(starting_player + 1))
    lead_player = starting_player
    played_cards = {}
    lead_card = None
    lead_suit = None
    for card in range(0, 5):
        if lead_player == 0:
            # player starts
            print("Player 1 goes first")
            print_hand(h1)
            card1 = player_play_card(hand=h1, l_suit=None, t_suit=t_suit)
            played_cards[1] = card1
            lead_card = card1
            lead_suit = card1[-1:]
            h1.remove(card1)
            print("Player 1 plays {} \n".format(card1))
            lead_suit = card1[-1:]
            # other players 
            card2 = CPU_play_card(hand=h2, l_suit=lead_suit, t_suit=t_suit, cards_played=played_cards)
            played_cards[2] = card2
            h2.remove(card2)
            print("Player 2 plays {} \n".format(card2))
            card3 = CPU_play_card(hand=h3, l_suit=lead_suit, t_suit=t_suit, cards_played=played_cards)
            played_cards[3] = card3
            h3.remove(card3)
            print("Player 3 plays {} \n".format(card3))
            card4 = CPU_play_card(hand=h4, l_suit=lead_suit, t_suit=t_suit, cards_played=played_cards)
            played_cards[4] = card4
            h4.remove(card4)
            print("Player 4 plays {} \n".format(card4))
        if lead_player == 1:
            # CPU to left starts
            card2 = CPU_play_card(hand=h2, l_suit=None, t_suit=t_suit, cards_played=played_cards)
            played_cards[2] = card2
            lead_card = card2
            lead_suit = card2[-1:]
            h2.remove(card2)
            print("Player 2 plays {} \n".format(card2))
            lead_suit = card2[-1:]
            # other players 
            card3 = CPU_play_card(hand=h3, l_suit=lead_suit, t_suit=t_suit, cards_played=played_cards)
            played_cards[3] = card3
            h3.remove(card3)
            print("Player 3 plays {} \n".format(card3))
            card4 = CPU_play_card(hand=h4, l_suit=lead_suit, t_suit=t_suit, cards_played=played_cards)
            played_cards[4] = card4
            h4.remove(card4)
            print("Player 4 plays {} \n".format(card4))
            print_hand(h1)
            card1 = player_play_card(hand=h1, l_suit=lead_suit, t_suit=t_suit)
            played_cards[1] = card1
            h1.remove(card1)
            print("Player 1 plays {} \n".format(card1))
        if lead_player == 2:
            # CPU partner across starts
            card3 = CPU_play_card(hand=h3, l_suit=None, t_suit=t_suit, cards_played=played_cards)
            played_cards[3] = card3
            lead_card = card3
            lead_suit = card3[-1:]
            h3.remove(card3)
            print("Player 3 plays {}".format(card3))
            lead_suit = card3[-1:]
            # other players 
            card4 = CPU_play_card(hand=h4, l_suit=lead_suit, t_suit=t_suit, cards_played=played_cards)
            played_cards[4] = card4
            h4.remove(card4)
            print("Player 4 plays {}".format(card4))
            print_hand(h1)
            card1 = player_play_card(hand=h1, l_suit=lead_suit, t_suit=t_suit)
            played_cards[1] = card1
            h1.remove(card1)
            print("Player 1 plays {}".format(card1))
            card2 = CPU_play_card(hand=h2, l_suit=lead_suit, t_suit=t_suit, cards_played=played_cards)
            played_cards[2] = card2
            h2.remove(card2)
            print("Player 2 plays {}".format(card2))
        if lead_player == 3:
            # CPU to right starts
            card4 = CPU_play_card(hand=h4, l_suit=None, t_suit=t_suit, cards_played=played_cards)
            played_cards[4] = card4
            lead_card = card4
            lead_suit = card4[-1:]
            h4.remove(card4)
            print("Player 4 plays {}".format(card4))
            lead_suit = card4[-1:]
            # other players
            print_hand(h1)
            card1 = player_play_card(hand=h1, l_suit=lead_suit, t_suit=t_suit)
            played_cards[1] = card1
            h1.remove(card1)
            print("Player 1 plays {}".format(card1))
            card2 = CPU_play_card(hand=h2, l_suit=lead_suit, t_suit=t_suit, cards_played=played_cards)
            played_cards[2] = card2
            h2.remove(card2)
            print("Player 2 plays {}".format(card2))
            card3 = CPU_play_card(hand=h3, l_suit=lead_suit, t_suit=t_suit, cards_played=played_cards)
            played_cards[3] = card3
            h3.remove(card3)
            print("Player 3 plays {}".format(card3))
        print("Cards played: {}".format(played_cards))
        print(played_cards)
        winning_player = play_trick(cards_played=played_cards, t_suit=t_suit, l_suit=lead_suit, deck=deck)

        if winning_player == 1:
            t1_tricks += 1
        if winning_player == 2:
            t2_tricks += 1
        if winning_player == 3:
            t1_tricks += 1
        if winning_player == 4:
            t2_tricks += 1
        # lead for next trick should be the winner of this trick
        lead_player = winning_player - 1
    if t1_tricks > t2_tricks:
        winning_team = 0
    if t1_tricks < t2_tricks:
        winning_team = 1
    return winning_team, t1_tricks, t2_tricks

# main

def play_euchre():
    # main function, progresses game
    A = input("Welcome")
    B = input("press any key to deal out the hands (you start as dealer)... ")
    team_1_score = 0
    team_2_score = 0
    hand_counter = 0
    dealer = 0

    # Init deck for terminal viewed cards
    deck = Deck()
    # play until one team has at least 10 points
    while team_1_score < 10 and team_2_score < 10:
        # new deck of cards to shuffle
        deck = get_deck(suits=suits, values=values)
        # initiate blank trump suit for this hand
        trump_suit = ''
        # deal the hands, kat, three extra
        four_hands, kat, three_left = deal_four_hands(deck=deck)
        kat_suit = kat[-1:]
        hand1 = four_hands[0]
        hand2 = four_hands[1]
        hand3 = four_hands[2]
        hand4 = four_hands[3]
        print("Your hand: {}".format(hand1))
        print_hand(hand1)
        print("The top of the kitty: {}".format(kat))
        print_hand([kat])
        picked_up, calling_team, t_suit, new_hand = get_kat_decision(hand1, hand2, hand3, hand4, d=dealer, kat=kat)
        # if kat rejected, go to next phase
        if not picked_up:
            t_suit, calling_team = get_trump_suit_declared(hand1, hand2, hand3, hand4, d=dealer, kat=kat, kat_suit=kat_suit)
        # by this point, the kat was picked up or the trump suit was declared
        print("trump suit: {}".format(t_suit))

        # starting player is always to left of dealer
        starting = dealer+1
        # play the round
        deck = get_deck(suits=suits, values=values)
        win_team, t1_ts, t2_ts = play_round(h1=hand1, h2=hand2, h3=hand3, h4=hand4, t_suit=t_suit, starting_player=starting, deck=deck)

        team_1_score, team_2_score = score_round(t1_score=team_1_score, t2_score=team_2_score, t1_tricks=t1_ts, t2_tricks=t2_ts, calling_team=calling_team, alone=0)
        # hand is over, change dealer
        dealer += 1
        # reset dealer to player 1 if player 4 just went as dealer
        if dealer == 3:
            dealer = 0

        print("TEAM 1 SCORE: {}".format(team_1_score))
        print("TEAM 2 SCORE: {}".format(team_2_score))

    # win condition
    if team_1_score > 10:
        print("team 1 wins!")
        return 0
    if team_2_score > 10:
        print("team 2 wins!")
        return 1
    return -1

# call main function
play_euchre()

# tests
cards_played = {2: 'QD', 3: 'AD', 4: '10S', 1: 'AH'}
t_suit = "C"
l_suit = "D"
deck = get_deck(values=values, suits=suits)
print(play_trick(cards_played, t_suit, l_suit, deck))
