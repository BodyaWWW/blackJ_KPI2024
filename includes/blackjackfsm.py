#!/usr/bin/env python

import sys
import os

MAIN_DIR = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(1, os.path.join(MAIN_DIR, 'includes'))
from common import *
from carddecks import CardDecks


class State(object):

    def next_state(self, state):

        self.__class__ = state

    def get_state(self):

        temp = str(self.__class__).strip('\'>').split('.')
        return temp[2]


class InitialState(State):

    def __call__(self, common_vars, button_status):

        logging.info(type(self).__name__ + ': Credits: {0}'.format(common_vars.player_cash))

        common_vars.hands_status = {'first_hand_blackjack': False,
                                    'first_hand_win': False,
                                    'first_hand_push': False,
                                    'first_hand_loose': False,
                                    'first_hand_busted': False,
                                    'second_hand_blackjack': False,
                                    'second_hand_win': False,
                                    'second_hand_push': False,
                                    'second_hand_loose': False,
                                    'second_hand_busted': False}
        common_vars.player_hands = []
        hand_instance = []
        common_vars.player_hands.append(hand_instance)
        common_vars.player_bets = []
        common_vars.bets_pos = []  # [(x,y), (x,y), ...]
        common_vars.game_rounds += 1
        common_vars.double_downs = [False, False]
        common_vars.first_card_hidden = True
        button_status.reset()
        self.next_state(BettingState)


class BettingState(State):

    _current_bet = []
    _chips_visible = True
    # TODO: chips_visible as class variable?

    def __call__(self, common_vars, button_status):

        logging.debug(type(self).__name__ + ':' + 'enter')

        if common_vars.player_cash >= LOWEST_BET or sum(self._current_bet) > 0:
            plot_chips(common_vars.screen,
                       common_vars.player_cash,
                       common_vars.chips_image_width,
                       self._chips_visible)

            if sum(self._current_bet) > 0:
                button_status.play = True
                button_status.undo_bet = True
            else:
                button_status.play = False
                button_status.undo_bet = False
            plot_buttons(common_vars.screen, button_status)

            button_collide_instance = ButtonCollideArea.get_instance(common_vars)
            chips_collide_instance = ChipsCollideArea.get_instance(common_vars)

            sound_db = SoundDB.get_instance()
            chip_sound = sound_db.get_sound(SOUND_PATH + 'chipsstack.wav')

            temp_bet_list = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    common_vars.done = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_position = pygame.mouse.get_pos()
                    if button_collide_instance.play_button_area.collidepoint(mouse_position[0], mouse_position[1])\
                            and sum(self._current_bet) > 0:
                        # Time to play
                        logging.info(type(self).__name__ + ': [Play] pressed')
                        logging.info(type(self).__name__ + ': Current bet is {0}'.format(self._current_bet))
                        logging.info(type(self).__name__ + ': Remaining credits {0}'.format(common_vars.player_cash))
                        # Initiate all needed variables for the next state
                        common_vars.player_bets.append(self._current_bet)
                        common_vars.dealer_cards = []
                        common_vars.first_card_hidden = True
                        common_vars.player_deal = False
                        common_vars.player_hit = False
                        button_status.play = False
                        button_status.undo_bet = False

                        self._current_bet = []
                        self._chips_visible = True
                        self.next_state(DealingState)
                    elif button_collide_instance.undo_bet_button_area.\
                            collidepoint(mouse_position[0], mouse_position[1])\
                            and sum(self._current_bet) > 0:
                        chip_sound.play()
                        common_vars.player_cash += self._current_bet.pop()
                        logging.info(type(self).__name__ + ': [Undo bet] pressed, remaining credits {0}'.
                                     format(common_vars.player_cash))

                    if len(self._current_bet) < 14:
                        self._chips_visible = True
                        if chips_collide_instance.chip_5_area.collidepoint(mouse_position[0], mouse_position[1]) \
                                and common_vars.player_cash >= 5:
                            chip_sound.play()
                            self._current_bet.append(5)
                            common_vars.player_cash -= 5
                        elif chips_collide_instance.chip_10_area.collidepoint(mouse_position[0], mouse_position[1]) \
                                and common_vars.player_cash >= 10:
                            chip_sound.play()
                            self._current_bet.append(10)
                            common_vars.player_cash -= 10
                        elif chips_collide_instance.chip_50_area.collidepoint(mouse_position[0], mouse_position[1]) \
                                and common_vars.player_cash >= 50:
                            chip_sound.play()
                            self._current_bet.append(50)
                            common_vars.player_cash -= 50
                        elif chips_collide_instance.chip_100_area.collidepoint(mouse_position[0], mouse_position[1]) \
                                and common_vars.player_cash >= 100:
                            chip_sound.play()
                            self._current_bet.append(100)
                            common_vars.player_cash -= 100
                    else:
                        self._chips_visible = False

            temp_bet_list.append(self._current_bet)
            plot_bets(common_vars.screen, temp_bet_list)
        else:

            self.next_state(FinalState)


class DealingState(State):

    def __call__(self, common_vars, button_status):

        logging.debug(type(self).__name__ + ':' + 'enter')

        if is_cut_passed(common_vars.shoe_of_decks):
            logging.info(type(self).__name__ + ': Cut passed, create new shoe with {0} decks'.format(NUM_OF_DECKS))
            common_vars.shoe_of_decks = CardDecks(NUM_OF_DECKS)


        plot_chips(common_vars.screen, common_vars.player_cash, common_vars.chips_image_width, False)

        sound_db = SoundDB.get_instance()
        card_sound = sound_db.get_sound(SOUND_PATH + 'cardslide.wav')

        first_hand = 0
        if len(common_vars.dealer_cards) < 2:

            common_vars.pause_time = PAUSE_TIMER1

            if not common_vars.player_hands[first_hand]:

                card_sound.play()
                card = common_vars.shoe_of_decks.pop()
                common_vars.player_hands[first_hand].append(card)

            elif not common_vars.dealer_cards:

                card_sound.play()
                card = common_vars.shoe_of_decks.pop()
                common_vars.dealer_cards.append(card)

            elif len(common_vars.player_hands[first_hand]) == 1:

                card_sound.play()
                card = common_vars.shoe_of_decks.pop()
                common_vars.player_hands[first_hand].append(card)

            elif len(common_vars.dealer_cards) == 1:

                card_sound.play()
                card = common_vars.shoe_of_decks.pop()
                common_vars.dealer_cards.append(card)
        elif not button_status.hit:

            logging.info(type(self).__name__ + ': Two cards dealt, first evaluation')
            common_vars.pause_time = 0
            value_of_dealers_hand = get_value_of_dealers_hand(common_vars.dealer_cards)
            for hand in common_vars.player_hands:
                value_of_players_hand = get_value_of_players_hand(hand)
                if value_of_players_hand == 21 and len(common_vars.player_hands) != 2:  # Not in split mode
                    # Let's evaluate and compare towards dealers hand
                    common_vars.first_card_hidden = False
                    if value_of_dealers_hand == 21:
                        # A Tie or push, bets going back to player
                        logging.info(type(self).__name__ + ':' + 'Push')
                        common_vars.pause_time = PAUSE_TIMER3
                        plot_results(common_vars.screen, common_vars.text_font, 'Push')
                        common_vars.hands_status['first_hand_push'] = True
                        common_vars.player_cash += sum(common_vars.player_bets[0])
                    else:

                        logging.info(type(self).__name__ + ':' + 'Black Jack!!!')
                        common_vars.pause_time = PAUSE_TIMER3
                        plot_results(common_vars.screen, common_vars.text_font, 'Black Jack!!!')
                        common_vars.hands_status['first_hand_blackjack'] = True
                        common_vars.player_cash += sum(common_vars.player_bets[0])  # First get the bet back
                        common_vars.player_cash += int(sum(common_vars.player_bets[0]) * 1.5)

                    common_vars.dealer_last_hand = value_of_dealers_hand

                    common_vars.pause_time = PAUSE_TIMER3
                    button_status.reset()
                    self.next_state(InitialState)
                elif len(common_vars.player_hands) != 2 and is_possible_split(hand):

                    button_status.split = can_double_bet(common_vars.player_bets, common_vars.player_cash)
                    button_status.hit = True
                else:
                    button_status.hit = True
        else:
            button_status.hit = True
            button_status.stand = True
            button_status.double_down = can_double_bet(common_vars.player_bets, common_vars.player_cash)

        button_collide_instance = ButtonCollideArea.get_instance(common_vars)

        plot_buttons(common_vars.screen, button_status)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                common_vars.done = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_position = pygame.mouse.get_pos()  # returns (x, y) in a tuple
                if button_status.hit and button_collide_instance.hit_button_area.\
                        collidepoint(mouse_position[0], mouse_position[1]):
                    logging.info(type(self).__name__ + ': [Hit] pressed')
                    card_sound.play()
                    card = common_vars.shoe_of_decks.pop()
                    common_vars.player_hands[first_hand].append(card)
                    button_status.split = False
                    button_status.double_down = False
                    self.next_state(PlayerHitState)
                elif button_status.stand and button_collide_instance.stand_button_area.\
                        collidepoint(mouse_position[0], mouse_position[1]):
                    logging.info(type(self).__name__ + ': [Stand] pressed')
                    self.next_state(DealerInitState)
                elif button_status.double_down and button_collide_instance.double_down_button_area.\
                        collidepoint(mouse_position[0], mouse_position[1]):
                    logging.info(type(self).__name__ + ': [Double down] pressed')

                    common_vars.player_cash -= sum(common_vars.player_bets[0])
                    common_vars.player_bets.append(common_vars.player_bets[0])
                    logging.info(type(self).__name__ + ': Remaining credits {0}'.format(common_vars.player_cash))
                    card_sound.play()
                    card = common_vars.shoe_of_decks.pop()
                    common_vars.player_hands[first_hand].append(card)  # Pull a third card
                    common_vars.double_downs[first_hand] = True
                    button_status.double_down = False
                    self.next_state(DealerInitState)
                elif button_status.split and button_collide_instance.split_button_area.\
                        collidepoint(mouse_position[0], mouse_position[1]):

                    logging.info(type(self).__name__ + ': [Split] pressed')
                    common_vars.player_cash -= sum(common_vars.player_bets[0])
                    common_vars.player_bets.append(common_vars.player_bets[0])

                    button_status.reset()
                    logging.info(type(self).__name__ + ': Remaining credits {0}'.format(common_vars.player_cash))
                    self.next_state(SplitState)

        plot_bets(common_vars.screen, common_vars.player_bets)

        plot_buttons(common_vars.screen, button_status)

        plot_players_hands(common_vars.screen,
                           PLAYER_CARD_START_POS,
                           common_vars.player_hands,
                           common_vars.double_downs,
                           common_vars.hands_status)

        plot_dealers_hand(common_vars.screen,
                          DEALER_CARD_START_POS,
                          common_vars.dealer_cards,
                          common_vars.first_card_hidden)


class SplitState(State):

    def __call__(self, common_vars, button_status):

        logging.debug(type(self).__name__ + ':' + 'enter')

        if is_cut_passed(common_vars.shoe_of_decks):
            logging.info(type(self).__name__ + ': Cut passed, create new shoe with {0} decks'.format(NUM_OF_DECKS))
            common_vars.shoe_of_decks = CardDecks(NUM_OF_DECKS)

        plot_chips(common_vars.screen, common_vars.player_cash, common_vars.chips_image_width, False)
        plot_buttons(common_vars.screen, button_status)

        sound_db = SoundDB.get_instance()
        card_sound = sound_db.get_sound(SOUND_PATH + 'cardslide.wav')

        first_hand = 0
        second_hand = 1
        if len(common_vars.player_hands) == 1:
            hand_instance = []
            common_vars.player_hands.append(hand_instance)
            common_vars.player_hands[second_hand].append(common_vars.player_hands[first_hand].pop())

        logging.info(type(self).__name__ + ': {0}:{1}'.
                     format(len(common_vars.player_hands[first_hand]),
                            len(common_vars.player_hands[second_hand])))

        if len(common_vars.player_hands[second_hand]) != 2:

            common_vars.pause_time = PAUSE_TIMER1
            if len(common_vars.player_hands[first_hand]) < 2:
                card_sound.play()
                card = common_vars.shoe_of_decks.pop()
                common_vars.player_hands[first_hand].append(card)
            elif len(common_vars.player_hands[second_hand]) < 2:
                card_sound.play()
                card = common_vars.shoe_of_decks.pop()
                common_vars.player_hands[second_hand].append(card)
        else:

            value_of_players_hands = 0
            for hand in common_vars.player_hands:
                value_of_players_hands += get_value_of_players_hand(hand)
            if value_of_players_hands != 42:

                button_status.hit = True
                button_status.stand = True
                button_status.double_down = can_double_bet(common_vars.player_bets, common_vars.player_cash)
                self.next_state(PlayerHitState)
            else:

                value_of_dealers_hand = get_value_of_dealers_hand(common_vars.dealer_cards)
                common_vars.dealer_last_hand = value_of_dealers_hand
                sum_of_bets = 0
                for bet in common_vars.player_bets:
                    sum_of_bets += sum(bet)
                logging.info(type(self).__name__ + ':' + 'sum_of_bets = {0}'.format(sum_of_bets))
                if value_of_dealers_hand == 21:

                    logging.info(type(self).__name__ + ':' + 'Push')
                    plot_results(common_vars.screen, common_vars.text_font, 'Push')
                    common_vars.player_hands['first_hand_push'] = True
                    common_vars.player_hands['second_hand_push'] = True
                    common_vars.player_cash += sum_of_bets
                else:
                    # Double BlackJack, pay 3/2 (1.5)
                    logging.info(type(self).__name__ + ':' + 'Double BlackJack!!!')
                    plot_results(common_vars.screen, common_vars.text_font, 'Double Black Jack!!!')
                    common_vars.player_hands['first_hand_blackjack'] = True
                    common_vars.player_hands['second_hand_blackjack'] = True
                    common_vars.player_cash += sum_of_bets  # First get the bet back
                    common_vars.player_cash += int(sum_of_bets * 1.5)


                common_vars.pause_time = PAUSE_TIMER3
                button_status.reset()
                self.next_state(InitialState)

        plot_bets(common_vars.screen, common_vars.player_bets)

        plot_players_hands(common_vars.screen,
                           PLAYER_CARD_START_POS,
                           common_vars.player_hands,
                           common_vars.double_downs,
                           common_vars.hands_status)

        plot_dealers_hand(common_vars.screen,
                          DEALER_CARD_START_POS,
                          common_vars.dealer_cards,
                          common_vars.first_card_hidden)


class PlayerHitState(State):

    _current_hand = 0

    def __call__(self, common_vars, button_status):

        logging.debug(type(self).__name__ + ':' + 'enter')

        if is_cut_passed(common_vars.shoe_of_decks):
            logging.info(type(self).__name__ + ': Cut passed, create new shoe with {0} decks'.format(NUM_OF_DECKS))
            common_vars.shoe_of_decks = CardDecks(NUM_OF_DECKS)

        plot_chips(common_vars.screen, common_vars.player_cash, common_vars.chips_image_width, False)

        sound_db = SoundDB.get_instance()
        card_sound = sound_db.get_sound(SOUND_PATH + 'cardslide.wav')

        num_of_hands = len(common_vars.player_hands)
        if num_of_hands == 2:
            image_db = ImageDB.get_instance()
            if self._current_hand == 0:
                common_vars.screen.blit(image_db.get_image(IMAGE_PATH + 'hand.png'), (100, 315))
            else:
                common_vars.screen.blit(image_db.get_image(IMAGE_PATH + 'hand.png'), (100 + GAP_BETWEEN_SPLIT, 315))

        value_of_players_hand = get_value_of_players_hand(common_vars.player_hands[self._current_hand])
        if value_of_players_hand > 21:
            logging.info(type(self).__name__ + ': Player is busted {0}'.format(value_of_players_hand))
            common_vars.pause_time = PAUSE_TIMER3
            plot_results(common_vars.screen, common_vars.text_font,
                         'Player is busted {0}'.format(value_of_players_hand))
            if num_of_hands == 1:
                common_vars.hands_status['first_hand_busted'] = True
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            elif self._current_hand == 0:
                # In split mode and first hand busted
                common_vars.hands_status['first_hand_busted'] = True
                button_status.double_down = True
                self._current_hand += 1
            elif self._current_hand == 1 and common_vars.hands_status['first_hand_busted']:
                # In split mode and both hands busted
                common_vars.hands_status['second_hand_busted'] = True
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            else:
                # In split mode and first hand ok, but second hand busted
                common_vars.hands_status['second_hand_busted'] = True
                self._current_hand = 0
                self.next_state(DealerInitState)
        elif value_of_players_hand == 21:
            if num_of_hands == 2 and self._current_hand == 0:
                logging.info(type(self).__name__ + ': first hand has ' + '21, save this hand for later evaluation')
                self._current_hand += 1
            else:
                logging.info(type(self).__name__ + ': second hand has ' + '21, lets see what the dealer has')
                self._current_hand = 0
                self.next_state(DealerInitState)
        else:

            button_collide_instance = ButtonCollideArea.get_instance(common_vars)
            plot_buttons(common_vars.screen, button_status)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    common_vars.done = True
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_position = pygame.mouse.get_pos()
                    if button_collide_instance.hit_button_area.collidepoint(mouse_position[0], mouse_position[1]):
                        logging.info(type(self).__name__ + ': [Hit] pressed')
                        card_sound.play()
                        card = common_vars.shoe_of_decks.pop()
                        common_vars.player_hands[self._current_hand].append(card)
                        button_status.double_down = False
                    elif button_status.double_down and button_collide_instance.double_down_button_area.\
                            collidepoint(mouse_position[0], mouse_position[1]):
                        logging.info(type(self).__name__ + ': [Double down] pressed')
                        common_vars.double_downs[self._current_hand] = True
                        common_vars.player_cash -= sum(common_vars.player_bets[0])
                        common_vars.player_bets.append(common_vars.player_bets[0])
                        logging.info(type(self).__name__ + ': Remaining credits {0}'.format(common_vars.player_cash))
                        card_sound.play()
                        card = common_vars.shoe_of_decks.pop()
                        common_vars.player_hands[self._current_hand].append(card)
                        if num_of_hands == 2 and self._current_hand == 0:

                            self._current_hand += 1
                        else:
                            self._current_hand = 0
                            button_status.double_down = False
                            self.next_state(DealerInitState)
                    elif button_collide_instance.stand_button_area.collidepoint(mouse_position[0], mouse_position[1]):
                        logging.info(type(self).__name__ + ': [Stands] pressed, player has {0}'.
                                     format(value_of_players_hand))
                        if num_of_hands == 2 and self._current_hand == 0:

                            self._current_hand += 1
                            button_status.double_down = True
                        else:
                            self._current_hand = 0
                            self.next_state(DealerInitState)

        plot_bets(common_vars.screen, common_vars.player_bets)

        plot_buttons(common_vars.screen, button_status)

        plot_players_hands(common_vars.screen,
                           PLAYER_CARD_START_POS,
                           common_vars.player_hands,
                           common_vars.double_downs,
                           common_vars.hands_status)

        plot_dealers_hand(common_vars.screen,
                          DEALER_CARD_START_POS,
                          common_vars.dealer_cards,
                          common_vars.first_card_hidden)


class DealerInitState(State):

    _current_hand = 0

    def __call__(self, common_vars, button_status):

        logging.debug(type(self).__name__ + ':' + 'enter')

        if is_cut_passed(common_vars.shoe_of_decks):
            logging.info(type(self).__name__ + ': Cut passed, create new shoe with {0} decks'.format(NUM_OF_DECKS))
            common_vars.shoe_of_decks = CardDecks(NUM_OF_DECKS)

        plot_chips(common_vars.screen, common_vars.player_cash, common_vars.chips_image_width, False)

        common_vars.first_card_hidden = False
        num_of_hands = len(common_vars.player_hands)
        value_of_dealer_hand = get_value_of_dealers_hand(common_vars.dealer_cards)
        common_vars.dealer_last_hand = value_of_dealer_hand
        value_of_player_hand = get_value_of_players_hand(common_vars.player_hands[self._current_hand])

        if value_of_dealer_hand == 21:
            logging.info(type(self).__name__ +
                         ': Dealer has {0}, Player has {1}'.format(value_of_dealer_hand, value_of_player_hand))
            if value_of_player_hand < 21:

                common_vars.pause_time = PAUSE_TIMER3
                plot_results(common_vars.screen, common_vars.text_font,
                             'Dealer has {0}, Player has {1}'.format(value_of_dealer_hand, value_of_player_hand))
                if num_of_hands == 1:

                    common_vars.hands_status['first_hand_loose'] = True
                    self._current_hand = 0
                    button_status.reset()
                    self.next_state(InitialState)
                elif num_of_hands == 2 and self._current_hand == 0:

                    common_vars.player_bets.pop()

                    self._current_hand += 1
                    common_vars.hands_status['first_hand_loose'] = True
                else:

                    common_vars.hands_status['second_hand_loose'] = True
                    self._current_hand = 0
                    button_status.reset()
                    self.next_state(InitialState)
            else:
                logging.info(type(self).__name__ + ': Both dealer and player has 21, a push')
                common_vars.pause_time = PAUSE_TIMER3
                plot_results(common_vars.screen, common_vars.text_font,
                             'Both dealer and player has 21, a push')

                common_vars.player_cash += sum(common_vars.player_bets.pop())
                if num_of_hands == 1 or self._current_hand == 1:

                    common_vars.hands_status['first_hand_push'] = True
                    self._current_hand = 0
                    button_status.reset()
                    self.next_state(InitialState)
                else:

                    self._current_hand += 1
                    common_vars.hands_status['first_hand_push'] = True
        elif value_of_dealer_hand > 15 and value_of_dealer_hand > value_of_player_hand:

            logging.info(type(self).__name__ +
                         ': Dealer wins with {0} over player {1}'.
                         format(value_of_dealer_hand, value_of_player_hand))
            common_vars.pause_time = PAUSE_TIMER3
            plot_results(common_vars.screen, common_vars.text_font,
                         'Dealer wins with {0} over player {1}'.
                         format(value_of_dealer_hand, value_of_player_hand))
            if num_of_hands == 1 or self._current_hand == 1:

                common_vars.hands_status['first_hand_loose'] = True
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            else:

                self._current_hand += 1
                common_vars.hands_status['first_hand_loose'] = True
        elif value_of_player_hand > 21:

            logging.info(type(self).__name__ +
                         ': Player is busted with {0}'.format(value_of_player_hand))
            common_vars.pause_time = PAUSE_TIMER3
            plot_results(common_vars.screen, common_vars.text_font,
                         'Player is busted with {0}'.format(value_of_player_hand))
            if num_of_hands == 1 or self._current_hand == 1:

                common_vars.hands_status['first_hand_busted'] = True
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            else:

                self._current_hand += 1
                common_vars.hands_status['first_hand_busted'] = True
        else:
            self._current_hand = 0
            self.next_state(DealerHitState)

        plot_bets(common_vars.screen, common_vars.player_bets)

        plot_buttons(common_vars.screen, button_status)

        plot_players_hands(common_vars.screen,
                           PLAYER_CARD_START_POS,
                           common_vars.player_hands,
                           common_vars.double_downs,
                           common_vars.hands_status)

        plot_dealers_hand(common_vars.screen,
                          DEALER_CARD_START_POS,
                          common_vars.dealer_cards,
                          common_vars.first_card_hidden)


class DealerHitState(State):

    _current_hand = 0

    def __call__(self, common_vars, button_status):

        logging.debug(type(self).__name__ + ':' + 'enter')

        if is_cut_passed(common_vars.shoe_of_decks):
            logging.info(type(self).__name__ + ': Cut passed, create new shoe with {0} decks'.format(NUM_OF_DECKS))
            common_vars.shoe_of_decks = CardDecks(NUM_OF_DECKS)

        plot_chips(common_vars.screen, common_vars.player_cash, common_vars.chips_image_width, False)

        sound_db = SoundDB.get_instance()
        card_sound = sound_db.get_sound(SOUND_PATH + 'cardslide.wav')

        num_of_hands = len(common_vars.player_hands)
        value_of_dealer_hand = get_value_of_dealers_hand(common_vars.dealer_cards)
        common_vars.dealer_last_hand = value_of_dealer_hand
        value_of_player_hand = get_value_of_players_hand(common_vars.player_hands[self._current_hand])

        if value_of_dealer_hand < 16:

            card_sound.play()
            card = common_vars.shoe_of_decks.pop()
            common_vars.dealer_cards.append(card)
            common_vars.pause_time = 1.0

        elif value_of_dealer_hand < 17 and value_of_dealer_hand < value_of_player_hand:

            card_sound.play()
            card = common_vars.shoe_of_decks.pop()
            common_vars.dealer_cards.append(card)
            common_vars.pause_time = 1.0

        elif value_of_player_hand > 21 or 22 > value_of_dealer_hand > value_of_player_hand:

            common_vars.pause_time = PAUSE_TIMER3
            if value_of_player_hand > 21:
                logging.info(type(self).__name__ +
                             ': Player is busted {0}'.format(value_of_player_hand))
                plot_results(common_vars.screen, common_vars.text_font,
                             'Player is busted {0}'.format(value_of_player_hand))
                if self._current_hand == 0:
                    common_vars.hands_status['first_hand_busted'] = True
                else:
                    common_vars.hands_status['second_hand_busted'] = True
            else:
                logging.info(type(self).__name__ +
                             ': Dealer wins with {0} over player {1}'.
                             format(value_of_dealer_hand, value_of_player_hand))
                plot_results(common_vars.screen, common_vars.text_font,
                             'Dealer wins with {0} over player {1}'.
                             format(value_of_dealer_hand, value_of_player_hand))
                if self._current_hand == 0:
                    common_vars.hands_status['first_hand_loose'] = True
                else:
                    common_vars.hands_status['second_hand_loose'] = True

            common_vars.player_bets.pop()
            if common_vars.double_downs[self._current_hand]:

                common_vars.player_bets.pop()
            common_vars.pause_time = PAUSE_TIMER3
            if num_of_hands == 1 or self._current_hand == 1:

                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            else:

                self._current_hand += 1
        elif value_of_dealer_hand == value_of_player_hand:

            common_vars.pause_time = PAUSE_TIMER3
            logging.info(type(self).__name__ +
                         ': A push, dealer has {0}, player has {1}'.
                         format(value_of_dealer_hand, value_of_player_hand))
            plot_results(common_vars.screen, common_vars.text_font,
                         'A push dealer has {0}, player has {1}'.
                         format(value_of_dealer_hand, value_of_player_hand))
            if self._current_hand == 0:
                common_vars.hands_status['first_hand_push'] = True
            else:
                common_vars.hands_status['second_hand_push'] = True

            if num_of_hands == 1 or self._current_hand == 1:

                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            else:

                self._current_hand += 1


            common_vars.player_cash += sum(common_vars.player_bets.pop())
            if common_vars.double_downs[self._current_hand]:

                common_vars.player_cash += sum(common_vars.player_bets.pop())

        else:

            if self._current_hand == 0:
                common_vars.hands_status['first_hand_win'] = True
            else:
                common_vars.hands_status['second_hand_win'] = True
            logging.info(type(self).__name__ +
                         ': Player wins with {0} over dealer {1}, bet is {2}'.
                         format(value_of_player_hand, value_of_dealer_hand, common_vars.player_bets[0]))
            common_vars.pause_time = PAUSE_TIMER3
            plot_results(common_vars.screen, common_vars.text_font,
                         "Player wins with {0} over dealer {1}".format(value_of_player_hand, value_of_dealer_hand))
            common_vars.player_cash += sum(common_vars.player_bets.pop()) * 2
            if common_vars.double_downs[self._current_hand]:
                # Doubled down hand, add additional win
                logging.info(type(self).__name__ +
                             ': Double down, add additional win {0}'.
                             format(common_vars.player_bets[0]))
                common_vars.player_cash += sum(common_vars.player_bets.pop()) * 2
            common_vars.dealer_last_hand = value_of_dealer_hand
            if num_of_hands == 1 or self._current_hand == 1:

                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            else:

                self._current_hand += 1

        plot_bets(common_vars.screen, common_vars.player_bets)

        plot_buttons(common_vars.screen, button_status)

        plot_players_hands(common_vars.screen,
                           PLAYER_CARD_START_POS,
                           common_vars.player_hands,
                           common_vars.double_downs,
                           common_vars.hands_status)

        plot_dealers_hand(common_vars.screen,
                          DEALER_CARD_START_POS,
                          common_vars.dealer_cards,
                          common_vars.first_card_hidden)


class FinalState(State):

    def __call__(self, common_vars, button_status):

        logging.debug(type(self).__name__ + ':' + 'enter')


        account_text = common_vars.text_font.render("Game Over, you're out of money", False, GOLD_COLOR)
        common_vars.screen.blit(account_text, (5, GAME_BOARD_Y_SIZE - 30))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                common_vars.done = True
