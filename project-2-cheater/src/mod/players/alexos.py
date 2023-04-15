from random import choice

from .player import Player

Card = tuple[int, int]
class AlexosPlayer(Player):
  Cards = tuple(
    (rank, color)
    for rank in range(9, 15)
    for color in range(4)
  )

  def __init__(self, name: str):
    super().__init__(name)
    self.used: set[Card] = set()

  def on_start(self):
    print("I started")
    pass

  def on_take(self, taken: list[Card]):
    print(f"I took cards {taken}")
    pass

  def on_opponent_draw(self):
    print("Opponent drew a few cards")

  def on_feedback(
      self,
      is_accusation: bool,
      is_player: bool,
      has_player_drawn_cards: bool,
      revealed: Card | None,
      taken_count: int | None
  ):
    print("I got feedback")
    if is_accusation: self.on_accusation(is_player, has_player_drawn_cards, revealed, taken_count)

  def on_accusation(self, is_player, has_player_drawn_cards, revealed, taken_count):
    print("there was an accusation!")
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
    print(f"I was wrong so I took took {taken_count} cards. Also the top card was {revealed}.")

  def on_right_accusation(self, revealed: Card, taken_count: int):
    print(f"I was right so they took {taken_count} cards. Also the top card was {revealed}.")

  def on_caught(self, taken_count: int):
    print(f"I was caught so I took {taken_count} cards.")

  def on_honest(self, taken_count: int):
    print(f"I was honest and accused so they took {taken_count} cards.")

  def declare(self, declared: Card | None):
    if not declared: self.on_opponent_draw()
    print(f"Declared card {declared}")

    valid_held_cards = [card for card in self.cards if not declared or card[0] > declared[0]]
    invalid_held_cards = [card for card in self.cards if card not in valid_held_cards]

    valid_declarable_cards = [card for card in self.Cards if not declared or card[0] > declared[0]]
    not_held_declarable_cards = [card for card in valid_declarable_cards if card not in valid_held_cards]

    if not valid_held_cards: return "draw"

    card = choice(valid_held_cards)
    return card, card

  def should_accuse(self, declared: Card):
    print(f"I wonder whether {declared} is a dirty trick.")
    return False

  def putCard(self, declared_card, *args, **kwargs):
    return self.declare(declared_card)

  def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=False, *args, **kwargs):
    self.on_feedback(checked, iChecked, iDrewCards, revealedCard, noTakenCards)

  def checkCard(self, opponent_declaration, *args, **kwargs):
    return self.should_accuse(opponent_declaration)

  def startGame(self, cards, *args, **kwargs):
    super().startGame(cards)
    self.on_start()

  def takeCards(self, taken, *args, **kwargs):
    super().takeCards(taken)
    self.on_take(taken)
