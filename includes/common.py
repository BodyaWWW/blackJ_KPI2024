#!/usr/bin/env python
import sys
import os
import pygame
import inspect
MAIN_DIR = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(1, os.path.join(MAIN_DIR, 'includes'))
from globals import *
from playingcard import PlayingCard

def plot_players_hands(screen,
                       player_pos_start,
                       player_hands,
                       double_downs,
                       hands_status):

    logging.debug(inspect.stack()[0][3] + ': enter')

    player_x_pos, player_y_pos = player_pos_start
    image_db = ImageDB.get_instance()
    for index_x, hand in enumerate(player_hands):
        for index_y, card in enumerate(hand):
            image = BlackJackCardFormatter.get_instance(IMAGE_PATH_CARDS).get_string(card)

            if index_y == 2 and len(hand) == 3 and double_downs[index_x]:
                # rotate the third card if we have a double down in current hand
                screen.blit(pygame.transform.rotate(image_db.get_image(image), 90),
                            (player_x_pos, player_y_pos))
            else:
                screen.blit(image_db.get_image(image), (player_x_pos, player_y_pos))
            player_x_pos += GAP_BETWEEN_CARDS
            player_y_pos -= 14

        x_offset = -50
        y_offset = -40
        if index_x == 0:
            hand = 'first_hand_'
        else:
            hand = 'second_hand_'

        if hands_status[hand + 'blackjack']:
            screen.blit(image_db.get_image(IMAGE_PATH + "blackjack.png"),
                        (player_x_pos + x_offset, player_y_pos + y_offset))
        elif hands_status[hand + 'win']:
            screen.blit(image_db.get_image(IMAGE_PATH + "you_win.png"),
                        (player_x_pos + x_offset, player_y_pos + y_offset))
        elif hands_status[hand + 'push']:
            screen.blit(image_db.get_image(IMAGE_PATH + "push.png"),
                        (player_x_pos + x_offset, player_y_pos + y_offset))
        elif hands_status[hand + 'loose']:
            screen.blit(image_db.get_image(IMAGE_PATH + "you_loose.png"),
                        (player_x_pos + x_offset, player_y_pos + y_offset))
        elif hands_status[hand + 'busted']:
            screen.blit(image_db.get_image(IMAGE_PATH + "busted.png"),
                        (player_x_pos + x_offset, player_y_pos + y_offset))
        player_x_pos, player_y_pos = player_pos_start
        player_x_pos += GAP_BETWEEN_SPLIT


def plot_dealers_hand(screen,
                      dealer_card_start_pos,
                      dealer_cards,
                      first_card_hidden):

    logging.debug(inspect.stack()[0][3] + ': enter')

    dealer_x_pos, dealer_y_pos = dealer_card_start_pos
    image_db = ImageDB.get_instance()
    for card in dealer_cards:
        if first_card_hidden is True:
            # Show first dealer card hidden
            screen.blit(image_db.get_image(IMAGE_PATH_CARDS + CARDBACK_FILENAME),
                        (dealer_x_pos, dealer_y_pos))
        else:
            image = BlackJackCardFormatter.get_instance(IMAGE_PATH_CARDS).get_string(card)
            screen.blit(image_db.get_image(image), (dealer_x_pos, dealer_y_pos))
        first_card_hidden = False
        dealer_x_pos += GAP_BETWEEN_CARDS
        dealer_y_pos += 14


def plot_chips(screen,
               player_cash,
               chips_image_width,
               visible):

    logging.debug(inspect.stack()[0][3] + ': enter')
    chips_x_pos, chips_y_pos = CHIPS_START_POS
    gap = chips_image_width + GAP_BETWEEN_CHIPS
    image_db = ImageDB.get_instance()
    if visible:
        if player_cash >= 5:
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_5_FILENAME_ON),
                        (chips_x_pos, chips_y_pos))
        if player_cash >= 10:
            chips_x_pos += gap
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_10_FILENAME_ON),
                        (chips_x_pos, chips_y_pos))
        if player_cash >= 50:
            chips_x_pos -= gap
            chips_y_pos += gap
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_50_FILENAME_ON),
                        (chips_x_pos, chips_y_pos))
        if player_cash >= 100:
            chips_x_pos += gap
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_100_FILENAME_ON),
                        (chips_x_pos, chips_y_pos))
    else:
        if player_cash >= 5:
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_5_FILENAME_OFF),
                        (chips_x_pos, chips_y_pos))
        if player_cash >= 10:
            chips_x_pos += gap
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_10_FILENAME_OFF),
                        (chips_x_pos, chips_y_pos))
        if player_cash >= 50:
            chips_x_pos -= gap
            chips_y_pos += gap
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_50_FILENAME_OFF),
                        (chips_x_pos, chips_y_pos))
        if player_cash >= 100:
            chips_x_pos += gap
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_100_FILENAME_OFF),
                        (chips_x_pos, chips_y_pos))


def plot_bets(screen, player_bets):


    logging.debug(inspect.stack()[0][3] + ': enter')
    image_db = ImageDB.get_instance()
    chip_x_pos = 30
    chip_y_pos = 360
    for bet in player_bets:
        for chip in bet:
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + 'chip_{0}_w85h85.png'.format(chip)),
                        (chip_x_pos, chip_y_pos))
            chip_y_pos += 8
        chip_y_pos = 360
        chip_x_pos += 50


def plot_buttons(screen, button_status):

    logging.debug(inspect.stack()[0][3] + ': enter')
    button_x_pos, button_y_pos = BUTTONS_START_POS
    image_db = ImageDB.get_instance()
    if button_status.play is True:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + PLAY_BUTTON_FILENAME_ON),
                    (button_x_pos, button_y_pos))
    else:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + PLAY_BUTTON_FILENAME_OFF),
                    (button_x_pos, button_y_pos))
    button_x_pos += GAP_BETWEEN_BUTTONS

    if button_status.undo_bet is True:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + UNDO_BET_BUTTON_FILENAME_ON),
                    (button_x_pos, button_y_pos))
    else:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + UNDO_BET_BUTTON_FILENAME_OFF),
                    (button_x_pos, button_y_pos))
    button_x_pos += GAP_BETWEEN_BUTTONS

    if button_status.hit is True:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + HIT_BUTTON_FILENAME_ON),
                    (button_x_pos, button_y_pos))
    else:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + HIT_BUTTON_FILENAME_OFF),
                    (button_x_pos, button_y_pos))
    button_x_pos += GAP_BETWEEN_BUTTONS

    if button_status.stand is True:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + STAND_BUTTON_FILENAME_ON),
                    (button_x_pos, button_y_pos))
    else:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + STAND_BUTTON_FILENAME_OFF),
                    (button_x_pos, button_y_pos))
    button_x_pos += GAP_BETWEEN_BUTTONS

    if button_status.split is True:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + SPLIT_BUTTON_FILENAME_ON),
                    (button_x_pos, button_y_pos))
    else:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + SPLIT_BUTTON_FILENAME_OFF),
                    (button_x_pos, button_y_pos))
    button_x_pos += GAP_BETWEEN_BUTTONS

    if button_status.double_down is True:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + DOUBLE_DOWN_BUTTON_FILENAME_ON),
                    (button_x_pos, button_y_pos))
    else:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + DOUBLE_DOWN_BUTTON_FILENAME_OFF),
                    (button_x_pos, button_y_pos))
    button_x_pos += GAP_BETWEEN_BUTTONS


def plot_results(screen, text_font, message):

    logging.debug(inspect.stack()[0][3] + ': enter')

    assert isinstance(message, str)
    text_to_plot = text_font.render(message, False, GOLD_COLOR)
    x_pos, y_pos = STATUS_START_POS
    screen.blit(text_to_plot, (x_pos, y_pos + 50))


def get_value_of_players_hand(hand):

    logging.debug(inspect.stack()[0][3] + ': enter')
    assert isinstance(hand, list)
    summary = 0
    num_of_soft_aces = 0
    for card in hand:
        assert isinstance(card, PlayingCard)
        rank = card.get_rank()
        if rank > 10:
            # Treat all face cards as 10
            summary += 10
            logging.debug(inspect.stack()[0][3] + ': face')
        elif rank == 1 and summary <= 10:
            # If an ace, start treating as Soft hand "high ace"
            summary += 11
            num_of_soft_aces += 1
            logging.debug(inspect.stack()[0][3] + ': soft ace')
        else:
            summary += rank
            logging.debug(inspect.stack()[0][3] + ': add rank {0} to summary givs {1}'.format(rank, summary))

        if num_of_soft_aces and summary > 21:
            # turn soft to hard ace , decrease with 10 since we already accounted for 11
            summary -= 10
            num_of_soft_aces -= 1
            logging.debug(inspect.stack()[0][3] + ': busted, toggle soft to hard ace')

    return summary


def get_value_of_dealers_hand(hand):

    logging.debug(inspect.stack()[0][3] + ': enter')
    assert isinstance(hand, list)
    summary = 0
    hard_ace = 0
    for card in hand:
        assert isinstance(card, PlayingCard)
        rank = card.get_rank()
        if rank > 10:
            # Treat all face cards as 10
            summary += 10
            logging.debug(inspect.stack()[0][3] + ': face')
        elif rank == 1:
            # If the card is an ace and if the total summary of the current hand will be 17 or more
            # but less than 21 the dealer has to count the ace as a "soft" ace.
            if 17 <= (summary + 11) < 22:
                summary += 11
                logging.debug(inspect.stack()[0][3] + ': soft ace')
            else:
                # Save the ace for later evaluation when more cards are added to the summary
                hard_ace = 1
                summary += 1
                logging.debug(inspect.stack()[0][3] + ': hard ace')
                continue
        else:
            summary += rank
            logging.debug(inspect.stack()[0][3] + ': add rank {0} to summary givs {1}'.format(rank, summary))

        if hard_ace and 17 <= (summary + hard_ace * 10) < 22:
            # turn hard ace to soft, increase with 10 since 1 is already in the summary, total 11
            summary += 10
            logging.debug(inspect.stack()[0][3] + ': toggle hard to soft ace')

    return summary


def is_cut_passed(shoe_of_decks):

    logging.debug(inspect.stack()[0][3] + ': enter')

    status = False
    if shoe_of_decks is None or shoe_of_decks.length() < (NUM_OF_DECKS * 52 * 0.18):
        logging.debug(inspect.stack()[0][3] + 'Passed the "cut" in the shoe')
        status = True
    return status


def is_possible_split(player_cards):

    logging.debug(inspect.stack()[0][3] + ': enter')

    if len(player_cards) != 2:
        return False
    if player_cards[0].get_rank() != player_cards[1].get_rank():
        return False
    else:
        return True


def can_double_bet(player_bets, player_cash):

    if player_cash < sum(player_bets[0]):
        return False
    else:
        return True


class ImageDB:

    instance = None

    @classmethod
    def get_instance(cls):

        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):
        logging.info(inspect.stack()[0][3] + ':' + 'ImageDb instance created')
        self.image_library = {}

    def get_image(self, path):

        logging.debug(inspect.stack()[0][3] + ':' + 'enter')

        image = self.image_library.get(path)
        if image is None:
            logging.info(inspect.stack()[0][3] + ':' + path)
            canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
            image = pygame.image.load(canonicalized_path)
            self.image_library[path] = image
        return image


class SoundDB:

    instance = None

    @classmethod
    def get_instance(cls):

        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):
        logging.info(inspect.stack()[0][3] + ':' + 'SoundDb instance created')
        self.sound_library = {}

    def get_sound(self, path):

        logging.debug(inspect.stack()[0][3] + ':' + 'enter')

        sound = self.sound_library.get(path)
        if sound is None:
            logging.info(inspect.stack()[0][3] + ':' + path)
            canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
            sound = pygame.mixer.Sound(canonicalized_path)
            self.sound_library[path] = sound
        return sound


class BlackJackCardFormatter:

    instance = None

    @classmethod
    def get_instance(cls, path=''):

        if cls.instance is None:
            cls.instance = cls(path)
        return cls.instance

    def __init__(self, path):

        logging.info(inspect.stack()[0][3] + ':' + 'BlackJackCardFormatter instance created')
        self.path = path
        self.card_rank = ["Invalid", "ace", "2", "3", "4", "5", "6", "7",
                          "8", "9", "10", "jack", "queen", "king"]
        self.card_suit = ["spades", "clubs", "diamonds", "hearts"]

    def get_string(self, card):

        logging.debug(inspect.stack()[0][3] + ':' + 'enter')

        image = self.path + self.card_rank[card.get_rank()] + "_of_" \
            + self.card_suit[card.get_suit()] + ".png"
        return image


class ButtonCollideArea:

    instance = None

    @classmethod
    def get_instance(cls, common_vars):

        if cls.instance is None:
            cls.instance = cls(common_vars)
        return cls.instance

    def __init__(self, common_vars):

        logging.info(inspect.stack()[0][3] + ':' + 'ButtonCollideArea instance created')
        button_x_pos, button_y_pos = BUTTONS_START_POS

        self.play_button_area = pygame.Rect(button_x_pos,
                                            button_y_pos,
                                            common_vars.button_image_width,
                                            common_vars.button_image_height)
        button_x_pos += GAP_BETWEEN_BUTTONS
        self.undo_bet_button_area = pygame.Rect(button_x_pos,
                                                button_y_pos,
                                                common_vars.button_image_width,
                                                common_vars.button_image_height)
        button_x_pos += GAP_BETWEEN_BUTTONS
        self.hit_button_area = pygame.Rect(button_x_pos,
                                           button_y_pos,
                                           common_vars.button_image_width,
                                           common_vars.button_image_height)
        button_x_pos += GAP_BETWEEN_BUTTONS
        self.stand_button_area = pygame.Rect(button_x_pos,
                                             button_y_pos,
                                             common_vars.button_image_width,
                                             common_vars.button_image_height)
        button_x_pos += GAP_BETWEEN_BUTTONS
        self.split_button_area = pygame.Rect(button_x_pos,
                                             button_y_pos,
                                             common_vars.button_image_width,
                                             common_vars.button_image_height)
        button_x_pos += GAP_BETWEEN_BUTTONS
        self.double_down_button_area = pygame.Rect(button_x_pos,
                                                   button_y_pos,
                                                   common_vars.button_image_width,
                                                   common_vars.button_image_height)


class ChipsCollideArea:

    instance = None

    @classmethod
    def get_instance(cls, common_vars):

        if cls.instance is None:
            cls.instance = cls(common_vars)
        return cls.instance

    def __init__(self, common_vars):

        logging.info(inspect.stack()[0][3] + ':' + 'ChipsCollideArea instance created')
        chips_x_pos, chips_y_pos = CHIPS_START_POS
        gap = common_vars.chips_image_width + GAP_BETWEEN_CHIPS
        self.chip_5_area = pygame.Rect(chips_x_pos,
                                       chips_y_pos,
                                       common_vars.chips_image_width,
                                       common_vars.chips_image_height)
        chips_x_pos += gap
        self.chip_10_area = pygame.Rect(chips_x_pos,
                                        chips_y_pos,
                                        common_vars.chips_image_width,
                                        common_vars.chips_image_height)
        chips_x_pos -= gap
        chips_y_pos += gap
        self.chip_50_area = pygame.Rect(chips_x_pos,
                                        chips_y_pos,
                                        common_vars.chips_image_width,
                                        common_vars.chips_image_height)
        chips_x_pos += gap
        self.chip_100_area = pygame.Rect(chips_x_pos,
                                        chips_y_pos,
                                        common_vars.chips_image_width,
                                        common_vars.chips_image_height)


class CommonVariables:

    instance = None

    @classmethod
    def get_instance(cls):

        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):

        self.done = None
        self.screen = None
        self.shoe_of_decks = None
        self.player_hands = None
        self.hands_status = None
        self.double_downs = None
        self.dealer_cards = None
        self.dealer_last_hand = None
        self.player_deal = None
        self.player_hit = None
        self.player_cash = None
        self.player_bets = None
        self.bets_pos = None
        self.game_rounds = None
        self.text_font = None
        self.first_card_hidden = None
        self.pause_time = None
        self.button_image_width = None
        self.button_image_height = None
        self.chips_image_width = None
        self.chips_image_height = None


class ButtonStatus:

    instance = None

    @classmethod
    def get_instance(cls):

        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):

        self.play = False
        self.undo_bet = False
        self.hit = False
        self.stand = False
        self.split = False
        self.double_down = False

    def reset(self):

        self.play = False
        self.undo_bet = False
        self.hit = False
        self.stand = False
        self.split = False
        self.double_down = False
