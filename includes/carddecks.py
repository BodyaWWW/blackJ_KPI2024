#!/usr/bin/env python
from random import shuffle
from playingcard import PlayingCard


class CardDecks(object):


    def __init__(self, num_of_decks=1):

        self.__card_decks = []
        for num in range(0, num_of_decks):
            for suit in range(0, 4):
                for rank in range(1, 14):
                    instance = PlayingCard(rank, suit)
                    self.__card_decks.append(instance)
        self.shuffle()

    def shuffle(self):

        shuffle(self.__card_decks)

    def pop(self):

        return self.__card_decks.pop()

    def length(self):

        return len(self.__card_decks)


class TestingCardDeck(object):


    def __init__(self):

        self.__card_decks = []

        for x in range(1, 52):  # Fill up a deck of dummies
            instance = PlayingCard(7, 1)
            self.__card_decks.append(instance)

        self.__card_decks.append(PlayingCard(4, 1))
        self.__card_decks.append(PlayingCard(1, 0))
        self.__card_decks.append(PlayingCard(8, 3))
        self.__card_decks.append(PlayingCard(1, 3))
        self.__card_decks.append(PlayingCard(1, 2))

        self.__card_decks.append(PlayingCard(6, 2))
        self.__card_decks.append(PlayingCard(8, 1))
        self.__card_decks.append(PlayingCard(4, 1))
        self.__card_decks.append(PlayingCard(10, 0))

        self.__card_decks.append(PlayingCard(6, 2))
        self.__card_decks.append(PlayingCard(10, 1))
        self.__card_decks.append(PlayingCard(4, 1))
        self.__card_decks.append(PlayingCard(1, 0))

        self.__card_decks.append(PlayingCard(6, 2))
        self.__card_decks.append(PlayingCard(2, 1))
        self.__card_decks.append(PlayingCard(4, 1))
        self.__card_decks.append(PlayingCard(2, 0))

        self.__card_decks.append(PlayingCard(12, 1))
        self.__card_decks.append(PlayingCard(4, 1))
        self.__card_decks.append(PlayingCard(2, 0))
        self.__card_decks.append(PlayingCard(6, 2))
        self.__card_decks.append(PlayingCard(8, 1))
        self.__card_decks.append(PlayingCard(4, 1))
        self.__card_decks.append(PlayingCard(8, 0))

    def pop(self):

        return self.__card_decks.pop()

    def length(self):

        return len(self.__card_decks)
