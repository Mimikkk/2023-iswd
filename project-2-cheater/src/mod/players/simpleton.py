from .player import Player


class SimpletonPlayer(Player):
  def declare(self, declared):
    valid = [card for card in self.cards if self.is_valid(card, declared)]
    if not valid: return "draw"

    card = declaration = min(self.cards, key=self.by_rank)

    if declared:
      minimum = declared[0]
      if card[0] < minimum:
        declaration = (min(minimum + 1, 14), declaration[1])
        declaration = self.pick(declaration)
    return card, declaration

  def should_accuse(self, declared):
    return declared in self.cards

  def pick(self, declaration):
    for card in self.cards:
      if card[0] in (declaration[0], declaration[0] + 1): return card
    return declaration

  def __init__(self, name: str):
    super().__init__(name)

  def putCard(self, declared_card):
    return self.declare(declared_card)

  def checkCard(self, opponent_declaration):
    return self.should_accuse(opponent_declaration)

  def is_valid(self, first, other):
    return not other or first[0] >= other[0]

  def by_rank(self, card):
    return card[0]

  def by_color(self, card):
    return card[1]
