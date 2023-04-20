from random import choice, random
from .player import Player

Card = tuple[int, int]


def by_rank(card: Card): return card[0]


def by_color(card: Card): return card[1]


def increase_by(card: Card, declarable: list[Card], value: int):
  if value == 0: return card, card
  declarable = [(rank, color) for (rank, color) in declarable if rank == rank + value]
  if not declarable: return increase_by(card, declarable, value - 1)
  return card, choice(declarable)


class CompanerosPlayer(Player):
  Cards = tuple(
    (rank, color)
    for rank in range(9, 15)
    for color in range(4)
  )

  def __init__(self, name: str):
    super().__init__(name)
    self.suspected = []
    self.pile = []

  def on_right_accusation(self, revealed, taken_count):
    if revealed in self.suspected:
      self.suspected.remove(revealed)
    for _ in range(taken_count):
      if len(self.pile) > 0 and (card := self.pile.pop()) in self.suspected: self.suspected.remove(card)

  def on_wrong_accusation(self, revealed, taken_count):
    self.suspected.remove(revealed)

  def on_caught(self, taken_count: int):
    for _ in range(taken_count):
      if len(self.pile) > 0: self.pile.pop()

  def on_honest(self, taken_count: int):
    for _ in range(taken_count):
      if len(self.pile) > 0 and (card := self.pile.pop()) in self.suspected: self.suspected.remove(card)

  def on_start(self):
    self.suspected.extend(self.cards)

  def on_take(self, taken):
    self.suspected.extend(taken)

  def on_opponent_draw(self):
    for _ in range(3):
      if len(self.pile) > 0 and (card := self.pile.pop()) in self.suspected: self.suspected.remove(card)

  def declare(self, declared):
    valid: list[Card] = declared and [card for card in self.cards if card[0] >= declared[0]] or self.cards
    declarable: list[Card] = declared and [card for card in self.Cards if card[0] >= declared[0]] or self.Cards

    if len(valid) == 0 and len(self.cards) == 1 and random() < 0.20:
      card = declaration = self.cards[0]
      self.pile.append(card)
      return card, declaration

    if not valid: return "draw"
    min_valid, max_valid = min(valid, key=by_rank), max(valid, key=by_rank)
    difference = max_valid[0] - min_valid[0]

    card, declaration = len(self.cards) <= 3 \
                        and (max_valid, max_valid) \
                        or increase_by(min_valid, declarable, difference)

    self.pile.append(card)
    return card, declaration

  def should_accuse(self, declared):
    return declared in self.suspected

  def __on_feedback(
      self,
      is_accusation: bool,
      is_player: bool,
      has_player_drawn_cards: bool,
      revealed: Card | None,
      taken_count: int | None
  ):
    if is_accusation: self.__on_accusation(is_player, has_player_drawn_cards, revealed, taken_count)

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
