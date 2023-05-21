from numpy._typing import NDArray
import torch
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm
from sklearn.metrics import roc_auc_score

class NumpyDataset(Dataset):
  def __init__(self, data, targets):
    self.data = torch.Tensor(data)
    self.targets = torch.LongTensor(targets.astype(int))

  def __getitem__(self, index):
    x = self.data[index]
    y = self.targets[index]
    return x, y

  def __len__(self):
    return len(self.data)


def calculate_regret(x, target):
  return torch.mean(
    torch.relu(-(target >= 1).float() * x) + torch.relu((target < 1).float() * x)
  )

def calculate_accuracy(x, target):
  return (target == (x[:, 0] > 0) * 1).detach().numpy().mean()

def calculate_auc(x, target):
  return roc_auc_score(target.detach().numpy(), x.detach().numpy()[:, 0])

def create_data_loader(X: NDArray, y: NDArray, *, batchsize=None) -> DataLoader:
  dataset = NumpyDataset(X, y)
  batchsize = batchsize if batchsize is not None else len(dataset)
  return DataLoader(dataset, batch_size=batchsize)

def train_model(model, train_dataloader, test_dataloader, path, lr=0.01, epoch_nr=200):
  optimizer = optim.AdamW(model.parameters(), lr=lr, betas=(0.9, 0.99))
  best_acc = 0.0
  best_auc = 0.0
  for epoch in tqdm(range(epoch_nr)):
    for _, data in enumerate(train_dataloader, 0):
      inputs, labels = data
      optimizer.zero_grad()
      outputs = model(inputs)
      loss = calculate_regret(outputs, labels)
      loss.backward()
      optimizer.step()
      acc = calculate_accuracy(outputs, labels)
      auc = calculate_auc(outputs, labels)

    if acc > best_acc:
      best_acc = acc
      best_auc = auc
      with torch.no_grad():
        for i, data in enumerate(test_dataloader, 0):
          inputs, labels = data
          outputs = model(inputs)
          loss_test = calculate_regret(outputs, labels)
          acc_test = calculate_accuracy(outputs, labels)
          auc_test = calculate_auc(outputs, labels)

      torch.save(
        {
          "epoch": epoch,
          "model_state_dict": model.state_dict(),
          "optimizer_state_dict": optimizer.state_dict(),
          "loss_train": loss,
          "loss_test": loss_test,
          "accuracy_train": acc,
          "accuracy_test": acc_test,
          "auc_train": auc,
          "auc_test": auc_test,
        },
        path,
      )

  return best_acc, acc_test, best_auc, auc_test
