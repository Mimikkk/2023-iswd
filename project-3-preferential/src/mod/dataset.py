from numpy.typing import NDArray
from typing import ClassVar, TypeAlias, Literal
from sklearn.preprocessing import OneHotEncoder
from dataclasses import dataclass
import pandas as pd

from pandas import DataFrame

SplitType: TypeAlias = Literal['labeled', 'unlabeled']

@dataclass
class LoanDataset(object):
  labeled: DataFrame
  unlabeled: DataFrame
  _encoder: ClassVar[OneHotEncoder] = OneHotEncoder(handle_unknown='ignore')

  @classmethod
  def load(cls):
    return cls(
      pd.read_csv(f"./resources/datasets/loan_sanction_labeled.csv"),
      pd.read_csv(f"./resources/datasets/loan_sanction_unlabeled.csv")
    )

  def preprocess(self, *, type: SplitType = 'labeled') -> tuple[NDArray, NDArray | None]:
    if type == 'labeled':
      df = self.labeled.copy()
      df.dropna(inplace=True)
      df.drop(columns=["Loan_ID"], inplace=True)

      X = df.drop(columns=["Loan_Status"])
      y = df["Loan_Status"]

      X = self._encoder.fit_transform(X).toarray()
      y = y.map({"N": 0, "Y": 1}).to_numpy()

      return X, y
    df = self.unlabeled.copy()
    df.dropna(inplace=True)

    df.drop(columns=["Loan_ID"], inplace=True)
    X = self._encoder.fit_transform(df).toarray()

    return X
