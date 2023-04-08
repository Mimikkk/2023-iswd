from mod.game import Game
from mod import players

def analyze(FirstPlayer, SecondPlayer, repeats=100):
  stats_wins = [0, 0]
  stats_moves = [0, 0]
  stats_cheats = [0, 0]
  stats_errors = [0, 0]
  stats_cards = [0, 0]
  stats_checks = [0, 0]
  stats_draw_decisions = [0, 0]
  stats_pile_size = 0
  errors = 0

  for t in range(repeats):
    game = Game([FirstPlayer(name="first"), SecondPlayer(name="second")], log=False)

    error = False
    while True:
      valid, player = game.takeTurn(log=False)
      if not valid:
        error = True
        stats_errors[player] += 1
        errors += 1
        break
      if game.isFinished(log=False):
        stats_wins[player] += 1
        break

    stats_pile_size += len(game.pile)
    if not error:
      for j in range(2):
        stats_moves[j] += game.moves[j]
        stats_cheats[j] += game.cheats[j]
        stats_checks[j] += game.checks[j]
        stats_draw_decisions[j] += game.draw_decisions[j]
        stats_cards[j] += len(game.player_cards[j])

  stats_pile_size /= (repeats - errors)

  for j in range(2):
    stats_moves[j] /= (repeats - errors)
    stats_cheats[j] /= (repeats - errors)
    stats_checks[j] /= (repeats - errors)
    stats_draw_decisions[j] /= (repeats - errors)
    stats_cards[j] /= (repeats - errors)

  print(f"First  player  : {FirstPlayer.__name__}")
  print(f"Second player  : {SecondPlayer.__name__}")
  print(f"Wins           : {stats_wins}")
  print(f"Moves          : {stats_moves}")
  print(f"Cards          : {stats_cards}")
  print(f"Pile size      : {stats_pile_size}")
  print(f"Checks         : {stats_checks}")
  print(f"Draw decisions : {stats_draw_decisions}")
  print(f"Cheats         : {stats_cheats}")
  print(f"Errors         : {stats_errors}")
  print(f"Total errors   : {errors}")

if __name__ == '__main__':
  analyze(players.SimplePlayer, players.SimplePlayer, repeats=100)
