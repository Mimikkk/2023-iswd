from mod.game import Game
from mod import players

def analyze(FirstPlayer, SecondPlayer, repeats=100):
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
    game = Game([FirstPlayer(name="first"), SecondPlayer(name="second")], log=False)

    error = False
    while True:
      valid, player = game.takeTurn(log=False)
      if not valid:
        error = True
        stats["errors"][player] += 1
        errors += 1
        break
      if game.isFinished(log=False):
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

if __name__ == '__main__':
  analyze(players.SimplePlayer, players.SimplePlayer, repeats=1000)
