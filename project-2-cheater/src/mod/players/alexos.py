import random
from .player import Player

Card = tuple[int, int]

class AlexosPlayer(Player):
  def __init__(self, name):
    super().__init__(name)
    self.memory: set[Card] = set()
    self.history = []
    self.used = {value: 0 for value in range(9, 15)}

  def startGame(self, cards):
    super().startGame(cards)
    ...

  def putCard(self, declared):
    chosen = random.choice(self.cards)
    return chosen, chosen

  def takeCards(self, cards):
    super().takeCards(cards)
    ...

  def checkCard(self, opponent_declaration):
    return True

  def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=False):
    ...
