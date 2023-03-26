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
  epsilon = LpVariable(name='epsilon', lowBound=0, cat='Continuous')

  # variables
  variables = []
  u1_000 = LpVariable(name='u1_000', lowBound=0, cat='Continuous')
  u2_000 = LpVariable(name='u2_000', lowBound=0, cat='Continuous')
  u3_000 = LpVariable(name='u3_000', lowBound=0, cat='Continuous')
  u4_000 = LpVariable(name='u4_000', lowBound=0, cat='Continuous')
  variables += [u1_000, u2_000, u3_000, u4_000]

  u1_100 = LpVariable(name='u1_100', lowBound=0, cat='Continuous')
  u2_100 = LpVariable(name='u2_100', lowBound=0, cat='Continuous')
  u3_100 = LpVariable(name='u3_100', lowBound=0, cat='Continuous')
  u4_100 = LpVariable(name='u4_100', lowBound=0, cat='Continuous')
  variables += [u1_100, u2_100, u3_100, u4_100]

  u1_062 = LpVariable(name='u1_062', lowBound=0, cat='Continuous')
  u1_068 = LpVariable(name='u1_068', lowBound=0, cat='Continuous')
  u1_065 = LpVariable(name='u1_065', lowBound=0, cat='Continuous')
  u1_071 = LpVariable(name='u1_071', lowBound=0, cat='Continuous')
  variables += [u1_062, u1_068, u1_065, u1_071]

  u2_025 = LpVariable(name='u2_025', lowBound=0, cat='Continuous')
  u2_090 = LpVariable(name='u2_090', lowBound=0, cat='Continuous')
  u2_093 = LpVariable(name='u2_093', lowBound=0, cat='Continuous')
  u2_027 = LpVariable(name='u2_027', lowBound=0, cat='Continuous')
  u2_044 = LpVariable(name='u2_044', lowBound=0, cat='Continuous')
  variables += [u2_025, u2_090, u2_093, u2_027, u2_044]

  u3_056 = LpVariable(name='u3_056', lowBound=0, cat='Continuous')
  u3_065 = LpVariable(name='u3_065', lowBound=0, cat='Continuous')
  u3_071 = LpVariable(name='u3_071', lowBound=0, cat='Continuous')
  u3_088 = LpVariable(name='u3_088', lowBound=0, cat='Continuous')
  variables += [u3_056, u3_065, u3_071, u3_088]

  u4_049 = LpVariable(name='u4_049', lowBound=0, cat='Continuous')
  u4_073 = LpVariable(name='u4_073', lowBound=0, cat='Continuous')
  u4_050 = LpVariable(name='u4_050', lowBound=0, cat='Continuous')
  u4_054 = LpVariable(name='u4_054', lowBound=0, cat='Continuous')
  u4_060 = LpVariable(name='u4_060', lowBound=0, cat='Continuous')
  u4_055 = LpVariable(name='u4_055', lowBound=0, cat='Continuous')
  u4_067 = LpVariable(name='u4_067', lowBound=0, cat='Continuous')
  u4_065 = LpVariable(name='u4_065', lowBound=0, cat='Continuous')
  u4_082 = LpVariable(name='u4_082', lowBound=0, cat='Continuous')
  variables += [u4_049, u4_073, u4_050, u4_054, u4_060, u4_055, u4_067, u4_065, u4_082]

  # referential ranking -- constraints
  u1_083 = LpVariable(name='u1_083', lowBound=0, cat='Continuous')
  u1_040 = LpVariable(name='u1_040', lowBound=0, cat='Continuous')
  u1_078 = LpVariable(name='u1_078', lowBound=0, cat='Continuous')
  u1_064 = LpVariable(name='u1_064', lowBound=0, cat='Continuous')
  u1_065 = LpVariable(name='u1_065', lowBound=0, cat='Continuous')
  u1_071 = LpVariable(name='u1_071', lowBound=0, cat='Continuous')
  u1_062 = LpVariable(name='u1_062', lowBound=0, cat='Continuous')
  u1_068 = LpVariable(name='u1_068', lowBound=0, cat='Continuous')
  u1_074 = LpVariable(name='u1_074', lowBound=0, cat='Continuous')
  u1_060 = LpVariable(name='u1_030', lowBound=0, cat='Continuous')
  variables += [u1_083, u1_040, u1_078, u1_064, u1_065, u1_071, u1_062, u1_068, u1_074, u1_060]

  u2_025 = LpVariable(name='u2_025', lowBound=0, cat='Continuous')
  u2_090 = LpVariable(name='u2_090', lowBound=0, cat='Continuous')
  u2_027 = LpVariable(name='u2_027', lowBound=0, cat='Continuous')
  u2_044 = LpVariable(name='u2_044', lowBound=0, cat='Continuous')
  u2_030 = LpVariable(name='u2_030', lowBound=0, cat='Continuous')
  u2_040 = LpVariable(name='u2_040', lowBound=0, cat='Continuous')
  u2_093 = LpVariable(name='u2_093', lowBound=0, cat='Continuous')
  variables += [u2_025, u2_090, u2_027, u2_044, u2_030, u2_040, u2_093]

  u3_080 = LpVariable(name='u3_080', lowBound=0, cat='Continuous')
  u3_071 = LpVariable(name='u3_071', lowBound=0, cat='Continuous')
  u3_054 = LpVariable(name='u3_054', lowBound=0, cat='Continuous')
  u3_088 = LpVariable(name='u3_088', lowBound=0, cat='Continuous')
  u3_056 = LpVariable(name='u3_056', lowBound=0, cat='Continuous')
  u3_065 = LpVariable(name='u3_065', lowBound=0, cat='Continuous')
  variables += [u3_080, u3_071, u3_054, u3_088, u3_056, u3_065]

  u4_065 = LpVariable(name='u4_065', lowBound=0, cat='Continuous')
  u4_082 = LpVariable(name='u4_082', lowBound=0, cat='Continuous')
  u4_050 = LpVariable(name='u4_050', lowBound=0, cat='Continuous')
  u4_054 = LpVariable(name='u4_054', lowBound=0, cat='Continuous')
  u4_055 = LpVariable(name='u4_055', lowBound=0, cat='Continuous')
  u4_067 = LpVariable(name='u4_067', lowBound=0, cat='Continuous')
  u4_049 = LpVariable(name='u4_049', lowBound=0, cat='Continuous')
  u4_073 = LpVariable(name='u4_073', lowBound=0, cat='Continuous')
  u4_060 = LpVariable(name='u4_060', lowBound=0, cat='Continuous')
  variables += [u4_065, u4_082, u4_050, u4_054, u4_055, u4_067, u4_049, u4_073, u4_060]

  # constraints
  model += (u1_083 + u2_025 + u3_080 + u4_065 >= u1_040 + u2_090 + u3_000 + u4_082 + epsilon, '#1 constraint')
  model += (u1_078 + u2_027 + u3_071 + u4_050 >= u1_064 + u2_044 + u3_054 + u4_054 + epsilon, '#2 constraint')
  model += (u1_065 + u2_030 + u3_071 + u4_055 >= u1_071 + u2_025 + u3_088 + u4_067 + epsilon, '#3 constraint')
  model += (u1_062 + u2_040 + u3_056 + u4_050 == u1_068 + u2_040 + u3_065 + u4_060, '#4 constraint')
  model += (u1_074 + u2_025 + u3_080 + u4_049 >= u1_060 + u2_093 + u3_000 + u4_073 + epsilon, '#5 constraint')

  # normalization
  for u in [u1_000, u2_000, u3_000, u4_000]:
    model += u == 1
  #
  # normalization
  for u in [u1_100, u2_100, u3_100, u4_100]:
    model += u == 0

  # monotonicity
  model += u1_062 >= u1_068
  model += u1_065 >= u1_071
  model += u2_025 >= u2_090
  model += u2_025 >= u2_093
  model += u2_027 >= u2_044
  model += u3_056 >= u3_065
  model += u3_071 >= u3_088
  model += u4_049 >= u4_073
  model += u4_050 >= u4_054
  model += u4_050 >= u4_060
  model += u4_055 >= u4_067
  model += u4_065 >= u4_082

  # Non-negativity
  for u in variables:
    model += u <= 0

  # Objective function
  model += epsilon

  # Solve
  status = model.solve()

  # Wypisanie statusu
  print(f'status: {model.status}, {LpStatus[model.status]}')
  # WYNIK: status: 1, Optimal

  # Wypisanie realizacji funkcji celu
  print(f'objective: {model.objective.value()}')
  # WYNIK: objective : 12.000000199999999

  # Wypisanie wartosci zmiennych decyzyjnych
  # u1, u2, u3 = u1_35.value(), u2_62.value(), u3_25.value()
  # print(f'Dubov {u1} + {u2} + {u3} = {u1 + u2 + u3}')
  #
  # u1, u2, u3 = u1_7.value(), u2_55.value(), u3_12.value()
  # print(f'Elmendi {u1} + {u2} + {u3} = {u1 + u2 + u3}')
  #
  # u1, u2, u3 = u1_25.value(), u2_30.value(), u3_12.value()
  # print(f'Ferrert {u1} + {u2} + {u3} = {u1 + u2 + u3}')
  #
  # u1, u2, u3 = u1_9.value(), u2_62.value(), u3_88.value()
  # print(f'Grishuk {u1} + {u2} + {u3} = {u1 + u2 + u3}')
