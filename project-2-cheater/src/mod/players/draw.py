from numpy.random import choice
from .player import Player

class DrawPlayer(Player):
  def putCard(self, declared, *args, **kwargs):
    return "draw"

  def checkCard(self, declared, *args, **kwargs):
    return choice([False, False])
