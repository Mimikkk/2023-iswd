from random import choice

from .player import Player

Card = tuple[int, int]
class AlexosPlayer(Player):
  def __init__(self, name):
    super().__init__(name)
    self.used: set[Card] = set()

  def on_start(self):
    print("I started")
    pass

  def on_take(self, taken):
    print("I took", taken)
    pass

  def on_feedback(self, is_accusation, is_player, has_player_drawn_cards, revealed, taken_count):
    print("I got feedback", is_accusation, is_player, has_player_drawn_cards, revealed, taken_count)
    if is_accusation: self.on_accusation(is_player, has_player_drawn_cards, revealed, taken_count)

  def on_accusation(self, is_player, has_player_drawn_cards, revealed, taken_count):
    print("there was an accusation!", is_player, has_player_drawn_cards, revealed, taken_count)
    if (is_player):
      if (has_player_drawn_cards):
        self.on_caught(revealed, taken_count)
      else:
        self.on_honest(revealed, taken_count)
    else:
      if (has_player_drawn_cards):
        self.on_right_accusation(revealed, taken_count)
      else:
        self.on_wrong_accusation(revealed, taken_count)


  def on_wrong_accusation(self, revealed, taken_count):
    print(f"I was wrong so I took took {taken_count} cards. Also the top card was {revealed}.")

  def on_right_accusation(self, revealed, taken_count):
    print(f"I was right so opponent took {taken_count} cards. Also the top card was {revealed}.")

  def on_caught(self, revealed, taken_count):
    print(f"I was caught by opponent so I took {taken_count} cards. Also the top card was {revealed}.")

  def on_honest(self, revealed, taken_count):
    print(f"I was honest but falsely accused by opponent so he took {taken_count} cards. Also the top card was {revealed}.")

  def declare(self, declared):
    valid_cards = [card for card in self.cards if not declared or card[0] > declared[0]]
    invalid_cards = [card for card in self.cards if declared and card[0] <= declared[0]]

    if not valid_cards: return "draw"

    card = declaration = choice(valid_cards)
    return card, declaration

  def should_accuse(self, declared):
    return False

  def putCard(self, declared_card):
    return self.declare(declared_card)

  def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=False):
    self.on_feedback(checked, iChecked, iDrewCards, revealedCard, noTakenCards)

  def checkCard(self, opponent_declaration):
    return self.should_accuse(opponent_declaration)

  def startGame(self, cards):
    super().startGame(cards)
    self.on_start()

  def takeCards(self, taken):
    super().takeCards(taken)
    self.on_take(taken)
