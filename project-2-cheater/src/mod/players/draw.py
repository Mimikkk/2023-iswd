from .extended_player import ExtendedPlayer

class DrawPlayer(ExtendedPlayer):
  def declare(self, declared): return "draw"
  def should_accuse(self, declared): return False
