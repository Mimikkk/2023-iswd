import asyncio
from mod.game import Game
from mod.players.player import Player
from inspect import getmembers, isclass
from itertools import combinations_with_replacement

async def analyze_matches(FirstPlayer: type[Player], SecondPlayer: type[Player], repeats: int, timeout: float):
  stats = {
    "wins": [0, 0],
    "moves": [0, 0],
    "cheats": [0, 0],
    "errors": [0, 0],
    "cards": [0, 0],
    "checks": [0, 0],
    "draw_decisions": [0, 0],
    "pile_size": 0
  }

  errors = 0

  for t in range(repeats):
    game = Game([FirstPlayer(name="first"), SecondPlayer(name="second")])

    error = False
    while True:
      try:
        async def task(): return game.takeTurn()
        valid, player = await asyncio.wait_for(task(), timeout=timeout)
      except asyncio.TimeoutError:
        valid = False
        player = game.player_move
      # task

      if not valid:
        error = True
        stats["errors"][player] += 1
        errors += 1
        break
      if game.isFinished():
        stats["wins"][player] += 1
        break

    stats["pile_size"] += len(game.pile)
    if not error:
      for player in range(2):
        stats["moves"][player] += game.moves[player]
        stats["cheats"][player] += game.cheats[player]
        stats["checks"][player] += game.checks[player]
        stats["draw_decisions"][player] += game.draw_decisions[player]
        stats["cards"][player] += len(game.player_cards[player])

  stats["pile_size"] /= (repeats - errors)

  for player in range(2):
    stats["moves"][player] /= (repeats - errors)
    stats["cheats"][player] /= (repeats - errors)
    stats["checks"][player] /= (repeats - errors)
    stats["draw_decisions"][player] /= (repeats - errors)
    stats["cards"][player] /= (repeats - errors)

  print(f"First  player  : {FirstPlayer.__name__}")
  print(f"Second player  : {SecondPlayer.__name__}")
  print(f"Repeats        : {repeats}")
  print(f"-" * 50)
  print(f"Wins           : [{stats['wins'][0] / repeats * 100:.2f}%, {stats['wins'][1] / repeats * 100:.2f}%]")
  print(f"Moves          : {stats['moves']}")
  print(f"Cards          : {stats['cards']}")
  print(f"Pile size      : {stats['pile_size']}")
  print(f"Checks         : {stats['checks']}")
  print(f"Draw decisions : {stats['draw_decisions']}")
  print(f"Cheats         : {stats['cheats']}")
  print(f"Errors         : {stats['errors']}")
  print(f"Total errors   : {errors}")

async def main():
  from mod import players
  players = [player for (_, player) in sorted(getmembers(players, isclass), key=lambda x: x[0])]

  for (first, second) in combinations_with_replacement(players, r=2):
    print(first.__name__, second.__name__)

    try:
      task = asyncio.create_task(analyze_matches(first, second, repeats=100, timeout=1))
      await asyncio.wait({task}, timeout=5)
    except asyncio.TimeoutError:
      print("Timeout")
    print()

if __name__ == '__main__': asyncio.run(main())
