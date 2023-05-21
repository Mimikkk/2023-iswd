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

  @classmethod
  def load(cls):
    return cls(
      pd.read_csv(f"./resources/datasets/loan_sanction_labeled.csv"),
      pd.read_csv(f"./resources/datasets/loan_sanction_unlabeled.csv")
    )

  def preprocess(self, *, variant: SplitType = 'labeled') -> tuple[NDArray, NDArray | None, DataFrame]:
    df = self.labeled.copy() if variant == 'labeled' else self.unlabeled.copy()
    df.dropna(inplace=True)

    df.drop(columns=["Loan_ID"], inplace=True)
    df["Gender"] = df["Gender"].map({"Male": 1, "Female": 0})
    df["Married"] = df["Married"].map({"Yes": 1, "No": 0})
    df["Dependents"] = df["Dependents"].map({"0": 0, "1": 1, "2": 2, "3+": 3})
    df["Education"] = df["Education"].map({"Graduate": 1, "Not Graduate": 0})
    df["Self_Employed"] = df["Self_Employed"].map({"Yes": 1, "No": 0})
    df["Property_Area"] = df["Property_Area"].map({"Urban": 2, "Semiurban": 1, "Rural": 0})

    if variant == 'labeled':
      df["Loan_Status"] = df["Loan_Status"].map({"N": 0, "Y": 1})
      return df.drop(columns=["Loan_Status"]).to_numpy(), df["Loan_Status"].to_numpy(), df

    return df.to_numpy(), None, df
