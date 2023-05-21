import torch

from mod.dataset import LoanDataset
from mod.models import ModelManager

def main():
  ds = LoanDataset.load()
  logistic = ModelManager.use_logistic(ds, invalidate=True)
  print(logistic.validator.best_score_)


if __name__ == '__main__':
  main()
