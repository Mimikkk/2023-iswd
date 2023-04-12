from random import choice

from .player import Player

class NaivePlayer(Player):
  def __init__(self, name):
    super().__init__(name)

  def on_start(self):
    pass

  def on_take(self, taken):
    pass

  def on_feedback(self, is_accusation, is_player, has_player_drawn_cards, revealed, taken_count):
    if is_accusation: self.on_accusation(is_player, has_player_drawn_cards, revealed, taken_count)

  def on_accusation(self, is_player, has_player_drawn_cards, revealed, taken_count):
    if (is_player):
      if (has_player_drawn_cards):
        self.on_caught(taken_count)
      else:
        self.on_uncaught(taken_count)
    else:
      if (has_player_drawn_cards):
        self.on_right_accusation(revealed, taken_count)
      else:
        self.on_wrong_accusation(revealed, taken_count)


  def on_wrong_accusation(self, revealed, taken_count):
    pass

  def on_right_accusation(self, revealed, taken_count):
    pass

  def on_caught(self, taken_count):
    pass

  def on_uncaught(self, taken_count):
    pass

  def declare(self, declared):
    valid_cards = [card for card in self.cards if not declared or card[0] > declared[0]]
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
