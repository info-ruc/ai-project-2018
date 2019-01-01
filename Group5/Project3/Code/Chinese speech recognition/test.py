# -*- coding: utf-8 -*-

import os

import utils
from config import Config
from model import BiRNN

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

print('# Config')
conf = Config()
print('# Load waves and labels')
wav_files, text_labels = utils.get_wavs_lables()
print('# Create dictionary')
words_size, words, word_num_map = utils.create_dict(text_labels)
print('# Build Model')
bi_rnn = BiRNN(wav_files, text_labels, words_size, words, word_num_map)
print('# Begin to test')
bi_rnn.build_test()