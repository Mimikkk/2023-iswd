from dataclasses import dataclass

from sklearn.model_selection import train_test_split

from ..dataset import LoanDataset
from ..utils import *
from .ann_layers import ChoquetConstrained

def transform_mobius(row):
  row = list(row)
  row.extend([
    min(row[i], row[j]) for i in range(len(row)) for j in range(i + 1, len(row))
  ])
  return row

@dataclass
class AnnModel(object):
  model: ChoquetConstrained

  @classmethod
  def create(cls, dataset: LoanDataset, model_path: str) -> 'AnnModel':
    _, _, df = dataset.preprocess(variant='labeled')
    df.drop([
      "Gender",
      "Married",
      "Dependents",
      "Education",
      "Self_Employed",
      "Credit_History",
      "Property_Area",
    ], axis=1, inplace=True)

    X = df.iloc[:, :4].apply(transform_mobius, axis=1, result_type="expand")
    y = df["Loan_Status"]

    X_train, X_test, y_train, y_test = train_test_split(
      X.values, y.values, test_size=0.1, random_state=10
    )

    model = cls.empty().model
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

  @classmethod
  def empty(cls):
    return cls(ChoquetConstrained(4))
