import pickle
from typing import ClassVar
from .logistic_model import LogisticModel
from .ann_model import AnnModel
from .cnn_model import CnnModel
from os.path import exists
from os import makedirs
from ..dataset import LoanDataset

class ModelManager(object):
  _logistic_path: ClassVar[str] = './resources/models/logistic_model.pkl'
  _ann_path: ClassVar[str] = './resources/models/ann_model.pkl'
  _cnn_path: ClassVar[str] = './resources/models/cnn_model.pkl'

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
  def use_ann(cls, dataset: LoanDataset, *, invalidate: bool = False) -> AnnModel:
    if not invalidate and exists(cls._logistic_path): return cls.load_ann()
    model = AnnModel.create(dataset)
    cls.save_ann(model)
    return model

  @classmethod
  def load_ann(cls) -> AnnModel:
    raise NotImplementedError

  @classmethod
  def save_ann(cls, model: AnnModel):
    raise NotImplementedError

  @classmethod
  def use_cnn(cls, dataset: LoanDataset, *, invalidate: bool = False):
    # if not invalidate and exists(cls._logistic_path): return cls.load_cnn()
    model = CnnModel.create(dataset)
    # cls.save_cnn(model)
    return model

  @classmethod
  def load_cnn(cls) -> CnnModel:
    raise NotImplementedError

  @classmethod
  def save_cnn(cls, model: CnnModel):
    raise NotImplementedError
