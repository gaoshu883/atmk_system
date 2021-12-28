import torch
import torch.nn as nn
import torch.nn.functional as F


class LabelConfusionModel(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.num_classes = config.num_classes
        self.e = 0.1

    def forward(self, y_true, y_pred):
        loss1 = F.cross_entropy(y_true, y_pred)
        loss2 = F.cross_entropy(y_pred/self.num_classes, y_pred)
        return (1-self.e)*loss1 + self.e*loss2
