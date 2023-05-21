from dataclasses import dataclass

from torch import nn
from torch.nn import Sequential
from ..dataset import LoanDataset

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

    return cls(model)
