from random import choice

from .player import Player

class RandomPlayer(Player):

  def putCard(self, declared):
    should_draw = len(self.cards) == 1 and declared is not None and self.cards[0][0] < declared[0]

    if should_draw: return "draw"
    declaration = card = choice(self.cards)

    should_cheat = choice([True, False])
    if should_cheat: declaration = choice(self.cards)

    # Yet, declared card should be no worse than a card on the top of the pile.
    is_worse_than_declared = declared is not None and declaration[0] < declared[0]
    if is_worse_than_declared: declaration = (min(declared[0] + 1, 14), declaration[1])

    return card, declaration

  def checkCard(self, declared):
    return choice([True, False])
