import torch
import torch.nn as nn
import torch.nn.functional as F

from .base import BaseModel

class Model(BaseModel):
    def __init__(self, config, use_attention=False):
        super(Model, self).__init__(config)
        self.use_att = use_attention
        self.convs = nn.ModuleList(
            [nn.Conv2d(1, config.num_filters, (k, config.emb_size)) for k in config.filter_sizes])
        self.dropout = nn.Dropout(config.dropout)
        self.fc = nn.Linear(config.num_filters *
                            len(config.filter_sizes), config.num_classes)

    def conv_and_pool(self, x, conv):
        x = F.relu(conv(x)).squeeze(3)
        x = F.max_pool1d(x, x.size(2)).squeeze(2)
        return x

    def forward(self, x):
        out = self.embedding(x[0])
        out = out.unsqueeze(1)
        out = torch.cat([self.conv_and_pool(out, conv)
                        for conv in self.convs], 1)
        out = self.dropout(out)
        if self.use_att:
            out = self.label_att(out, x[0])
        out = self.fc(out)
        return out
