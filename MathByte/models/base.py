""" A base class for Model. """
import torch
import torch.nn as nn
import utils
from .attention import LabelAttention


class BaseModel(nn.Module):
    def __init__(self, config):
        super(BaseModel, self).__init__()
        embeddings = utils.load_embed_data(config.embeddings)
        self.embedding = self._load_embeddings(embeddings)
        self.label_att = LabelAttention()

    def _load_embeddings(self, embeddings):
        """Load the embeddings based on flag"""
        weight = torch.FloatTensor(embeddings)
        word_embeddings = torch.nn.Embedding.from_pretrained(weight)
        return word_embeddings
