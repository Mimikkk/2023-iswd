from sklearn.model_selection import train_test_split
import torch
from torch.utils.data import Dataset
from tqdm import tqdm

from mod.dataset import LoanDataset
from mod.models import ModelManager
from mod.helpers import *

def main():
  ds = LoanDataset.load()
  cnn = ModelManager.use_cnn(ds, invalidate=True)
  (X, y) = ds.preprocess(type='labeled')

  (X_train, X_test, y_train, y_test) = train_test_split(X, y, test_size=0.2, random_state=42)

  train_dataloader = create_data_loader(X_train, y_train, batchsize=32)
  test_dataloader = create_data_loader(X_test, y_test, batchsize=32)

  path = './resources/models/cnn_model.chkpt'
  model = cnn.model
  best_acc, acc_test, best_auc, auc_test = train_model(model, train_dataloader, test_dataloader, path, lr=1e-5, epoch_nr=500)

  print(f"Best accuracy: {best_acc}")
  print(f"Test accuracy: {acc_test}")
  print(f"Best AUC: {best_auc}")
  print(f"Test AUC: {auc_test}")

if __name__ == '__main__':
  main()
