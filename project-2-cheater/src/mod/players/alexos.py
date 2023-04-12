from numpy.random import choice

from .player import Player

Card = tuple[int, int]
class AlexosPlayer(Player):
  def __init__(self, name):
    super().__init__(name)
    self.used: set[Card] = set()

  def on_start(self):
    print("I started")
    pass

  def on_take(self, taken):
    print("I took", taken)
    pass

  def on_feedback(self, is_accusation, is_player, has_player_drawn_cards, revealed, taken_count):
    print("I got feedback", is_accusation, is_player, has_player_drawn_cards, revealed, taken_count)
    if is_accusation: self.on_accusation(is_player, has_player_drawn_cards, revealed, taken_count)

  def on_accusation(self, is_player, has_player_drawn_cards, revealed, cards_taken):
    print("I was accused or accused someone")

  def on_wrong_accusation(self):
    print("I was wrong")

  def on_right_accusation(self):
    print("I was right")

  def on_caught(self):
    print("I was caught by opponent")

  def on_uncaught(self):
    print("I was caught by opponent")

  def declare(self, declared):
    valid_cards = [card for card in self.cards if not declared or card[0] > declared[0]]
    invalid_cards = [card for card in self.cards if declared and card[0] <= declared[0]]

    if not valid_cards: return "draw"

    card = declaration = choice(valid_cards)
    return card, declaration

  def should_accuse(self, declared):
    return False

  def putCard(self, declared_card):
    return self.declare(declared_card)

  def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=False):
    self.on_feedback(checked, iChecked, iDrewCards, revealedCard, noTakenCards)

  def checkCard(self, opponent_declaration):
    return self.should_accuse(opponent_declaration)

  def startGame(self, cards):
    super().startGame(cards)
    self.on_start()

  def takeCards(self, taken):
    super().takeCards(taken)
    self.on_take(taken)
