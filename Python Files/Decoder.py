#####################################################################################################################################
#                                                                                                                                   #
#                                                    DECODER MODULE                                                                 #
#                                                                                                                                   #   
#                                                                                                                                   #
#####################################################################################################################################

# Importing Requisites
import torch
import torch.nn as nn
import torch.nn.functional as F

class DecoderRNN(nn.Module):
    def __init__(self, embedding_dim, hidden_dim, vocab_size):
        super(DecoderRNN, self).__init__()
        self.hidden_dim = hidden_dim
        self.word_embeddings = nn.Embedding(vocab_size, embedding_dim)
        self.gru = nn.GRU(embedding_dim, hidden_dim)
        self.linear = nn.Linear(hidden_dim, vocab_size)
        self.init_weights()
    
    def init_weights(self):
        self.word_embeddings.weight.data.uniform_(-0.1, 0.1)
        self.linear.weight.data.uniform_(-0.1, 0.1)
        self.linear.bias.data.fill_(0)
        
    def forward(self, features, caption):
        seq_length = len(caption) + 1
        embeds = self.word_embeddings(caption)
        embeds = torch.cat((features, embeds), 0)
        gru_out, _ = self.gru(embeds.unsqueeze(1))
        out = self.linear(gru_out.view(seq_length, -1))
        return out

    def get_caption_ids(self, cnn_out, seq_len = 20):
        ip = cnn_out
        hidden = None
        ids_list = []
        for t in range(seq_len):
            gru_out, hidden = self.gru(ip.unsqueeze(1), hidden)
            # generating single word at a time
            linear_out = self.linear(gru_out.squeeze(1))
            word_caption = gru_out.max(dim=1)[1]
            ids_list.append(word_caption)
            ip = self.word_embeddings(word_caption)
        return ids_list
        