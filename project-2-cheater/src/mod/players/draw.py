from .player import Player

class DrawPlayer(Player):
  def putCard(self, declared_card):
    return "draw"

  def checkCard(self, opponent_declaration):
    return False
