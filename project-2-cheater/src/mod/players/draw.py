from numpy.random import choice
from .player import Player

class DrawPlayer(Player):
  def putCard(self, declared):
    return "draw"

  def checkCard(self, declared):
    return choice([False, False])
