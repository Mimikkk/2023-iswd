from random import choice

from .extended_player import ExtendedPlayer

Card = tuple[int, int]


class DanielosPlayer(ExtendedPlayer):
  Cards = tuple(
    (rank, color)
    for rank in range(9, 15)
    for color in range(4)
  )

  def __init__(self, name: str):
    super().__init__(name)
    self.suspected = []
    self.declared = None
    self.pile = []

  def on_feedback(self):
    self.present_state()

  def on_right_accusation(self, revealed, taken_count):
    print(
      f"I was right so they took {taken_count} cards. Also the top card was {revealed} declared as {self.declared}.")
    if revealed in self.suspected:
      self.suspected.remove(revealed)
    for _ in range(taken_count):
      if len(self.pile) > 0 and (card := self.pile.pop()) in self.suspected: self.suspected.remove(card)

  def on_wrong_accusation(self, revealed, taken_count):
    print(f"I was wrong so I took took {taken_count} cards. Also the top card was {revealed}")
    self.suspected.remove(revealed)

  def on_caught(self, taken_count: int):
    print(f"I was caught so I took {taken_count} cards.")
    for _ in range(taken_count):
      if len(self.pile) > 0: self.pile.pop()

  def on_honest(self, taken_count: int):
    print(f"I was honest and accused so they took {taken_count} cards.")
    for _ in range(taken_count):
      if len(self.pile) > 0 and (card := self.pile.pop()) in self.suspected: self.suspected.remove(card)

  def on_start(self):
    self.suspected.extend(self.cards)

  def on_take(self, taken):
    self.suspected.extend(taken)

  def declare(self, declared):
    if declared and declared not in self.pile: self.pile.append(declared)
    valid_held_cards = declared and [card for card in self.cards if card[0] >= declared[0]] or self.cards

    if not valid_held_cards: return "draw"

    card = declaration = choice(valid_held_cards)
    self.pile.append(card)
    return card, declaration

  def should_accuse(self, declared):
    print(f"Declared: {declared}")
    if declared in self.suspected or declared in self.pile:
      self.declared = declared
      return True
    self.suspected.append(declared)
    return False

  def present_state(self):
    print(f"Recreated Pile  : {self.pile}")
    print(f"Real Pile       : {self.state.pile}")
    print(f"Suspected       : {sorted(self.suspected)}")

    opponent = self.state.players[[
      is_same_hand(self.cards, self.state.players[i].cards) for i in range(2)
    ].index(False)]

    print(f"Cards           : {sorted(self.cards)}")
    print(f"Opponent's Cards: {sorted(opponent.cards)}")
    print("-" * 64)


def is_same_hand(first: list[Card], second: list[Card]):
  return len(first) == len(second) and all(
    x == y for x, y in zip(sorted(first), sorted(second))
  )
