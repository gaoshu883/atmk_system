import torch
import torch.nn as nn
import torch.nn.functional as F


class LabelAttention(nn.Module):

    def __init__(self, dim):
        super(LabelAttention, self).__init__()
        self.linear_in = nn.Linear(dim, dim)
        self.linear_out = nn.Linear(dim*2, dim)
        self.mask = None

    def set_mask(self, mask):
        """
        Sets indices to be masked

        Args:
            mask (torch.Tensor): tensor containing indices to be masked
        """
        self.mask = mask

    def forward(self, x):
        embeddings = self.embeddings(x)
        embeddings = self.embedding_dropout(embeddings)
        # step1 get LSTM outputs
        hidden_state = self.init_hidden()
        outputs, hidden_state = self.lstm(embeddings, hidden_state)
        # step2 get self-attention
        selfatt = torch.tanh(self.linear_first(outputs))
        selfatt = self.linear_second(selfatt)
        selfatt = F.softmax(selfatt, dim=1)
        selfatt = selfatt.transpose(1, 2)
        self_att = torch.bmm(selfatt, outputs)
        # step3 get label-attention
        h1 = outputs[:, :, :self.lstm_hid_dim]
        h2 = outputs[:, :, self.lstm_hid_dim:]

        label = self.label_embed.weight.data
        m1 = torch.bmm(label.expand(self.batch_size, self.n_classes,
                       self.lstm_hid_dim), h1.transpose(1, 2))
        m2 = torch.bmm(label.expand(self.batch_size, self.n_classes,
                       self.lstm_hid_dim), h2.transpose(1, 2))
        label_att = torch.cat((torch.bmm(m1, h1), torch.bmm(m2, h2)), 2)
        # label_att = F.normalize(label_att, p=2, dim=-1)
        # self_att = F.normalize(self_att, p=2, dim=-1) #all can
        weight1 = torch.sigmoid(self.weight1(label_att))
        weight2 = torch.sigmoid(self.weight2(self_att))
        weight1 = weight1/(weight1+weight2)
        weight2 = 1-weight1

        doc = weight1*label_att+weight2*self_att
        # there two method, for simple, just add
        # also can use linear to do it
        avg_sentence_embeddings = torch.sum(doc, 1)/self.n_classes

        pred = torch.sigmoid(self.output_layer(avg_sentence_embeddings))
        return pred
