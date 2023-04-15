from numpy import array
from numpy.random import randint
from . import deck

class Game(object):
  def __init__(self, players, log=False):
    self.players = players
    self.deck = deck.create()
    self.player_cards = deck.shuffled(self.deck)
    self.game_deck = self.player_cards[0] + self.player_cards[1]

    self.cheats = [0, 0]
    self.moves = [0, 0]
    self.checks = [0, 0]
    self.draw_decisions = [0, 0]

    for i, cards in zip([0, 1], self.player_cards):
      self.players[i].startGame(cards.copy())

    # Which card is on top
    self.true_card = None
    # Which card was declared by active player
    self.declared_card = None

    # Init pile: [-1] = top card
    self.pile = []

    # Which player moves
    self.player_move = randint(2)

  def takeTurn(self, log=False):
    self.player_move = 1 - self.player_move

    active = self.players[self.player_move]
    opponent = self.players[1 - self.player_move]

    decision = active.putCard(self.declared_card)
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

      if opponent.checkCard(self.declared_card):
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

  def isFinished(self, log=False):
    return not self.players[self.player_move].cards

  def debugMove(self):
    if (self.previous_declaration is not None) and (self.true_card[0] < self.previous_declaration[0]) and \
        len(self.players[self.player_move].cards) == 1:
      print("[ERROR] Last played card should be valid (it is revealed, you cannot cheat)!")
      return False
    if array(self.true_card).size != 2:
      print("[ERROR] You put too many cards!")
      return False
    if self.true_card not in self.player_cards[self.player_move]:
      print("[ERROR] You do not have this card!")
      return False
    if self.true_card not in self.deck:
      print("[ERROR] There is no such card!")
      return False
    if (self.previous_declaration is not None) and len(self.pile) == 0:
      print("[ERROR] Inconsistency")
      return False
    if (self.previous_declaration is not None) and (self.declared_card[0] < self.previous_declaration[0]):
      print(len(self.pile))
      print(self.previous_declaration)
      print(self.declared_card)
      print(self.pile[-1])
      print("[ERROR] Improper move!")
      return False
    return True

  def debugGeneral(self):
    A = set(self.players[0].cards)
    B = set(self.players[1].cards)
    C = set(self.player_cards[0])
    D = set(self.player_cards[1])
    P = set(self.pile)
    E = set(self.game_deck)

    if not A == C:
      print("Error 001")
      return False
    if not B == D:
      print("Error 002")
      return False
    if not A | B | P == E:
      print("Error 003")
      print(A)
      print(B)
      print(P)
      print(E)
      return False
    return True
