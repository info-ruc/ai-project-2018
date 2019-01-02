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
wav_file = ['前进.wav']
wav_file = ['后退.wav']
# wav_file = ['左转.wav']
# wav_file = ['右转.wav']
text_label = ['前进 后退 左转 右转']
# print(type(wav_file))
bi_rnn.build_target_wav_file_test(wav_file, text_label)