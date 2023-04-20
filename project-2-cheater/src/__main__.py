import asyncio
from typing import Literal

from mod.game import Game
from mod.players.player import Player
from inspect import getmembers, isclass
from itertools import combinations_with_replacement


def analyze_matches(FirstPlayer: type[Player], SecondPlayer: type[Player], repeats: int, metrics: list[str] = None):
  stats = {"wins": [0, 0], }
  if metrics is None: metrics = sorted(stats)

  for _ in range(repeats):
    game = Game([FirstPlayer(name="first"), SecondPlayer(name="second")])

    while True:
      _, player = game.take_turn()

      if game.is_finished():
        stats["wins"][player] += 1
        break

  print(f"First  player  : {FirstPlayer.__name__}")
  print(f"Second player  : {SecondPlayer.__name__}")
  if "wins" in metrics:
    print(f"Wins           : [{stats['wins'][0] / repeats * 100:.2f}%, {stats['wins'][1] / repeats * 100:.2f}%]")


async def analyze_all_vs_all(repeats: int, metrics: list[str] = None):
  from mod import players
  players = [player for (_, player) in sorted(getmembers(players, isclass), key=lambda x: x[0])]

  for (first, second) in combinations_with_replacement(players, r=2):
    # always tie
    if first.__name__ == 'DrawPlayer' and second.__name__ == 'DrawPlayer': continue

    analyze_matches(first, second, repeats=repeats, metrics=metrics)
    print(f"-" * 50)


async def analyze_all_vs_player(
    used: type[Player],
    repeats: int,
    metrics: list[str] = None,
    start_as: Literal['first', 'second'] = 'first'
):
  from mod import players
  players = [player for (_, player) in sorted(getmembers(players, isclass), key=lambda x: x[0])]

  for player in players:
    print(player.__name__)
    first = used if start_as == 'first' else player
    second = used if start_as == 'second' else player

    analyze_matches(first, second, repeats=repeats, metrics=metrics)
    print(f"-" * 50)


async def analyze(first: type[Player], second: type[Player], repeats: int, metrics: list[str] = None):
  analyze_matches(first, second, repeats=repeats, metrics=metrics)
  print(f"-" * 50)


async def main():
  import mod.players as players
  repeats = 10000
  metrics = ['wins']
  print(f"Repeats        : {repeats}")
  print(f"Metrics        : {', '.join(metrics)}")
  print(f"-" * 50)

  print(f"As first " + "-" * 50)
  await analyze_all_vs_player(players.LiarAlexosPlayer, start_as='first', repeats=repeats, metrics=metrics)
  print(f"As second" + "-" * 50)
  await analyze_all_vs_player(players.LiarAlexosPlayer, start_as='second', repeats=repeats, metrics=metrics)


if __name__ == '__main__': asyncio.run(main())
