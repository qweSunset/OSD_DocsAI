import json
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
from keras.models import Model
model = load_model('model/MODEL.hdf5')

with open('tokenizer/ix2wd.json') as json_file:
    idx2word = json.load(json_file)
with open('tokenizer/wd2ix.json') as json_file:
    word2idx = json.load(json_file)
with open('tokenizer/ix2tg.json') as json_file:
    idx2tag = json.load(json_file)
with open('tokenizer/tg2ix.json') as json_file:
    tag2idx = json.load(json_file)
with open('tokenizer/ch2ix.json') as json_file:
    char2idx = json.load(json_file)
