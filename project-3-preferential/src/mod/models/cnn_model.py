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
    df = dataset.labeled.copy()
    df.drop(["Loan_ID"], axis=1, inplace=True)
    df.dropna(inplace=True)
    target_map = {"N": 0, "Y": 1}
    df["Gender"] = df["Gender"].map({
      "Male": 1,
      "Female": 0,
    })
    df["Married"] = df["Married"].map({
      "Yes": 1,
      "No": 0,
    })
    df["Dependents"] = df["Dependents"].map({
      "0": 0,
      "1": 1,
      "2": 2,
      "3+": 3,
    })
    df["Education"] = df["Education"].map({
      "Graduate": 1,
      "Not Graduate": 0,
    })
    df["Self_Employed"] = df["Self_Employed"].map({
      "Yes": 1,
      "No": 0,
    })
    df["Credit_History"] = df["Credit_History"].map({
      1.0: 1,
      0.0: 0,
    })
    df["Property_Area"] = df["Property_Area"].map({
      "Urban": 2,
      "Semiurban": 1,
      "Rural": 0,
    })
    df["Loan_Status"] = df["Loan_Status"].map(target_map)

    X = df.drop(["Loan_Status"], axis=1)
    y = df["Loan_Status"]

    X_train, X_test, y_train, y_test = train_test_split(
      X.values, y.values, test_size=0.1, random_state=10
    )
    train_dataloader = create_data_loader(X_train, y_train, batchsize=32)
    test_dataloader = create_data_loader(X_test, y_test, batchsize=32)
    PATH = "choquet.pt"

    model = Sequential(
      nn.Linear(len(df.columns) - 1, 256),
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
    acc, acc_test, auc, auc_test = train_model(model, train_dataloader, test_dataloader, PATH, lr=0.001, epoch_nr=500)

    print("Accuracy train:\t%.2f%%" % (acc * 100.0))
    print("AUC train: \t%.2f%%" % (acc_test * 100.0))
    print()
    print("Accuracy test:\t%.2f%%" % (auc * 100.0))
    print("AUC test: \t%.2f%%" % (auc_test * 100.0))


    return cls(model)
