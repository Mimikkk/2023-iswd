import asyncio
from mod.game import Game
from mod.players.player import Player
from inspect import getmembers, isclass
from itertools import combinations_with_replacement

async def analyze_matches(FirstPlayer: type[Player], SecondPlayer: type[Player], repeats: int, timeout: float,
                          metrics: list[str] = None):
  stats = {"wins": [0, 0], }
  if metrics is None: metrics = sorted(stats)

  for _ in range(repeats):
    game = Game([FirstPlayer(name="first"), SecondPlayer(name="second")])

    while True:
      try:
        async def task(): return game.take_turn()
        _, player = await asyncio.wait_for(task(), timeout=timeout)
      except asyncio.TimeoutError:
        player = game.player_move

      if game.is_finished():
        print(player)
        stats["wins"][player] += 1
        break

  print(f"First  player  : {FirstPlayer.__name__}")
  print(f"Second player  : {SecondPlayer.__name__}")
  if "wins" in metrics:
    print(f"Wins           : [{stats['wins'][0] / repeats * 100:.2f}%, {stats['wins'][1] / repeats * 100:.2f}%]")

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
  await analyze_all_vs_player(used=players.DanielosPlayer, repeats=repeats, timeout=timeout, metrics=metrics)

if __name__ == '__main__': asyncio.run(main())
