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
  u1_0 = LpVariable(name='u1_0', lowBound=0, cat='Continuous')
  u2_0 = LpVariable(name='u2_0', lowBound=0, cat='Continuous')
  u3_0 = LpVariable(name='u3_0', lowBound=0, cat='Continuous')
  u4_0 = LpVariable(name='u4_0', lowBound=0, cat='Continuous')
  variables += [u1_0, u2_0, u3_0, u4_0]
  u1_100 = LpVariable(name='u_100', lowBound=0, cat='Continuous')
  u2_100 = LpVariable(name='u_100', lowBound=0, cat='Continuous')
  u3_100 = LpVariable(name='u_100', lowBound=0, cat='Continuous')
  u4_100 = LpVariable(name='u_100', lowBound=0, cat='Continuous')
  variables += [u1_100, u2_100, u3_100, u4_100]

  u1_62 = LpVariable(name='u1_62', lowBound=0, cat='Continuous')
  u1_68 = LpVariable(name='u1_68', lowBound=0, cat='Continuous')
  u1_65 = LpVariable(name='u1_65', lowBound=0, cat='Continuous')
  u1_71 = LpVariable(name='u1_71', lowBound=0, cat='Continuous')
  variables += [u1_62, u1_68, u1_65, u1_71]

  u2_25 = LpVariable(name='u1_25', lowBound=0, cat='Continuous')
  u2_90 = LpVariable(name='u1_90', lowBound=0, cat='Continuous')
  u2_93 = LpVariable(name='u1_93', lowBound=0, cat='Continuous')
  u2_27 = LpVariable(name='u1_27', lowBound=0, cat='Continuous')
  u2_44 = LpVariable(name='u1_44', lowBound=0, cat='Continuous')
  variables += [u2_25, u2_90, u2_93, u2_27, u2_44]

  u3_56 = LpVariable(name='u1_56', lowBound=0, cat='Continuous')
  u3_65 = LpVariable(name='u1_65', lowBound=0, cat='Continuous')
  u3_71 = LpVariable(name='u1_71', lowBound=0, cat='Continuous')
  u3_88 = LpVariable(name='u1_88', lowBound=0, cat='Continuous')
  variables += [u3_56, u3_65, u3_71, u3_88]

  u4_49 = LpVariable(name='u1_49', lowBound=0, cat='Continuous')
  u4_73 = LpVariable(name='u1_73', lowBound=0, cat='Continuous')
  u4_50 = LpVariable(name='u1_50', lowBound=0, cat='Continuous')
  u4_54 = LpVariable(name='u1_54', lowBound=0, cat='Continuous')
  u4_60 = LpVariable(name='u1_60', lowBound=0, cat='Continuous')
  u4_55 = LpVariable(name='u1_55', lowBound=0, cat='Continuous')
  u4_67 = LpVariable(name='u1_67', lowBound=0, cat='Continuous')
  u4_65 = LpVariable(name='u1_65', lowBound=0, cat='Continuous')
  u4_82 = LpVariable(name='u1_82', lowBound=0, cat='Continuous')
  variables += [u4_49, u4_73, u4_50, u4_54, u4_60, u4_55, u4_67, u4_65, u4_82]

  # referential ranking -- constraints
  u1_83 = LpVariable(name='u1_83', lowBound=0, cat='Continuous')
  u1_40 = LpVariable(name='u1_40', lowBound=0, cat='Continuous')
  u1_78 = LpVariable(name='u1_78', lowBound=0, cat='Continuous')
  u1_64 = LpVariable(name='u1_64', lowBound=0, cat='Continuous')
  u1_65 = LpVariable(name='u1_65', lowBound=0, cat='Continuous')
  u1_71 = LpVariable(name='u1_71', lowBound=0, cat='Continuous')
  u1_62 = LpVariable(name='u1_62', lowBound=0, cat='Continuous')
  u1_68 = LpVariable(name='u1_68', lowBound=0, cat='Continuous')
  u1_74 = LpVariable(name='u1_74', lowBound=0, cat='Continuous')
  u1_60 = LpVariable(name='u1_30', lowBound=0, cat='Continuous')
  variables += [u1_83, u1_40, u1_78, u1_64, u1_65, u1_71, u1_62, u1_68, u1_74, u1_60]

  u2_25 = LpVariable(name='u2_25', lowBound=0, cat='Continuous')
  u2_90 = LpVariable(name='u2_90', lowBound=0, cat='Continuous')
  u2_27 = LpVariable(name='u2_27', lowBound=0, cat='Continuous')
  u2_44 = LpVariable(name='u2_44', lowBound=0, cat='Continuous')
  u2_30 = LpVariable(name='u2_30', lowBound=0, cat='Continuous')
  u2_40 = LpVariable(name='u2_40', lowBound=0, cat='Continuous')
  u2_93 = LpVariable(name='u2_93', lowBound=0, cat='Continuous')
  variables += [u2_25, u2_90, u2_27, u2_44, u2_30, u2_40, u2_93]

  u3_80 = LpVariable(name='u3_80', lowBound=0, cat='Continuous')
  u3_71 = LpVariable(name='u3_71', lowBound=0, cat='Continuous')
  u3_54 = LpVariable(name='u3_54', lowBound=0, cat='Continuous')
  u3_88 = LpVariable(name='u3_88', lowBound=0, cat='Continuous')
  u3_56 = LpVariable(name='u3_56', lowBound=0, cat='Continuous')
  u3_65 = LpVariable(name='u3_65', lowBound=0, cat='Continuous')
  variables += [u3_80, u3_71, u3_54, u3_88, u3_56, u3_65]

  u4_65 = LpVariable(name='u4_65', lowBound=0, cat='Continuous')
  u4_82 = LpVariable(name='u4_82', lowBound=0, cat='Continuous')
  u4_50 = LpVariable(name='u4_50', lowBound=0, cat='Continuous')
  u4_54 = LpVariable(name='u4_54', lowBound=0, cat='Continuous')
  u4_55 = LpVariable(name='u4_55', lowBound=0, cat='Continuous')
  u4_67 = LpVariable(name='u4_67', lowBound=0, cat='Continuous')
  u4_49 = LpVariable(name='u4_49', lowBound=0, cat='Continuous')
  u4_73 = LpVariable(name='u4_73', lowBound=0, cat='Continuous')
  u4_60 = LpVariable(name='u4_60', lowBound=0, cat='Continuous')
  variables += [u4_65, u4_82, u4_50, u4_54, u4_55, u4_67, u4_49, u4_73, u4_60]

  # constraints
  model += (u1_83 + u2_25 + u3_80 + u4_65 >= u1_40 + u2_90 + u3_0 + u4_82 + epsilon, '#1 constraint')
  model += (u1_78 + u2_27 + u3_71 + u4_50 >= u1_64 + u2_44 + u3_54 + u4_54 + epsilon, '#2 constraint')
  model += (u1_65 + u2_30 + u3_71 + u4_55 >= u1_71 + u2_25 + u3_88 + u4_67 + epsilon, '#3 constraint')
  model += (u1_62 + u2_40 + u3_56 + u4_50 == u1_68 + u2_40 + u3_65 + u4_60, '#4 constraint')
  model += (u1_74 + u2_25 + u3_80 + u4_49 >= u1_60 + u2_93 + u3_0 + u4_73 + epsilon, '#5 constraint')

  # normalization
  for u in [u1_0, u2_0, u3_0, u4_0]:
    model += u == 0

  # normalization
  for u in [u1_100, u2_100, u3_100, u4_100]:
    model += u == 1

  # monotonicity
  model += u1_62 >= u1_68
  model += u1_65 >= u1_71
  model += u2_25 >= u2_90
  model += u2_25 >= u2_93
  model += u2_27 >= u2_44
  model += u3_56 >= u3_65
  model += u3_71 >= u3_88
  model += u4_49 >= u4_73
  model += u4_50 >= u4_54
  model += u4_50 >= u4_60
  model += u4_55 >= u4_67
  model += u4_65 >= u4_82

  # Non-negativity
  for u in variables: model += u >= 0

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
