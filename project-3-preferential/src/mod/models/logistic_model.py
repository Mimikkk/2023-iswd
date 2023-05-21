from dataclasses import dataclass
from typing import ClassVar

from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder

from ..dataset import LoanDataset

@dataclass
class LogisticModel(object):
  regressor: LogisticRegression
  validator: GridSearchCV
  _path: ClassVar[str] = './resources/models/logistic_model.pkl'
  _encoder: ClassVar[OneHotEncoder] = OneHotEncoder()

  @classmethod
  def create(cls, dataset: LoanDataset) -> 'LogisticModel':
    regressor = LogisticRegression()
    (X, y) = dataset.preprocess(variant='labeled')
    cls._encoder.fit_transform(X)

    validator = GridSearchCV(regressor, {}, scoring={
      'accuracy': 'accuracy',
      'f1': 'f1',
      'roc_auc': 'roc_auc'
    }, refit='accuracy', cv=10, n_jobs=-1, verbose=1)

    validator.fit(X, y)

    return cls(regressor, validator)
