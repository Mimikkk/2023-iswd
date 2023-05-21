from numpy._typing import NDArray
import torch
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm
from sklearn.metrics import roc_auc_score

class ArrayDataset(Dataset):
  def __init__(self, data, targets):
    self.data = torch.Tensor(data)
    self.targets = torch.LongTensor(targets.astype(int))

  def __getitem__(self, index):
    x = self.data[index]
    y = self.targets[index]
    return x, y

  def __len__(self):
    return len(self.data)


def calculate_loss(x, target):
  return torch.mean(
    torch.relu(-(target >= 1).float() * x) + torch.relu((target < 1).float() * x)
  )

def calculate_accuracy(x, target):
  return (target == (x[:, 0] > 0) * 1).detach().numpy().mean()

def calculate_auc(x, target):
  return roc_auc_score(target.detach().numpy(), x.detach().numpy()[:, 0])

def create_data_loader(X: NDArray, y: NDArray, *, batchsize=None) -> DataLoader:
  dataset = ArrayDataset(X, y)
  batchsize = batchsize if batchsize is not None else len(dataset)
  return DataLoader(dataset, batch_size=batchsize)

def train_model(model, train_dataloader, test_dataloader, checkpoint_path, lr=0.01, epoch_nr=200):
  optimizer = optim.AdamW(model.parameters(), lr=lr, betas=(0.9, 0.99))

  best_acc = 0.0
  best_auc = 0.0
  for epoch in tqdm(range(epoch_nr)):
    for _, data in enumerate(train_dataloader, 0):
      X, y_true = data
      optimizer.zero_grad()
      y_pred = model(X)

      loss_train = calculate_loss(y_pred, y_true)
      loss_train.backward()
      optimizer.step()
      acc_train = calculate_accuracy(y_pred, y_true)
      auc_train = calculate_auc(y_pred, y_true)

    if acc_train > best_acc:
      best_acc = acc_train
      best_auc = auc_train

      with torch.no_grad():
        for i, data in enumerate(test_dataloader, 0):
          X, y_true = data
          y_pred = model(X)
          loss_test = calculate_loss(y_pred, y_true)
          acc_test = calculate_accuracy(y_pred, y_true)
          auc_test = calculate_auc(y_pred, y_true)

      torch.save({
        "epoch": epoch,
        "model": {
          "state": model.state_dict(),
        },
        "optimizer": {
          "state": optimizer.state_dict(),
        },
        "train": {
          "accuracy": acc_train,
          "auc": auc_train,
          "loss": loss_train,
        },
        "test": {
          "accuracy": acc_test,
          "auc": auc_test,
          "loss": loss_test,
        },
      }, checkpoint_path)

  return best_acc, acc_test, best_auc, auc_test
