from random import sample

Card = tuple[int, int]
Deck = list[Card]


def create() -> Deck:
  return [(number, color) for color in range(4) for number in range(9, 15)]

def shuffled(deck: Deck) -> tuple[Deck, Deck, Deck]:
  cards = set(deck)
  first_cards = set(sample(deck, 8))
  second_cards = set(sample(list(cards - first_cards), 8))
  unused = cards - first_cards - second_cards

  return list(first_cards), list(second_cards), list(unused)
