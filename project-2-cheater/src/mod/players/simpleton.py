from .extended_player import ExtendedPlayer


class SimpletonPlayer(ExtendedPlayer):
  def declare(self, declared):

    if len(self.cards) == 1 and not self.is_valid(self.cards[0], declared):
      return "draw"

    card = declaration = min(self.cards, key=self.by_rank)
    if declared:
      min_val = declared[0]
      if card[0] < min_val:
        declaration = (min(min_val + 1, 14), declaration[1])
        declaration = self.pick_your_card(declaration)
    return card, declaration

  def should_accuse(self, declared):
    return declared in self.cards

  def pick_your_card(self, declaration):
    for card in self.cards:
      if card[0] in (declaration[0], declaration[0] + 1): return card
    return declaration
