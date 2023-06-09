import matplotlib.pyplot as plt
import numpy as np

def create_concordance_matrix(dataset, preferences, indifferences, weights):
  alternative_count = dataset.shape[0]
  criteria_count = dataset.shape[1]

  concordance = np.zeros((alternative_count, alternative_count))

  for k in range(criteria_count):
    for i in range(alternative_count):
      for j in range(alternative_count):
        if dataset[j, k] - dataset[i, k] >= preferences[k]:
          concordance[i, j] = concordance[i, j] + weights[k] * 0
        elif dataset[j, k] - dataset[i, k] < indifferences[k]:
          concordance[i, j] = concordance[i, j] + weights[k] * 1
        elif indifferences[k] <= dataset[j, k] - dataset[i, k] < preferences[k]:
          concordance[i, j] = (
              concordance[i, j] + weights[k]
              * ((preferences[k] - dataset[j, k] + dataset[i, k]) / (preferences[k] - indifferences[k]))
          )

  return concordance / np.sum(weights)

def create_credibility_matrix(dataset, concordance, preferences, vetoes):
  alternative_count = dataset.shape[0]
  criteria_count = dataset.shape[1]

  credibility = np.copy(concordance)
  for i in range(alternative_count):
    for j in range(alternative_count):
      discordance = 0
      for k in range(0, criteria_count):
        if dataset[j, k] - dataset[i, k] < preferences[k]:
          discordance = 0
        elif dataset[j, k] - dataset[i, k] >= vetoes[k]:
          discordance = 1
        elif preferences[k] <= dataset[j, k] - dataset[i, k] < vetoes[k]:
          discordance = (-preferences[k] - dataset[i, k] + dataset[j, k]) / (vetoes[k] - preferences[k])

        credibility[i, j] *= ((1 - discordance) / (1 - concordance[i, j])) if discordance > concordance[i, j] else 1
        if i == j: credibility[i, j] = 0

  return credibility

def create_qualification(credibility, alpha=0.3, beta=-0.15):
  alternative_count = credibility.shape[0]
  max_ = np.max(credibility)

  s = alpha + beta * max_
  l = credibility[credibility < (max_ - s)]
  l = l.max() if l.shape[0] > 0 else 0

  distance = np.zeros((alternative_count, alternative_count))
  for i in range(0, alternative_count):
    for j in range(0, alternative_count):
      if i == j: continue
      if credibility[i, j] <= l or credibility[i, j] <= credibility[j, i] + s: continue
      distance[i, j] = 1.0

  rows = np.sum(distance, axis=1)
  cols = np.sum(distance, axis=0)
  return rows - cols

def distill(credibility, direction):
  fn = np.amax if direction == 'descending' else np.amin
  alternatives = list(range(credibility.shape[0]))

  rank = []
  while alternatives:
    qualification = create_qualification(credibility)
    if np.where(qualification == fn(qualification))[0].shape[0] > 1:
      index = np.where(qualification == fn(qualification))[0]
      credibility_tie = credibility[index[:, None], index]
      qualification_tie = create_qualification(credibility_tie)

      while (
          1
          < np.where(qualification_tie == fn(qualification_tie))[0].shape[0]
          < np.where(qualification == fn(qualification))[0].shape[0]
      ):
        qualification = create_qualification(credibility_tie)

        index_tie = np.where(qualification == fn(qualification))[0]
        credibility_tie = credibility_tie[index_tie[:, None], index_tie]
        qualification_tie = create_qualification(credibility_tie)

        for i in reversed(range(index.shape[0])):
          if not np.isin(i, index_tie):
            index = np.delete(index, i, axis=0)
      if np.where(qualification_tie == fn(qualification_tie))[0].shape[0] > 1:
        rank.append([alternatives[item] for item in index])

        for i in reversed(range(index.shape[0])):
          del alternatives[index[i]]
      else:
        index_tie = int(np.where(qualification_tie == fn(qualification_tie))[0])
        index = index[index_tie]
        rank.append([alternatives[index]])
        del alternatives[index]
    else:
      index = int(np.where(qualification == fn(qualification))[0])
      rank.append([alternatives[index]])
      del alternatives[index]

    credibility = np.delete(credibility, index, axis=1)
    credibility = np.delete(credibility, index, axis=0)

  return rank if direction == 'descending' else rank[::-1]

def create_final_matrix(descending, ascending, alternative_count):
  alts = list(range(alternative_count))

  desc = [0] * alternative_count
  asc = [0] * alternative_count

  for a in range(alternative_count):
    for b in range(len(descending)):
      if alts[a] not in descending[b]: continue
      desc[a] = b + 1

    for b in range(len(ascending)):
      if alts[a] not in ascending[b]: continue
      asc[a] = b + 1

  preorder = np.full((alternative_count, alternative_count), dtype=str, fill_value=' ')

  for a in range(alternative_count):
    for b in range(a + 1, alternative_count):
      if ((desc[a] < desc[b] and asc[a] < asc[b])
          or (desc[a] == desc[b] and asc[a] < asc[b])
          or (desc[a] < desc[b] and asc[a] == asc[b])):
        preorder[a, b] = '+'
        preorder[b, a] = '-'

      if ((desc[a] > desc[b] and asc[a] > asc[b])
          or (desc[a] == desc[b] and asc[a] > asc[b])
          or (desc[a] > desc[b] and asc[a] == asc[b])):
        preorder[a, b] = '-'
        preorder[b, a] = '+'

      if desc[a] == desc[b] and asc[a] == asc[b]:
        preorder[a, b] = 'I'
        preorder[b, a] = 'I'

      if (desc[a] > desc[b] and asc[a] < asc[b]) or (desc[a] < desc[b] and asc[a] > asc[b]):
        preorder[a, b] = 'R'
        preorder[b, a] = 'R'

  return preorder

def create_final_ranking(names, preorder):
  alts = list(map(lambda x: (x,), range(preorder.shape[0])))

  for i in reversed(range(preorder.shape[0])):
    for j in reversed(range(preorder.shape[1])):
      if preorder[i, j] != 'I': continue

      preorder = np.delete(preorder, i, axis=0)
      preorder = np.delete(preorder, i, axis=1)
      alts[j] = (*alts[j], *alts[i])
      del alts[i]
      break

  preorder_matrix = np.zeros((preorder.shape[0], preorder.shape[1]))
  for i in range(preorder.shape[0]):
    for j in range(preorder.shape[1]):
      if preorder[i, j] != '+': continue
      preorder_matrix[i, j] = 1

  col_sum = np.sum(preorder_matrix, axis=1)
  alts_rank = [x for _, x in sorted(zip(col_sum, alts))]
  if np.sum(col_sum) != 0: alts_rank.reverse()

  graph = {value: key for (key, value) in enumerate(alts)}
  ranks = {value: key for (key, value) in enumerate(alts_rank)}

  rank = np.copy(preorder_matrix)
  for i in range(preorder_matrix.shape[0]):
    for j in range(preorder_matrix.shape[1]):
      if (preorder_matrix[i, j] == 1):
        rank[i, :] = np.clip(rank[i, :] - rank[j, :], 0, 1)
  rank_xy = np.zeros((len(alts_rank), 2))

  for i in range(rank_xy.shape[0]):
    rank_xy[i, 0] = 0
    if (len(alts_rank) - np.sum(~rank.any(1)) != 0):
      rank_xy[i, 1] = len(alts_rank) - np.sum(~rank.any(1))
    else:
      rank_xy[i, 1] = 1

  for i in range(len(alts_rank) - 1):
    i1 = int(graph[alts_rank[i][:2]])
    i2 = int(graph[alts_rank[i + 1][:2]])
    if (preorder[i1, i2] == '+'):
      rank_xy[i + 1, 1] = rank_xy[i + 1, 1] - 1
      for j in range(i + 2, rank_xy.shape[0]):
        rank_xy[j, 1] = rank_xy[i + 1, 1]
    if (preorder[i1, i2] == 'R'):
      rank_xy[i + 1, 0] = rank_xy[i, 0] + 1

  for i in range(rank_xy.shape[0]):
    plt.text(
      rank_xy[i, 0],
      rank_xy[i, 1],
      f"({i}) {', '.join([names[x] for x in alts_rank[i]])}",
      size=12,
      ha='center',
      va='center',
      bbox=dict(boxstyle='round', facecolor='cyan', edgecolor='black')
    )

  keys, values = zip(*graph.items())
  for i in range(rank.shape[0]):
    for j in range(rank.shape[1]):
      if rank[i, j] != 1: continue
      k1 = ranks[keys[values.index(i)]]
      k2 = ranks[keys[values.index(j)]]

      plt.arrow(
        rank_xy[k1, 0],
        rank_xy[k1, 1],
        rank_xy[k2, 0] - rank_xy[k1, 0],
        rank_xy[k2, 1] - rank_xy[k1, 1],
        head_width=0.15,
        head_length=0.4,
        overhang=0.0,
        color='gray',
        linewidth=0.9,
        length_includes_head=True
      )

  plt.gcf().set_size_inches(12, 16)
  plt.axis('off')
  plt.show()
  return ranks

def create_median_ranking(ranks, descending, ascending):
  ...

def perform(dataset, preferences, indifferences, vetoes, weights):
  names = dataset.index
  dataset = dataset.values
  concordance = create_concordance_matrix(dataset, preferences, indifferences, weights)
  credibility = create_credibility_matrix(dataset, concordance, preferences, vetoes)

  alternative_count = dataset.shape[0]
  rank_descending = distill(credibility, direction='descending')
  rank_ascending = distill(credibility, direction='ascending')
  ranking = create_final_matrix(rank_descending, rank_ascending, alternative_count)

  rank_final = create_final_ranking(names, ranking)
  # TODO
  rank_median = create_median_ranking(rank_final, rank_descending, rank_ascending)

  return ranking, rank_final  # , rank_median

if __name__ == '__main__':
  from pandas import read_csv
  dataset = read_csv('./resources/datasets/ai-index.csv', index_col="Country")
  criteria = [
    'Talent',
    'Infrastructure',
    'Operating Environment',
    'Research',
    'Development',
    'Government Strategy',
    'Commercial',
  ]
  criteria_count = len(criteria)
  preferences = [10] * criteria_count
  indifferences = [2.5] * criteria_count
  vetoes = [40] * criteria_count
  weights = [5.0, 2.0, 1.0, 5.0, 5.0, 1.0, 7.0, ]

  df = dataset[criteria]
  alternatives = df

  rank_final, rank_median = perform(
    alternatives,
    preferences,
    indifferences,
    vetoes,
    weights
  )

  print(rank_final)
  print(rank_median)
