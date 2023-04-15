from random import choice

from .extended_player import ExtendedPlayer

Card = tuple[int, int]
class NaivePlayer(ExtendedPlayer):
  def declare(self, declared: Card | None):
    if not declared: self.on_opponent_draw()

    valid_held_cards = [card for card in self.cards if not declared or card[0] > declared[0]]
    if not valid_held_cards: return "draw"

    card = declaration = choice(valid_held_cards)
    return card, declaration

  def should_accuse(self, declared: Card): return False
