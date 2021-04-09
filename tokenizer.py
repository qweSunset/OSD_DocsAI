import json
import numpy as np
from collections import OrderedDict
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

max_len = 100
max_len_char = 15

def tokenWords(set_words):
  X_word = []
  unkWords = []
  for s in set_words:
    sets = []
    unkSet = []
    for w in s:
      try:
        if (word2idx[w]):
          sets.append(word2idx[w])
      except:
        sets.append(word2idx['UNK'])
        unkSet.append(w)
    X_word.append(sets)
    unkWords.append(unkSet)
  X_word = pad_sequences(maxlen=max_len, sequences=X_word, value=word2idx["PAD"], padding='post', truncating='post')
  return [X_word, unkWords]

def tokenChars(set_words):
  X_char = []
  for sentence in set_words:
      sent_seq = []
      for i in range(max_len):
          word_seq = []
          for j in range(max_len_char):
              try:
                  word_seq.append(char2idx.get(sentence[i][j]))
              except:
                  word_seq.append(char2idx.get("PAD"))
          sent_seq.append(word_seq)
      X_char.append(np.array(sent_seq))
  X_char = np.array(X_char).reshape((len(X_char), max_len, max_len_char))
  return X_char

def getJson(test_pred, X_word, unkWords):
  outdict = []
  for i in range(len(test_pred)):
    wid = 0
    sent = OrderedDict()
    for w, pred in zip(X_word[i], np.argmax(test_pred[i], axis=-1)):
      if w != 0:
        if w == 1:
          sent[unkWords[i][wid]] = idx2tag[str(pred)]
          wid += 1
        else:
          sent[idx2word[str(w)]] = idx2tag[str(pred)]
    outdict.append(sent)
  jsonString = json.dumps(outdict)
  return jsonString
