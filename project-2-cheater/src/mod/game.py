from numpy.random import randint
from . import deck

class Game(object):
  def __init__(self, players):
    self.players = players
    self.deck = deck.create()
    self.player_cards = deck.shuffled(self.deck)
    self.game_deck = self.player_cards[0] + self.player_cards[1]

    for i, cards in zip([0, 1], self.player_cards): self.players[i].startGame(cards.copy())
    self.true_card = None
    self.declared_card = None
    self.pile = []
    self.player_move = randint(2)

  def take_turn(self):
    self.player_move = 1 - self.player_move

    active = self.players[self.player_move]
    opponent = self.players[1 - self.player_move]

    decision = active.putCard(self.declared_card, self)
    if decision == "draw":
      taken = self.pile[max([-3, -len(self.pile)]):]
      for card in taken: self.pile.remove(card)
      active.takeCards(taken)

      self.declared_card = self.true_card = None
      active.getCheckFeedback(False, False, False, None, None)
      opponent.getCheckFeedback(False, False, False, None, None)
    else:
      self.true_card, self.declared_card = decision

      active.cards.remove(self.true_card)
      self.pile.append(self.true_card)

      if opponent.checkCard(self.declared_card, self):
        taken = self.pile[max([-3, -len(self.pile)]):]
        for card in taken: self.pile.remove(card)

        if not self.true_card == self.declared_card:
          active.takeCards(taken)
          active.getCheckFeedback(True, False, True, None, len(taken))
          opponent.getCheckFeedback(True, True, False, tuple(taken[-1]), len(taken))
        else:
          opponent.takeCards(taken)
          active.getCheckFeedback(True, False, False, None, len(taken))
          opponent.getCheckFeedback(True, True, True, tuple(taken[-1]), len(taken))

        self.declared_card = self.true_card = None
      else:
        active.getCheckFeedback(False, False, False, None, None)
        opponent.getCheckFeedback(False, False, False, None, None)

    return True, self.player_move

  def is_finished(self):
    return not self.players[self.player_move].cards
