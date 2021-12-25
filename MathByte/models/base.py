""" A base class for Model. """
import torch
import torch.nn as nn


class BaseModel(nn.Module):
    def __init__(self, config):
        super(BaseModel, self).__init__()
        self.embedding = self._load_embeddings()

    def _load_embeddings(self, embeddings):
        """Load the embeddings based on flag"""
        weight = torch.FloatTensor(embeddings)
        word_embeddings = torch.nn.Embedding.from_pretrained(weight)
        return word_embeddings
