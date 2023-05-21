import pickle
from typing import ClassVar

import torch

from .logistic_model import LogisticModel
from .ann_model import AnnModel
from .dnn_model import DnnModel
from os.path import exists
from os import makedirs
from ..dataset import LoanDataset

class ModelManager(object):
  _logistic_path: ClassVar[str] = './resources/models/logistic.model'
  _ann_path: ClassVar[str] = './resources/models/ann.model'
  _dnn_path: ClassVar[str] = './resources/models/dnn.model'

  @classmethod
  def use_logistic(cls, dataset: LoanDataset, *, invalidate: bool = False):
    if not invalidate and exists(cls._logistic_path): return cls.load_logistic()
    model = LogisticModel.create(dataset)
    cls.save_logistic(model)
    return model

  @classmethod
  def load_logistic(cls) -> LogisticModel:
    return pickle.load(open(cls._logistic_path, 'rb'))

  @classmethod
  def save_logistic(cls, model: LogisticModel):
    if not exists(cls._logistic_path): makedirs('./resources/models', exist_ok=True)
    pickle.dump(model, open(cls._logistic_path, 'wb'))

  @classmethod
  def use_ann(cls, dataset: LoanDataset, *, invalidate: bool = False):
    if not invalidate and exists(cls._ann_path): return cls.load_ann()
    AnnModel.create(dataset, cls._ann_path)
    return cls.load_ann()

  @classmethod
  def load_ann(cls) -> AnnModel:
    return torch.load(cls._ann_path)

  @classmethod
  def use_dnn(cls, dataset: LoanDataset, *, invalidate: bool = False):
    if not invalidate and exists(cls._dnn_path): return cls.load_dnn()
    DnnModel.create(dataset, cls._dnn_path)
    return cls.load_dnn()

  @classmethod
  def load_dnn(cls) -> DnnModel:
    return torch.load(cls._dnn_path)
