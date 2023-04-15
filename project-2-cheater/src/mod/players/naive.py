from random import choice

from .player import Player

Card = tuple[int, int]
class NaivePlayer(Player):
  def __init__(self, name: str):
    super().__init__(name)
    self.used: set[Card] = set()

  def on_start(self):
    ...

  def on_take(self, taken: list[Card]):
    ...

  def on_opponent_draw(self):
    ...

  def on_feedback(
      self,
      is_accusation: bool,
      is_player: bool,
      has_player_drawn_cards: bool,
      revealed: Card | None,
      taken_count: int | None
  ):
    if is_accusation: self.on_accusation(is_player, has_player_drawn_cards, revealed, taken_count)

  def on_accusation(self, is_player, has_player_drawn_cards, revealed, taken_count):
    if is_player:
      if has_player_drawn_cards:
        self.on_wrong_accusation(revealed, taken_count)
      else:
        self.on_right_accusation(revealed, taken_count)
    else:
      if has_player_drawn_cards:
        self.on_caught(taken_count)
      else:
        self.on_honest(taken_count)

  def on_wrong_accusation(self, revealed: Card, taken_count: int):
    ...

  def on_right_accusation(self, revealed: Card, taken_count: int):
    ...

  def on_caught(self, taken_count: int):
    ...

  def on_honest(self, taken_count: int):
    ...

  def declare(self, declared: Card | None):
    if not declared: self.on_opponent_draw()

    valid_held_cards = [card for card in self.cards if not declared or card[0] > declared[0]]
    if not valid_held_cards: return "draw"

    card = declaration = choice(valid_held_cards)
    return card, declaration

  def should_accuse(self, declared: Card):
    return False

  def putCard(self, declared_card):
    return self.declare(declared_card)

  def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=False):
    self.on_feedback(checked, iChecked, iDrewCards, revealedCard, noTakenCards)

  def checkCard(self, opponent_declaration):
    return self.should_accuse(opponent_declaration)

  def startGame(self, cards, state):
    super().startGame(cards)
    self.on_start()

  def takeCards(self, taken):
    super().takeCards(taken)
    self.on_take(taken)
