import torch
import torch.nn as nn
import numpy as np

from .base import BaseModel


class Model(BaseModel):
    def __init__(self, config, use_attention=False):
        super(Model, self).__init__(config)
        self.lstm = nn.LSTM(config.emb_size, config.hidden_size, config.num_layers,
                            bidirectional=True, batch_first=True, dropout=config.dropout)
        self.fc = nn.Linear(config.hidden_size * 2, config.num_classes)

    def forward(self, x):
        x, _ = x
        # [batch_size, seq_len, embeding]=[128, 32, 300]
        out = self.embedding(x)
        out, _ = self.lstm(out)
        out = self.fc(out[:, -1, :])  # 句子最后时刻的 hidden state
        return out
