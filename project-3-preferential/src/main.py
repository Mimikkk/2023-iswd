from sklearn.model_selection import train_test_split
from mod.dataset import LoanDataset
from mod.models import ModelManager
from mod.helpers import *

def main():
  ds = LoanDataset.load()
  ann = ModelManager.use_ann(ds, invalidate=True)
  # dnn = ModelManager.use_dnn(ds, invalidate=True)

if __name__ == '__main__':
  main()
