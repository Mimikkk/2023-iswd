from mod.dataset import LoanDataset
from mod.models import ModelManager

def main():
  ds = LoanDataset.load()
  log = ModelManager.use_logistic(ds, invalidate=True)
  ann = ModelManager.use_ann(ds, invalidate=True)
  dnn = ModelManager.use_dnn(ds, invalidate=True)

if __name__ == '__main__':
  main()
