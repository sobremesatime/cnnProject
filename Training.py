import torch

from CnnModel import *
from DataLoader import *

#length长度
train_size = len(train_set)
test_size = len(test_set)
print("训练集的长度：{}".format(train_size))
print("测试集的长度：{}".format(test_size))

#定义训练设备
device = torch.device("cuda")


#创建网络模型
lenet_5 = LeNet_5()
lenet_5.to(device)


#损失函数
loss_fn = nn.CrossEntropyLoss()
loss_fn.to(device)

#优化器
learning_rate = 0.001
optimizer = torch.optim.Adam(lenet_5.parameters(), lr=learning_rate)

#设置训练网络的一些参数
#记录训练次数，测试次数，训练轮数
total_train_step = 0
total_test_step = 0
epoch = 50

#添加tensorboard
writer = SummaryWriter("logs")

for i in range(epoch):
    print("----------------第{}轮训练开始--------------".format(i+1))

    #训练步骤
    lenet_5.train()
    for data in train_loader:
        imgs, targets = data
        imgs = imgs.to(device)
        targets = targets.to(device)
        output = lenet_5(imgs)
        loss = loss_fn(output, targets)

        #优化器优化模型
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_train_step = total_train_step + 1
        if total_train_step % 100 == 0:
            print("训练次数： {}，Loss：{}".format(total_train_step, loss.item()))
            writer.add_scalar("train_loss", loss.item(), total_train_step)

    #测试步骤
    lenet_5.eval()
    total_test_loss = 0
    total_accuracy = 0
    with torch.no_grad():
        for data in test_loader:
            imgs, targets = data
            imgs = imgs.to(device)
            targets = targets.to(device)
            output = lenet_5(imgs)
            loss = loss_fn(output, targets)
            total_test_loss = total_test_loss + loss.item()
            accuracy = (output.argmax(1) == targets).sum()
            total_accuracy = total_accuracy + accuracy

    print("整体测试集上的loss: {}".format(total_test_loss))
    print("整体测试集上的识别率: {}".format(total_accuracy/test_size))

    writer.add_scalar("test_loss", total_test_loss, total_test_step)
    writer.add_scalar("test_accuracy", total_accuracy/test_size, total_test_step)
    total_test_step = total_test_step + 1

    #保存最后一次模型
    if i == epoch - 1:
        torch.save(lenet_5, "./models/LeNet+.pth")
        print("最后一次模型已保存")

writer.close()
