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
      nn.Conv2d(1, 20, 5, 1),
      nn.ReLU(),
      nn.Conv2d(20, 64, 5, 1),
      nn.ReLU(),
      nn.MaxPool2d(2, 2),
      nn.Dropout2d(),
      nn.Flatten(),
      nn.Linear(64 * 4 * 4, 128),
      nn.ReLU(),
      nn.Linear(128, 10),
      nn.Softmax(dim=1)
    )

    return cls(model)
