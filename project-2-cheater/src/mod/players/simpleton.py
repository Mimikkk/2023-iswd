from .extended_player import ExtendedPlayer


class SimpletonPlayer(ExtendedPlayer):
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
