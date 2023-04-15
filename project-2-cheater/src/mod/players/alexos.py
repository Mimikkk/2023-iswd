from random import choice

from .extended_player import ExtendedPlayer

Card = tuple[int, int]
class AlexosPlayer(ExtendedPlayer):
  def on_start(self):
    print("I started")

  def on_take(self, taken: list[Card]):
    print(f"I took cards {taken}")

  def on_opponent_draw(self):
    print("Opponent drew a few cards")

  def on_feedback(self):
    print("I got feedback")

  def on_wrong_accusation(self, revealed: Card, taken_count: int):
    print(f"I was wrong so I took took {taken_count} cards. Also the top card was {revealed}.")

  def on_right_accusation(self, revealed: Card, taken_count: int):
    print(f"I was right so they took {taken_count} cards. Also the top card was {revealed}.")

  def on_caught(self, taken_count: int):
    print(f"I was caught so I took {taken_count} cards.")

  def on_honest(self, taken_count: int):
    print(f"I was honest and accused so they took {taken_count} cards.")

  def declare(self, declared: Card | None):
    print(f"I'm declaring a card. I've started with {declared}.")
    valid_held_cards = [card for card in self.cards if not declared or card[0] >= declared[0]]

    if not valid_held_cards: return "draw"

    card = declaration = choice(valid_held_cards)
    return card, declaration

  def should_accuse(self, declared: Card):
    print(f"I wonder whether {declared} is a dirty trick.")
    return False
