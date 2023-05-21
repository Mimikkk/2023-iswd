from dataclasses import dataclass

from sklearn.model_selection import train_test_split

from ..dataset import LoanDataset
from ..helpers import *

import torch
from torch import nn
import torch.nn.functional as F

class LinearGreaterThanZero(nn.Linear):
  def __init__(self, in_features, bias=False, min_w=0.0000001):
    super().__init__(in_features, 1, bias)
    self.is_bias = bias
    self.min_w = min_w
    if bias:
      nn.init.uniform_(self.bias, self.min_w, 1.0)
    else:
      self.bias = None

  def reset_parameters(self):
    nn.init.uniform_(self.weight, 0.1, 1.0)

  def w(self):
    with torch.no_grad():
      self.weight.data[self.weight.data < 0] = self.min_w
    return self.weight

  def forward(self, input):
    return F.linear(input, self.w(), self.bias)

class LinearInteraction(nn.Linear):
  def __init__(self, in_features, criterion_layer):
    super().__init__(((in_features - 1) * in_features) // 2, 1, False)
    self.in_features = in_features
    self.criterion_layer = criterion_layer

  def reset_parameters(self):
    nn.init.normal_(self.weight, 0.0, 0.1)

  def w(self):
    with torch.no_grad():
      w_i = 0
      w = self.criterion_layer.w()
      for i in range(self.in_features):
        for j in range(i + 1, self.in_features):
          self.weight.data[:, w_i] = torch.max(
            self.weight.data[:, w_i], -w[:, i]
          )
          self.weight.data[:, w_i] = torch.max(
            self.weight.data[:, w_i], -w[:, j]
          )
          w_i += 1
    return self.weight

  def forward(self, input):
    return F.linear(input, self.w(), None)

class ThresholdLayer(nn.Module):
  def __init__(self, threshold=None, requires_grad=True):
    super().__init__()
    if threshold is None:
      self.threshold = nn.Parameter(
        torch.FloatTensor(1).uniform_(0.1, 0.5), requires_grad=requires_grad
      )
    else:
      self.threshold = nn.Parameter(
        torch.FloatTensor([threshold]), requires_grad=requires_grad
      )

  def forward(self, x):
    return x - self.threshold

class ChoquetConstrained(nn.Module):
  def __init__(self, criteria_nr):
    super().__init__()
    self.criteria_nr = criteria_nr
    self.criteria_layer = LinearGreaterThanZero(criteria_nr)
    self.interaction_layer = LinearInteraction(criteria_nr, self.criteria_layer)
    self.thresholdLayer = ThresholdLayer()

  def forward(self, x):
    if len(x.shape) == 3:
      x = x[:, 0, :]
    x_wi = self.criteria_layer(x[:, : self.criteria_nr])
    x_wij = self.interaction_layer(x[:, self.criteria_nr:])
    weight_sum = self.criteria_layer.w().sum() + self.interaction_layer.w().sum()

    score = (x_wi + x_wij) / (weight_sum)
    return self.thresholdLayer(score)

def mobious_transform(row):
  return list(row) + [
    min(row[i], row[j]) for i in range(len(row)) for j in range(i + 1, len(row))
  ]

@dataclass
class AnnModel(object):
  model: ChoquetConstrained

  @classmethod
  def create(cls, dataset: LoanDataset) -> 'AnnModel':
    df = dataset.labeled.copy()

    df.drop([
      "Loan_ID",
      "Gender",
      "Married",
      "Dependents",
      "Education",
      "Self_Employed",
      "Credit_History",
      "Property_Area",
    ], axis=1, inplace=True)
    df.dropna(inplace=True)
    target_map = {"N": 0, "Y": 1}

    criteria_nr = 4
    data_input = df.iloc[:, :criteria_nr].apply(
      lambda x: mobious_transform(x), axis=1, result_type="expand"
    )
    data_target = df["Loan_Status"].map(target_map)

    X_train, X_test, y_train, y_test = train_test_split(
      data_input.values, data_target.values, test_size=0.1, random_state=10
    )
    train_dataloader = create_data_loader(X_train, y_train, batchsize=32)
    test_dataloader = create_data_loader(X_test, y_test, batchsize=32)
    PATH = "choquet.pt"
    model = ChoquetConstrained(criteria_nr)
    acc, acc_test, auc, auc_test = train_model(model, train_dataloader, test_dataloader, PATH, lr=0.001, epoch_nr=500)

    print("Accuracy train:\t%.2f%%" % (acc * 100.0))
    print("AUC train: \t%.2f%%" % (acc_test * 100.0))
    print()
    print("Accuracy test:\t%.2f%%" % (auc * 100.0))
    print("AUC test: \t%.2f%%" % (auc_test * 100.0))

    return cls(model)
