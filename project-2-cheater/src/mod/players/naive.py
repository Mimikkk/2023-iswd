from random import choice

from .extended_player import ExtendedPlayer

class NaivePlayer(ExtendedPlayer):
  def declare(self, declared):
    if not declared: self.on_opponent_draw()

    valid = [card for card in self.cards if not declared or card[0] >= declared[0]]
    if not valid: return "draw"

    card = declaration = choice(valid)
    return card, declaration

  def should_accuse(self, declared): return False
