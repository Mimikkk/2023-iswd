import numpy as np
from pulp import *

if __name__ == '__main__':
  # Opt for:
  # C3 (Group 1 -- Optimistic  -- Future cost minimization)
  # C4 (Group 4 -- Pessimistic -- Risk cost minimization and current)
  # Minimization For:  C3 > C1 >= C2 > C4
  # Index,C1,   C2,   C3,   C4

  # Referencyjne wartości

  # Daniel
  # 7,  0.40, 0.90, 0.00, 0.82 -- 80% / 34%
  # 21, 0.83, 0.25, 0.80, 0.65
  # 7  -- Low  C3   | High   C4 --
  # 21 -- High C4   | Medium C4 -- Preferowane      -- 5

  # Alex
  # 8,  0.64, 0.44, 0.54, 0.54 -- 17% /  8%
  # 6,  0.78, 0.27, 0.71, 0.50
  # 8  -- Medium C3 | Medium C4 --
  # 6  -- High   C4 | Medium C4 -- Preferowane      -- 3

  # Random 1 0.5 - 1.0
  # 26, 0.71, 0.25, 0.88, 0.67 -- 17% / 24%
  # 9,  0.65, 0.30, 0.71, 0.55
  # 26 -- High   C3 | Medium C4 --
  # 9  -- High   C4 | Medium C4 -- Preferowane      -- 4

  # Random 2
  # 17, 0.68, 0.40, 0.65, 0.60 --  9% / 20%
  # 5 , 0.62, 0.40, 0.56, 0.50
  # 17 -- High   C3 | Medium C4 --
  # 5  -- Medium C4 | Medium C4 -- Nierozróżnialny  -- 2

  # Random 3
  # 1,  0.60, 0.93, 0.00, 0.73 -- 80% / 48%
  # 12, 0.74, 0.25, 0.80, 0.49
  # 1   -- Low  C3  | High C4   --
  # 12  -- High C4  | Medium C4 -- Preferowane      -- 1

  # I     C1,   C2,   C3,   C4 | P | Rank
  # P1 -----------------------------
  # 7,  0.40, 0.90, 0.00, 0.82 | 0 |
  # 21, 0.83, 0.25, 0.80, 0.65 | 1 |
  # P2 -----------------------------
  # 8,  0.64, 0.44, 0.54, 0.54 | 0 |
  # 6,  0.78, 0.27, 0.71, 0.50 | 1 |
  # P3 -----------------------------
  # 26, 0.71, 0.25, 0.88, 0.67 | 0 |
  # 9,  0.65, 0.30, 0.71, 0.55 | 1 |
  # P4 -----------------------------
  # 17, 0.68, 0.40, 0.65, 0.60 | ~ |
  # 5 , 0.62, 0.40, 0.56, 0.50 | ~ |
  # P5 -----------------------------
  # 1,  0.60, 0.93, 0.00, 0.73 | 0 |
  # 12, 0.74, 0.25, 0.80, 0.49 | 1 |
  # 0 -- Niepreferowane nad
  # 1 -- Preferowane nad
  # ~ -- nierozróżnialne

  # max: e
  # o1: u1(0.83) + u2(0.25) + u3(0.80) + u4(0.65) >= u1(0.40) + u2(0.90) + u3(0.00) + u4(0.82) + e
  # o2: u1(0.78) + u2(0.27) + u3(0.71) + u4(0.50) >= u1(0.64) + u2(0.44) + u3(0.54) + u4(0.54) + e
  # o3: u1(0.65) + u2(0.30) + u3(0.71) + u4(0.55) >= u1(0.71) + u2(0.25) + u3(0.88) + u4(0.67) + e
  # o4: u1(0.62) + u2(0.40) + u3(0.56) + u4(0.50) == u1(0.68) + u2(0.40) + u3(0.65) + u4(0.60)
  # o5: u1(0.74) + u2(0.25) + u3(0.80) + u4(0.49) >= u1(0.60) + u1(0.93) + u3(0.00) + u4(0.73) + e

  # normalization
  # sum of u_i = 1
  # forall u_i(0) = 0

  # monotonicity
  # u1(0.62) >= u1(0.68)
  # u1(0.65) >= u1(0.71)
  # u2(0.25) >= u2(0.90)
  # u2(0.25) >= u2(0.93)
  # u2(0.27) >= u2(0.44)
  # u3(0.56) >= u3(0.65)
  # u3(0.71) >= u3(0.88)
  # u4(0.49) >= u4(0.73)
  # u4(0.50) >= u4(0.54)
  # u4(0.50) >= u4(0.60)
  # u4(0.55) >= u4(0.67)
  # u4(0.65) >= u4(0.82)

  # non-negativity
  # forall u_i >= 0

  # Informacja o informacji preferencyjnej
  # C3 (Group 1 -- Optimistic  -- Future cost minimization)
  # C4 (Group 4 -- Pessimistic -- Risk cost minimization and current)
  # Preferencja została określona jako konieczna minimalizacja kosztu ryzyka (C4),
  # oraz ignorowanie wobec kosztów teraźniejszych (C2)  wobec pozostałych kryteriów, co ustawia
  # nasz ranking kryteriów jako C3 >= C1 ~ C2 >= C4
  # Co oznacza, że C4 ma być jak najmniejsze, a C3 od C1 i C2 może być mniejsze bądź równe.

  # Scenarios
  # | S | ILW | HLW |
  # | --- | --- | --- |
  # | S1 | 10 | 30 |
  # | S2 | 30 | 30 |
  # | S3 | 50 | 50 |
  # S -- Scenario
  # ILW -- Intermediate Level Waste
  # HLW -- High Level Waste
  # S1 -- Scenario 1
  # S2 -- Scenario 2
  # S3 -- Scenario 3
  # S1: 10 ILW + 30 HLW
  # S2: 30 ILW + 30 HLW
  # S3: 50 ILW + 50 HLW
  # C1 -- COST -- Group 3 Pessimistic -- Total financial cost
  # C2 -- COST -- Group 2 Pessimistic -- Cost incurred by the present consumers
  # C3 -- COST -- Group 1 Optimistic  -- Cost to be supported by the future consumers
  # C4 -- COST -- Group 4 Pessimistic -- Risk due to overcosts

  # max: e
  # o1: u1(0.83) + u2(0.25) + u3(0.80) + u4(0.65) >= u1(0.40) + u2(0.90) + u3(0.00) + u4(0.82) + e
  # o2: u1(0.78) + u2(0.27) + u3(0.71) + u4(0.50) >= u1(0.64) + u2(0.44) + u3(0.54) + u4(0.54) + e
  # o3: u1(0.65) + u2(0.30) + u3(0.71) + u4(0.55) >= u1(0.71) + u2(0.25) + u3(0.88) + u4(0.67) + e
  # o4: u1(0.62) + u2(0.40) + u3(0.56) + u4(0.50) == u1(0.68) + u2(0.40) + u3(0.65) + u4(0.60)
  # o5: u1(0.74) + u2(0.25) + u3(0.80) + u4(0.49) >= u1(0.60) + u1(0.93) + u3(0.00) + u4(0.73) + e

  # normalization
  # sum of u_i = 1
  # forall u_i(0) = 0

  # monotonicity
  # u1(0.62) >= u1(0.68)
  # u1(0.65) >= u1(0.71)
  # u2(0.25) >= u2(0.90)
  # u2(0.25) >= u2(0.93)
  # u2(0.27) >= u2(0.44)
  # u3(0.56) >= u3(0.65)
  # u3(0.71) >= u3(0.88)
  # u4(0.49) >= u4(0.73)
  # u4(0.50) >= u4(0.54)
  # u4(0.50) >= u4(0.60)
  # u4(0.55) >= u4(0.67)
  # u4(0.65) >= u4(0.82)

  # non-negativity
  # forall u_i >= 0
  model = LpProblem(name='problem', sense=LpMaximize)

  # objective function
  epsilon = LpVariable(name='epsilon', cat='Continuous')

  # variables
  vars = {}
  for u in range(0, 100 + 1):
    for i in range(1, 4 + 1):
      vars[f'u{i}_{u:03d}'] = LpVariable(name=f'u{i}_{u:03d}', cat='Continuous', lowBound=0, upBound=1)
  vars['epsilon'] = epsilon

  model.addConstraint(
    (vars['u1_083'] + vars['u2_025'] + vars['u3_080'] + vars['u4_065']
     >= vars['u1_040'] + vars['u2_090'] + vars['u3_000'] + vars['u4_082'] + vars['epsilon']),
    '#1 constraint'
  )
  model.addConstraint(
    (vars['u1_078'] + vars['u2_027'] + vars['u3_071'] + vars['u4_050']
     >= vars['u1_064'] + vars['u2_044'] + vars['u3_054'] + vars['u4_054'] + vars['epsilon']),
    '#2 constraint'
  )
  model.addConstraint(
    (vars['u1_065'] + vars['u2_030'] + vars['u3_071'] + vars['u4_055']
     >= vars['u1_071'] + vars['u2_025'] + vars['u3_088'] + vars['u4_067'] + vars['epsilon']),
    '#3 constraint'
  )
  model.addConstraint(
    (vars['u1_062'] + vars['u2_040'] + vars['u3_056'] + vars['u4_050']
     == vars['u1_068'] + vars['u2_040'] + vars['u3_065'] + vars['u4_060']),
    '#4 constraint'
  )
  model.addConstraint(
    (vars['u1_074'] + vars['u2_025'] + vars['u3_080'] + vars['u4_049']
     >= vars['u1_060'] + vars['u2_093'] + vars['u3_000'] + vars['u4_073'] + vars['epsilon']),
    '#5 constraint'
  )
  # monotonicity
  model.addConstraint(vars['u1_000'] <= vars['u1_100'])
  model.addConstraint(vars['u2_000'] <= vars['u2_100'])
  model.addConstraint(vars['u3_000'] <= vars['u3_100'])
  model.addConstraint(vars['u4_000'] <= vars['u4_100'])
  model.addConstraint(vars['u1_062'] >= vars['u1_068'])
  model.addConstraint(vars['u1_065'] >= vars['u1_071'])
  model.addConstraint(vars['u2_025'] >= vars['u2_090'])
  model.addConstraint(vars['u2_025'] >= vars['u2_093'])
  model.addConstraint(vars['u2_027'] >= vars['u2_044'])
  model.addConstraint(vars['u3_056'] >= vars['u3_065'])
  model.addConstraint(vars['u3_071'] >= vars['u3_088'])
  model.addConstraint(vars['u4_049'] >= vars['u4_073'])
  model.addConstraint(vars['u4_050'] >= vars['u4_054'])
  model.addConstraint(vars['u4_050'] >= vars['u4_060'])
  model.addConstraint(vars['u4_055'] >= vars['u4_067'])
  model.addConstraint(vars['u4_065'] >= vars['u4_082'])

  for u in range(1, 4 + 1):
    for i in range(2, 100 + 1):
      model.addConstraint(vars[f'u{u}_{i - 1:03d}'] >= vars[f'u{u}_{i:03d}'])

  model.addConstraint(vars[f'u1_000'] + vars[f'u2_000'] + vars[f'u3_000'] + vars[f'u4_000'] == 1)

  model.setObjective(epsilon)
  # Solve
  status = model.solve()

  # Wypisanie statusu
  print(f'status: {model.status}, {LpStatus[model.status]}')
  # WYNIK: status: 1, Optimal

  # Wypisanie realizacji funkcji celu
  print(f'objective: {model.objective.value()}')
  # WYNIK: objective : 12.000000199999999

  # Wypisanie wartości zmiennych decyzyjnych
  print(f'epsilon: {epsilon.value()}')

  # zaladowanie wszystkich wariantow
  variants = {
    "1": (0.60, 0.93, 0.00, 0.73),
    "2": (0.66, 0.55, 0.45, 0.49),
    "3": (1.00, 0.45, 0.57, 0.50),
    "4": (0.48, 0.87, 0.00, 0.75),
    "5": (0.62, 0.40, 0.56, 0.50),
    "6": (0.78, 0.27, 0.71, 0.50),
    "7": (0.40, 0.90, 0.00, 0.82),
    "8": (0.64, 0.44, 0.54, 0.54),
    "9": (0.65, 0.30, 0.71, 0.55),
    "10": (0.45, 0.86, 0.00, 0.73),
    "11": (0.61, 0.54, 0.38, 0.49),
    "12": (0.74, 0.25, 0.80, 0.49),
    "13": (0.48, 0.97, 0.00, 0.91),
    "14": (0.69, 0.49, 0.56, 0.61),
    "15": (0.87, 0.03, 1.00, 0.61),
    "16": (0.44, 0.95, 0.00, 0.90),
    "17": (0.68, 0.40, 0.65, 0.60),
    "18": (0.76, 0.06, 1.00, 0.60),
    "19": (0.35, 0.91, 0.00, 0.98),
    "20": (0.64, 0.22, 0.81, 0.65),
    "21": (0.83, 0.25, 0.80, 0.65),
    "22": (0.32, 0.83, 0.00, 0.94),
    "23": (0.59, 0.24, 0.70, 0.63),
    "24": (0.73, 0.03, 1.00, 0.63),
    "25": (0.34, 1.00, 1.00, 1.00),
    "26": (0.71, 0.25, 0.88, 0.67),
    "27": (0.80, 0.06, 1.00, 0.67)
  }

  # wypisanie wartosci zmiennych
  for g1, g2, g3, g4 in variants.values():
    g1, g2, g3, g4 = map(lambda x: int(x * 100), [g1, g2, g3, g4])
    u1, u2, u3, u4 = [vars[f"u1_{g1:03d}"], vars[f"u2_{g2:03d}"], vars[f"u3_{g3:03d}"], vars[f"u4_{g4:03d}"]]
    v1, v2, v3, v4 = map(lambda x: x.value(), [u1, u2, u3, u4])
    print(f'u1_{g1:03d} = {v1}, u2_{g2:03d} = {v2}, u3_{g3:03d} = {v3}, u4_{g4:03d} = {v4}')
