import asyncio
from mod.game import Game
from mod.players.player import Player
from inspect import getmembers, isclass
from itertools import combinations_with_replacement

async def analyze_matches(FirstPlayer: type[Player], SecondPlayer: type[Player], repeats: int, timeout: float,
                          metrics: list[str] = None):
  if metrics is None: metrics = ['wins', 'moves', 'cheats', 'errors', 'cards', 'checks', 'draw_decisions', 'pile_size']

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
  if "wins" in metrics:
    print(f"Wins           : [{stats['wins'][0] / repeats * 100:.2f}%, {stats['wins'][1] / repeats * 100:.2f}%]")
  if "moves" in metrics:
    print(f"Moves          : {stats['moves']}")
  if "cheats" in metrics:
    print(f"Cheats         : {stats['cheats']}")
  if "errors" in metrics:
    print(f"Errors         : {stats['errors']}")
    print(f"Total errors   : {errors}")
  if "cards" in metrics:
    print(f"Cards          : {stats['cards']}")
  if "checks" in metrics:
    print(f"Checks         : {stats['checks']}")
  if "draw_decisions" in metrics:
    print(f"Draw decisions : {stats['draw_decisions']}")
  if "pile_size" in metrics:
    print(f"Pile size      : {stats['pile_size']}")

async def analyze_all_vs_all(repeats: int, timeout: float, metrics: list[str] = None):
  from mod import players
  players = [player for (_, player) in sorted(getmembers(players, isclass), key=lambda x: x[0])]

  for (first, second) in combinations_with_replacement(players, r=2):
    # always tie
    if first.__name__ == 'DrawPlayer' and second.__name__ == 'DrawPlayer': continue

    try:
      task = asyncio.create_task(analyze_matches(first, second, repeats=repeats, timeout=timeout, metrics=metrics))
      await asyncio.wait({task}, timeout=5)
    except asyncio.TimeoutError:
      print("Timeout")
    print(f"-" * 50)

async def analyze_all_vs_player(used: type[Player], repeats: int, timeout: float, metrics: list[str] = None):
  from mod import players
  players = [players.NaivePlayer]
  # players = [player for (_, player) in sorted(getmembers(players, isclass), key=lambda x: x[0])]
  for player in players:
    try:
      print(player.__name__)
      task = asyncio.create_task(analyze_matches(used, player, repeats=repeats, timeout=timeout, metrics=metrics))
      await asyncio.wait({task}, timeout=5)
    except asyncio.TimeoutError:
      print("Timeout")
    print(f"-" * 50)

async def main():
  import mod.players as players
  repeats = 1
  timeout = 5
  metrics = ['wins']
  print(f"Repeats        : {repeats}")
  print(f"Timeout        : {timeout}")
  print(f"Metrics        : {', '.join(metrics)}")
  print(f"-" * 50)
  await analyze_all_vs_player(used=players.AlexosPlayer, repeats=repeats, timeout=timeout, metrics=metrics)

if __name__ == '__main__': asyncio.run(main())
