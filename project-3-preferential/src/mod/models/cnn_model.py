from dataclasses import dataclass

from sklearn.model_selection import train_test_split
from torch import nn
from torch.nn import Sequential
from ..dataset import LoanDataset
from ..helpers import *

@dataclass
class CnnModel(object):
  model: Sequential

  @classmethod
  def create(cls, dataset: LoanDataset) -> 'CnnModel':
    model = Sequential(
      nn.Linear(849, 256),
      nn.ReLU(),
      nn.Dropout(0.3),
      nn.Linear(256, 128),
      nn.ReLU(),
      nn.Dropout(0.2),
      nn.Linear(128, 64),
      nn.ReLU(),
      nn.Linear(64, 32),
      nn.ReLU(),
      nn.Linear(32, 1),
      nn.Sigmoid()
    )

    (X, y) = ds.preprocess(type='labeled')

    (X_train, X_test, y_train, y_test) = train_test_split(X, y, test_size=0.1, random_state=10)

    train_dataloader = create_data_loader(X_train, y_train, batchsize=32)
    test_dataloader = create_data_loader(X_test, y_test, batchsize=32)

    path = './resources/models/cnn_model.chkpt'
    best_acc, acc_test, best_auc, auc_test = train_model(
      model,
      train_dataloader,
      test_dataloader,
      path,
      lr=0.001,
      epoch_nr=1000
    )

    print(f"Best accuracy: {best_acc}")
    print(f"Test accuracy: {acc_test}")
    print(f"Best AUC: {best_auc}")
    print(f"Test AUC: {auc_test}")

    return cls(model)
