from random import choice
from .extended_player import ExtendedPlayer


class RandomPlayer(ExtendedPlayer):
  def declare(self, declared):
    should_draw = len(self.cards) == 1 and not self.is_valid(self.cards[0], declared)
    if should_draw: return "draw"

    declaration = card = choice(self.cards)

    should_cheat = choice([True, False])
    if should_cheat: declaration = choice(self.cards)

    is_worse_than_declared = declared and declaration[0] < declared[0]
    if is_worse_than_declared: declaration = (min(declared[0] + 1, 14), declaration[1])

    return card, declaration

  def should_accuse(self, declared):
    return choice([True, False])
