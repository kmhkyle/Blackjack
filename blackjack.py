from random import *
import time


suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
values = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
deck, game_deck = [], []
play_again = True


class Card:
    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value


def gen_deck():
    for suit in suits:
        for i in range(len(ranks)):
            deck.append(Card(suit, ranks[i], values[i]))
    shuffle(deck)


def format_cards(x, y):
    global p_hand
    global d_hand
    p_hand = []
    d_hand = []
    for c in x:
        p_hand.append(c.rank + ' of ' + c.suit)
    for c in y:
        d_hand.append(c.rank + ' of ' + c.suit)


def sent_formatting(hand, person):
    if len(hand) < 3:
        if person == 'dealer':
            line = 'The ' + person + ' has a ' + hand[0] + ' and a ' + hand[1]
            return line
        elif person == 'You':
            line = person + ' have a ' + hand[0] + ' and a ' + hand[1]
            return line
    else:
        comma = ', a '.join(hand[:len(hand) - 1])
        line = 'You have a ', comma + ', and a ', hand[len(hand) - 1]
        return ''.join(line)


def hand_value(hand):
    global h_value
    h_value = 0
    check_ace = []
    num_ace = 0
    for c in hand:
        h_value += c.value
        check_ace.append(c.rank)
    if h_value > 21:
        for rank in check_ace:
            if rank == 'Ace':
                num_ace += 1
        h_value -= (num_ace * 10)
    return h_value


def end():
    global play_again
    no_input_selected = True
    print('Would you like to play again? (y/n)')
    while no_input_selected:
        play_again = input()
        if play_again == 'y':
            no_input_selected = False
            game()
        elif play_again == 'n':
            print('Thanks for playing!')
            no_input_selected = False
            play_again = False
        else:
            print('Please enter y or n')


def game():
    while play_again:
        game_over = False
        dealers_turn = True
        gen_deck()
        players_hand, dealers_hand = [], []
        dealers_hand.append(deck.pop(0))
        dealers_hand.append(deck.pop(0))
        players_hand.append(deck.pop(0))
        players_hand.append(deck.pop(0))
        format_cards(players_hand, dealers_hand)
        print('The dealer shows a', d_hand[0], 'and one face down card')
        time.sleep(1)
        print('You have a', p_hand[0], 'and a', p_hand[1], '(Total =', str(hand_value(players_hand)) + ')')
        time.sleep(1)
        if h_value == 21:
            game_over = True
            print('you win!')
            end()
        while game_over is False:
            print('Would you like to hit or stand? (h for hit, s for stand)')
            answer = input()
            if answer == 'h':
                players_hand.append(deck.pop(0))
                format_cards(players_hand, dealers_hand)
                print(sent_formatting(p_hand, 'You') + ' (Total = ' + str(hand_value(players_hand)) + ')' )
                time.sleep(1)
                hand_value(players_hand)
                if h_value == 21:
                    game_over = True
                    print('Blackjack, you win!')
                    end()
                elif h_value > 21:
                    game_over = True
                    print('You bust, you lose!')
                    end()
            elif answer == 's':
                game_over = True
                dealers_turn = True
                print('The dealer flips the other card')
            else:
                print('please enter a letter')
        while dealers_turn:
            time.sleep(1)
            format_cards(players_hand, dealers_hand)
            print(sent_formatting(d_hand, 'dealer'), '(Total = ' + str(hand_value(dealers_hand)) + ')')
            if hand_value(dealers_hand) > 21:
                time.sleep(1)
                print('The dealer busts, you win!')
                dealers_turn = False
                end()
            elif hand_value(dealers_hand) > hand_value(players_hand):
                    time.sleep(1)
                    print('The dealers hand is larger than yours, you lose!')
                    dealers_turn = False
                    end()
            elif hand_value(dealers_hand) >= 17:
                if hand_value(dealers_hand) == hand_value(players_hand):
                    time.sleep(1)
                    print('You tied with the dealer!')
                    dealers_turn = False
                    end()
                else:
                    time.sleep(1)
                    print('Your hand is larger than the dealer\'s, you win!')
                    dealers_turn = False
                    end()
            else:
                dealers_hand.append(deck.pop(0))
                time.sleep(1)
                print('The dealer hits')

game()
