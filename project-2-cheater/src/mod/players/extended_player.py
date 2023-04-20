from random import choice
from typing import Literal

from .player import Player

Card = tuple[int, int]


class ExtendedPlayer(Player):
  def __init__(self, name: str):
    super().__init__(name)

  def on_start(self):
    ...

  def on_take(self, taken: list[Card]):
    ...

  def on_opponent_draw(self):
    ...

  def on_wrong_accusation(self, revealed: Card, taken_count: int):
    ...

  def on_right_accusation(self, revealed: Card, taken_count: int):
    ...

  def on_caught(self, taken_count: int):
    ...

  def on_honest(self, taken_count: int):
    ...

  def on_feedback(self):
    ...

  def declare(self, declared: Card | None) -> Card | Literal["draw"]:
    ...

  def should_accuse(self, declared: Card) -> bool:
    ...

  def __on_feedback(
      self,
      is_accusation: bool,
      is_player: bool,
      has_player_drawn_cards: bool,
      revealed: Card | None,
      taken_count: int | None
  ):
    if is_accusation: self.__on_accusation(is_player, has_player_drawn_cards, revealed, taken_count)
    self.on_feedback()

  def __on_accusation(self, is_player, has_player_drawn_cards, revealed, taken_count):
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

  def putCard(self, declared_card):
    if not declared_card: self.on_opponent_draw()
    return self.declare(declared_card)

  def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=False):
    self.__on_feedback(checked, iChecked, iDrewCards, revealedCard, noTakenCards)

  def checkCard(self, opponent_declaration):
    return self.should_accuse(opponent_declaration)

  def startGame(self, cards, state):
    super().startGame(cards, state)
    self.on_start()

  def takeCards(self, taken):
    super().takeCards(taken)
    self.on_take(taken)

  def is_valid(self, first: Card, other: Card | None):
    return not other or first[0] >= other[0]

  def by_rank(self, card: Card):
    return card[0]

  def by_color(self, card: Card):
    return card[1]
