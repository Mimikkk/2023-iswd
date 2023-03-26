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
  # u1(0.83) + u2(0.25) + u3(0.8) + u4(0.65) >= u1(0.4) + u2(0.9) + u3(0.0) + u4(0.82) + epsilon
  # o1: e + 0.4 + 0.9 + 0.0 + 0.82 <= 0.83 + 0.25 + 0.8 + 0.65
  # o2: e + 0.64 + 0.44 + 0.54 + 0.54 <= 0.78 + 0.27 + 0.71 + 0.50
  # o3: e + 0.71 + 0.25 + 0.88 + 0.67 <= 0.65 + 0.30 + 0.71 + 0.55
  # o4: 0.68 + 0.40 + 0.65 + 0.60 = 0.62 + 0.40 + 0.56 + 0.50
  # o5: e + 0.60 + 0.93 + 0.00 + 0.73 <= 0.74 + 0.25 + 0.80 + 0.49

  # normalization
  # sum of u_i = 1
  # forall u_i(0) = 0

  # monotonicity
  #

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

  model = LpProblem(name='problem', sense=LpMaximize)
  u1_35 = LpVariable(name='u1_35', lowBound=0, cat='Continuous')
  u3_25 = LpVariable(name='u3_25', lowBound=0, cat='Continuous')

  u1_7 = LpVariable(name='u1_7', lowBound=0, cat='Continuous')
  u2_55 = LpVariable(name='u2_55', lowBound=0, cat='Continuous')
  u3_12 = LpVariable(name='u3_12', lowBound=0, cat='Continuous')

  u1_25 = LpVariable(name='u1_25', lowBound=0, cat='Continuous')
  u2_30 = LpVariable(name='u2_30', lowBound=0, cat='Continuous')

  u1_9 = LpVariable(name='u1_9', lowBound=0, cat='Continuous')
  u2_62 = LpVariable(name='u2_62', lowBound=0, cat='Continuous')
  u3_88 = LpVariable(name='u3_88', lowBound=0, cat='Continuous')

  u1_62 = LpVariable(name='u1_62', lowBound=0, cat='Continuous')
  u3_100 = LpVariable(name='u3_100', lowBound=0, cat='Continuous')

  u1_0 = LpVariable(name='u1_0', lowBound=0, cat='Continuous')
  u2_2 = LpVariable(name='u2_2', lowBound=0, cat='Continuous')
  u3_0 = LpVariable(name='u3_0', lowBound=0, cat='Continuous')

  u1_31 = LpVariable(name='u1_31', lowBound=0, cat='Continuous')
  u2_32 = LpVariable(name='u2_32', lowBound=0, cat='Continuous')
  u3_50 = LpVariable(name='u3_50', lowBound=0, cat='Continuous')

  epsilon = LpVariable(name='epsilon', lowBound=0, cat='Continuous')

  # Ograniczenia problemu
  model += (u1_35 + u2_62 + u3_25 == u1_9 + u2_62 + u3_88, '#1 constraint')
  model += (u1_9 + u2_62 + u3_88 >= u1_25 + u2_30 + u3_12 + epsilon, '#2 constraint')
  model += (u1_25 + u2_30 + u3_12 >= u1_7 + u2_55 + u3_12 + epsilon, '#3 constraint')

  model += u1_62 + u2_62 + u3_100 == 1
  model += u1_0 == 0
  model += u2_2 == 0
  model += u3_0 == 0

  model += u1_31 >= u1_0
  model += u1_62 >= u1_31
  model += u2_32 >= u2_2
  model += u2_62 >= u2_32
  model += u3_100 >= u3_50
  model += u3_50 >= u3_0

  model += u1_0 >= 0
  model += u1_31 >= 0
  model += u1_62 >= 0
  model += u2_2 >= 0
  model += u2_32 >= 0
  model += u2_62 >= 0
  model += u3_0 >= 0
  model += u3_50 >= 0
  model += u3_100 >= 0
  # Funkcja celu
  model += epsilon
  status = model.solve()

  # Wypisanie statusu
  print(f'status: {model.status}, {LpStatus[model.status]}')
  # WYNIK: status: 1, Optimal

  # Wypisanie realizacji funkcji celu
  print(f'objective: {model.objective.value()}')
  # WYNIK: objective : 12.000000199999999

  # Wypisanie wartosci zmiennych decyzyjnych
  u1, u2, u3 = u1_35.value(), u2_62.value(), u3_25.value()
  print(f'Dubov {u1} + {u2} + {u3} = {u1 + u2 + u3}')

  u1, u2, u3 = u1_7.value(), u2_55.value(), u3_12.value()
  print(f'Elmendi {u1} + {u2} + {u3} = {u1 + u2 + u3}')

  u1, u2, u3 = u1_25.value(), u2_30.value(), u3_12.value()
  print(f'Ferrert {u1} + {u2} + {u3} = {u1 + u2 + u3}')

  u1, u2, u3 = u1_9.value(), u2_62.value(), u3_88.value()
  print(f'Grishuk {u1} + {u2} + {u3} = {u1 + u2 + u3}')
