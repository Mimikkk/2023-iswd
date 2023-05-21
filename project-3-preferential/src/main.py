from mod.dataset import LoanDataset
from mod.models import ModelManager

def main():
  ds = LoanDataset.load()
  manager = ModelManager.use_logistic(ds)

if __name__ == '__main__':
  main()
