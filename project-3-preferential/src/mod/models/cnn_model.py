from dataclasses import dataclass

from torch import nn
from torch.nn import Sequential
from ..dataset import LoanDataset

@dataclass
class CnnModel(object):
  model: Sequential

  @classmethod
  def create(cls, dataset: LoanDataset) -> 'CnnModel':
    # The input is one long array of random amount of features, and the output is a single value in range of (0 to 1)
    model = Sequential(
      nn.Linear(849, 512),
      nn.LeakyReLU(),
      nn.Dropout(0.2),
      nn.BatchNorm1d(512),
      nn.Linear(512, 256),
      nn.LeakyReLU(),
      nn.Dropout(0.2),
      nn.Linear(256, 128),
      nn.LeakyReLU(),
      nn.Linear(128, 64),
      nn.LeakyReLU(),
      nn.Linear(64, 32),
      nn.LeakyReLU(),
      nn.Linear(32, 1),
      nn.Sigmoid()
    )

    return cls(model)
