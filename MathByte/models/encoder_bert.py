import torch
import torch.nn as nn
from pytorch_pretrained import BertModel, BertTokenizer


class EncoderBERT(nn.Module):

    def __init__(self, config):
        super(EncoderBERT, self).__init__()
        self.bert = BertModel.from_pretrained(config.bert_path)
        for param in self.bert.parameters():
            param.requires_grad = True
        self.fc = nn.Linear(config.hidden_size, config.num_classes)

    def forward(self, x):
        context = x[0]  # 输入的句子
        # 对padding部分进行mask，和句子一个size，padding部分用0表示，如：[1, 1, 1, 1, 0, 0]
        mask = x[2]
        _, pooled = self.bert(context, attention_mask=mask,
                              output_all_encoded_layers=False)
        out = self.fc(pooled)
        return out
