import random

from numpy.random import choice
from .player import Player
from ..deck import Card

class AnonPlayer(Player):
  def __init__(self, name):
    super().__init__(name)

  def putCard(self, declared_card):
    valid_cards = [card for card in self.cards if (declared_card is None) or (card[0] >= declared_card[0])]
    invalid_cards = [card for card in self.cards if card not in valid_cards]

    if not valid_cards:
      return "draw"

    if invalid_cards and random.random() < 0.5:
      true_card = random.choice(invalid_cards)
      declared_card = random.choice(valid_cards)
      return true_card, declared_card
    else:
      true_card = random.choice(valid_cards)
      return true_card, true_card

  def checkCard(self, opponent_declaration):
    if not self.cards:
      return False

    valid_cards = [card for card in self.cards if card[0] >= opponent_declaration[0]]
    cheat_likelihood = len(valid_cards) / len(self.cards)

    return random.random() < cheat_likelihood
