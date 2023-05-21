from numpy.typing import NDArray
from typing import ClassVar
from sklearn.preprocessing import OneHotEncoder
from dataclasses import dataclass
import pandas as pd

from pandas import DataFrame

@dataclass
class LoanDataset(object):
  train: DataFrame
  test: DataFrame
  _encoder: ClassVar[OneHotEncoder] = OneHotEncoder(handle_unknown='ignore')

  @classmethod
  def load(cls):
    return cls(
      pd.read_csv(f"./resources/datasets/loan_sanction_train.csv"),
      pd.read_csv(f"./resources/datasets/loan_sanction_test.csv")
    )

  def preprocess(self, split: str = 'train') -> tuple[NDArray, NDArray | None]:
    if split == 'train':
      df = self.train.copy()
      df.dropna(inplace=True)
      df.drop(columns=["Loan_ID"], inplace=True)

      X = df.drop(columns=["Loan_Status"])
      y = df["Loan_Status"]

      X = self._encoder.fit_transform(X).toarray()
      y = y.map({"N": 0, "Y": 1}).to_numpy()

      return X, y
    df = self.test.copy()
    df.dropna(inplace=True)

    df.drop(columns=["Loan_ID"], inplace=True)
    X = self._encoder.fit_transform(df).toarray()

    return X
