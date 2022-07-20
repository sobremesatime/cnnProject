import torchvision.datasets
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

dataset_transform = torchvision.transforms.Compose([
    torchvision.transforms.ToTensor()
])
#加载数据集到dataset文件夹
train_set = torchvision.datasets.MNIST(root="./dataset", train=True, download=True, transform=dataset_transform)
train_loader = DataLoader(dataset=train_set, batch_size=32, shuffle=True, num_workers=0)
test_set = torchvision.datasets.MNIST(root="./dataset", train=False, download=True, transform=dataset_transform)
test_loader = DataLoader(dataset=test_set, batch_size=32, shuffle=True, num_workers=0)

#用tensorboard进行测试
# writer = SummaryWriter("datalogs")
# # for i in range(10):
# #     img, target = test_set[i]
# #     writer.add_image("test_set", img, i)
# #
# # writer.close()

