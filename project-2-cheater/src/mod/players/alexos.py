import random

from numpy.random import choice

from .player import Player

Card = tuple[int, int]
class AlexosPlayer(Player):
  def __init__(self, name):
    super().__init__(name)
    self.used = []

  def startGame(self, cards):
    super().startGame(cards)

  def takeCards(self, cards):
    super().takeCards(cards)
    for card in cards:
      if card in self.used: self.used.remove(card)

  def getCheckFeedback(self, is_check, is_player, is_failure, revealed, taken_count, log=False):
    if is_check: self.__handle_check(is_player, is_failure, revealed, taken_count)


  def __handle_check(self, is_player, is_failure, revealed, cards_taken):
    pass

  def putCard(self, declared):
    should_draw = len(self.cards) == 1 and declared is not None and self.cards[0][0] < declared[0]
    if should_draw: return "draw"

    declaration = card = min(self.cards, key=lambda x: x[0])
    if declared is not None:
      value = declared[0]
      if card[0] < value: declaration = (min(value + 1, 14), declaration[1])

    self.used.append(card)
    return card, declaration

  def checkCard(self, declared):
    if declared in self.cards or declared in self.used: return True
    return False
