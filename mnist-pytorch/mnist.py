import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from clearml import Dataset
from torchvision import datasets, transforms


class MNISTNet(nn.Module):
    def __init__(self):
        super(MNISTNet, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        output = F.log_softmax(x, dim=1)
        return output


def get_data_loaders(batch_size):
    transform = transforms.Compose([
        transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))
    ])

    dataset_path = Dataset.get(
        dataset_name='mnist_dataset', dataset_project='data_management'
    ).get_local_copy()

    trainset = datasets.MNIST(
        root=dataset_path, train=True, download=False, transform=transform
    )
    train_loader = torch.utils.data.DataLoader(
        trainset, batch_size=batch_size, shuffle=True, num_workers=10
    )

    testset = datasets.MNIST(
        root=dataset_path, train=False, download=False, transform=transform
    )
    test_loader = torch.utils.data.DataLoader(
        testset, batch_size=batch_size, shuffle=True, num_workers=10
    )
    return train_loader, test_loader


def train(model, device, train_loader, optimizer, epoch, log):
    model.train()
    for batch_idx, (X, y) in enumerate(train_loader):
        X, y = X.to(device), y.to(device)
        optimizer.zero_grad()
        output = model(X)
        loss = F.nll_loss(output, y)
        loss.backward()
        optimizer.step()
        if batch_idx % log == 0:
            # Logger.current_logger().report_scalar(
            #     "train", "loss", iteration=(epoch * len(train_loader) + batch_idx), value=loss.item()
            # )
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(epoch, batch_idx * len(X),
                                                                           len(train_loader.dataset),
                                                                           100. * batch_idx / len(train_loader),
                                                                           loss.item()))


def test(model, device, test_loader, epoch):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for X, y in test_loader:
            X, y = X.to(device), y.to(device)
            output = model(X)
            test_loss += F.nll_loss(output, y, reduction='sum').item()
            pred = output.argmax(dim=1, keepdim=True)
            correct += pred.eq(y.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)
    # Logger.current_logger().report_scalar(
    #     "test", "loss", iteration=epoch, value=test_loss)
    # Logger.current_logger().report_scalar(
    #     "test", "accuracy", iteration=epoch, value=(correct / len(test_loader.dataset)))
    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))


def setup_clearml():
    # init task
    params = {
        "epochs": 10,
        "batch_size": 64,
        "base_lr": 0.01,
        "momentum": 0.5,
        "log_interval": 10,
    }
    print(params)
    return None, params


def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    _, params = setup_clearml()

    train_loader, test_loader = get_data_loaders(params.get('batch_size'))
    print(f'Loaded {len(train_loader)} train samples and {len(test_loader)} test samples.')

    model = MNISTNet().to(device)
    optimizer = optim.SGD(model.parameters(),
                          lr=params.get('base_lr'),
                          momentum=params.get('momentum'))

    for epoch in range(1, params.get('epochs') + 1):
        train(model, device, train_loader, optimizer, epoch, params.get('log_interval'))
        test(model, device, test_loader, epoch)


if __name__ == '__main__':
    main()
