from random import choice

from .extended_player import ExtendedPlayer


class NaivePlayer(ExtendedPlayer):
  def declare(self, declared):
    valid = [card for card in self.cards if self.is_valid(card, declared)]
    if not valid: return "draw"

    card = declaration = choice(valid)
    return card, declaration

  def should_accuse(self, declared): return False
