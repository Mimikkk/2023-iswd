from dataclasses import dataclass

from sklearn.model_selection import train_test_split
from torch import nn
from torch.nn import Sequential
from ..dataset import LoanDataset
from ..helpers import *

@dataclass
class DnnModel(object):
  model: Sequential

  @classmethod
  def create(cls, dataset: LoanDataset) -> 'DnnModel':
    model = Sequential(
      nn.Linear(len(dataset.unlabeled.columns) - 1, 256),
      nn.LeakyReLU(),
      nn.Linear(256, 128),
      nn.LeakyReLU(),
      nn.Linear(128, 64),
      nn.LeakyReLU(),
      nn.Linear(64, 32),
      nn.LeakyReLU(),
      nn.Linear(32, 1),
      nn.Sigmoid()
    )

    model_path = "dnn.pt"
    (X, y, _) = dataset.preprocess(variant="labeled")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=10)
    best_acc, acc_test, best_auc, auc_test = train_model(
      model,
      create_data_loader(X_train, y_train, batchsize=32),
      create_data_loader(X_test, y_test, batchsize=32),
      model_path,
      lr=0.001,
      epoch_nr=500
    )

    print(f"Accuracy train:\t{best_acc * 100:.2f}%")
    print(f"AUC train: \t{best_auc * 100:.2f}%")
    print()
    print(f"Accuracy test:\t{acc_test * 100:.2f}%")
    print(f"AUC test: \t{auc_test * 100:.2f}%")

    return cls(model)
