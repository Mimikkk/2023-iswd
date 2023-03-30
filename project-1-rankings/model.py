from matplotlib import pyplot as plt
import numpy as np
from pulp import *
from itertools import pairwise

def flattened(it):
  return [element for iterable in it for element in iterable]
def exhaust(it):
  for _ in it: pass

def rank(variants, criteria):
  ranking = {}
  for row in variants:
    variant = int(row[0]) - 1

    score = 0
    for col in range(len(criteria)):
      crit_id = int(variants[variant][col + 1] * 100)
      if crit_id < len(criteria[col]):
        idx = crit_id
      else:
        idx = crit_id - 1
      score += criteria[col][idx]
    ranking[variant + 1] = score

  return sorted(ranking.items(), key=lambda x: x[1], reverse=True)
def plot_criteria(criteria):
  _, axes = plt.subplots(2, 2, figsize=(10, 10))
  for x in [0, 1]:
    for y in [0, 1]:
      criterion = x * 2 + y
      axes[x][y].plot(
        np.linspace(0, 1.0, 100),
        criteria[criterion],
      )
      axes[x][y].set_title(f"Criterion: '{criterion + 1}'")
  plt.show()

if __name__ == '__main__':
  model = LpProblem("ordinal-regression", LpMaximize)

  epsilon = LpVariable(f"e", lowBound=0, cat=LpContinuous)
  utilities = [[LpVariable(f"u{criterion}_{i:03d}", lowBound=0, upBound=1, cat=LpContinuous)
                for i in range(0, 100 + 1)
                ] for criterion in range(4)]
  (u1, u2, u3, u4) = utilities

  # # Warunek normalizacji — Typ koszt
  model.add(u1[0] + u2[0] + u3[0] + u4[0] == 1)
  for u in utilities: model.add(u[100] == 0)

  # Wariant (15, 26) : 26 > 15
  # (u1[87], u2[3], u3[100], u4[61])
  # (u1[71], u2[25], u3[88], u4[67])
  # Wariant (01, 05) : 05 > 01
  # (u1[60], u2[93], u3[0], u4[73])
  # (u1[62], u2[40], u3[56], u4[50])
  # Wariant (07, 21) : 21 > 07
  # (u1[83], u2[25], u3[80], u4[65])
  # (u1[40], u2[90], u3[0], u4[82])
  # Wariant (03, 27) : 03 > 27
  # (u1[100], u2[45], u3[57], u4[50])
  # (u1[80], u2[6], u3[100], u4[67])
  # Wariant (06, 08) : 08 ~ 06
  # (u1[64], u2[44], u3[54], u4[54])
  # (u1[78], u2[27], u3[71], u4[50])

  # odtworzenie rankingu referencyjnego
  model.add(u1[87] + u2[3] + u3[100] + u4[61] >= u1[71] + u2[25] + u3[88] + u4[67] + epsilon)
  model.add(u1[62] + u2[40] + u3[56] + u4[50] >= u1[60] + u2[93] + u3[0] + u4[73] + epsilon)
  model.add(u1[83] + u2[25] + u3[80] + u4[65] >= u1[40] + u2[90] + u3[0] + u4[82] + epsilon)
  model.add(u1[100] + u2[45] + u3[57] + u4[50] >= u1[80] + u2[6] + u3[100] + u4[67] + epsilon)
  model.add(u1[64] + u2[44] + u3[54] + u4[54] == u1[78] + u2[27] + u3[71] + u4[50])

  used = [
    [u1[0], u1[40], u1[60], u1[62], u1[64], u1[71], u1[78], u1[80], u1[83], u1[87], u1[100]],
    [u2[0], u2[3], u2[6], u2[25], u2[27], u2[40], u2[44], u2[45], u2[90], u2[93], u2[100]],
    [u3[0], u3[54], u3[56], u3[57], u3[71], u3[80], u3[88], u3[100]],
    [u4[0], u4[50], u4[54], u4[61], u4[65], u4[67], u4[73], u4[82], u4[100]],
  ]

  # Warunek monotoniczności — Typ koszt
  for (v1, v2) in flattened(map(pairwise, used)):
    model.add(v1 >= v2)

  # Nieujemność
  for value in flattened(used):
    model.add(value >= 0)

  # Funkcja celu
  model.setObjective(epsilon)

  print(f'status: {model.status}, {LpStatus[model.status]}')

  model.solve()
  print(f"Objective: {model.objective.value()}")

  def aspair(variable):
    value = variable.value()
    value = 0 if value < 0 else value
    return int(variable.name.split("_")[1]), value

  criteria = []
  for u in used:
    arr = []
    for (amin, amax), (bmin, bmax) in pairwise(map(aspair, u)):
      print(f"{amin} {amax} {bmin} {bmax}")
      arr.extend(np.linspace(amax, bmax, (bmin - amin)))
    criteria.append(np.array(arr))

  with open("resources/nuclear-waste.csv", "r") as file:
    lines = file.readlines()[1:]
  nuclear_waste = [(*map(float, line.split(',')),) for line in lines]
  print(nuclear_waste)
  print(rank(nuclear_waste, criteria))

  plot_criteria(criteria)
