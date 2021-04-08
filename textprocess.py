import re
import json
import numpy as np
from collections import OrderedDict
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

def textProc(text):
  text = text.replace(';', '. ').replace('  ',' ').replace('\t',' ').replace('\n','').replace('---','').replace('__','').replace('--','')
  text = text.replace(r' ',' ').replace(' ',' ').replace('\x0c',' ').replace('•', '').replace('□','')
  while re.findall('\s\s', text):
    text = text.replace('  ', ' ')
  if text[0] == ' ':
    text = text[:0] + text[1:]
  end = len(text)-1
  if text[end] != '.':
    text = text[:end+1] + '.'
  if re.findall('[М|м]\.\s[П|п]\.|[М|м]\.[П|п]', text):
    n = re.findall('[М|м]\.\s[П|п]\.|[М|м]\.[П|п]', text)
    r = re.compile('[М|м]\.\s[П|п]\.|[М|м]\.[П|п]')
    for i in range(len(n)):
      result = [[m.start(), m.end()-1] for m in r.finditer(text)]
      text = text[:result[0][0]] + ' . ' + text[result[0][1]+1:]
  if re.search('Исх', text):
    result = re.search('Исх', text)
    if text[result.start()-1] != ' ':
      text = text[:result.start()] + ' ' + text[result.start():]
    result = re.search('Исх', text)
    if text[result.start()-1] == ' ':
      text = text[:result.start()-1] + ' .' + text[result.start()-1:]
    result = re.search('Исх', text)
    if text[result.end()] == '.' and text[result.end()+1] == ' ':
      text = text[:result.end()+1] + ',' + text[result.end()+1:]
  if re.search('ХАРАКТЕР', text):
    result = re.search('ХАРАКТЕР', text)
    if text[result.start()-1] != ' ':
      text = text[:result.start()] + ' ' + text[result.start():]
    result = re.search('ХАРАКТЕР', text)
    if text[result.start()-1] == ' ':
      text = text[:result.start()-1] + ' .' + text[result.start()-1:]
  if re.search('СВЕДЕНИЯ', text):
    result = re.search('СВЕДЕНИЯ', text)
    if text[result.start()-1] != ' ':
      text = text[:result.start()] + ' ' + text[result.start():]
    result = re.search('СВЕДЕНИЯ', text)
    if text[result.start()-1] == ' ':
      text = text[:result.start()-1] + ' .' + text[result.start()-1:]
  if re.search('ОПИСАНИЕ', text):
    result = re.search('ОПИСАНИЕ', text)
    if text[result.start()-1] != ' ':
      text = text[:result.start()] + ' ' + text[result.start():]
    result = re.search('ОПИСАНИЕ', text)
    if text[result.start()-1] == ' ':
      text = text[:result.start()-1] + ' .' + text[result.start()-1:]
  if re.search('СУММА', text):
    result = re.search('СУММА', text)
    if text[result.start()-1] != ' ':
      text = text[:result.start()] + ' ' + text[result.start():]
    result = re.search('СУММА', text)
    if text[result.start()-1] == ' ':
      text = text[:result.start()-1] + ' .' + text[result.start()-1:]
  if re.search('СРОК', text):
    result = re.search('СРОК', text)
    if text[result.start()-1] != ' ':
      text = text[:result.start()] + ' ' + text[result.start():]
    result = re.search('СРОК', text)
    if text[result.start()-1] == ' ':
      text = text[:result.start()-1] + ' .' + text[result.start()-1:]
  if re.search('ПЕРЕЧЕНЬ', text):
    result = re.search('ПЕРЕЧЕНЬ', text)
    if text[result.start()-1] != ' ':
      text = text[:result.start()] + ' ' + text[result.start():]
    result = re.search('ПЕРЕЧЕНЬ', text)
    if text[result.start()-1] == ' ':
      text = text[:result.start()-1] + ' .' + text[result.start()-1:]
  if re.search('ПРЕДМЕТ', text):
    result = re.search('ПРЕДМЕТ', text)
    if text[result.start()-1] != ' ':
      text = text[:result.start()] + ' ' + text[result.start():]
    result = re.search('ПРЕДМЕТ', text)
    if text[result.start()-1] == ' ':
      text = text[:result.start()-1] + ' .' + text[result.start()-1:]
  if re.search('РЕКВИЗИТЫ', text):
    result = re.search('РЕКВИЗИТЫ', text)
    if text[result.start()-1] != ' ':
      text = text[:result.start()] + ' ' + text[result.start():]
    result = re.search('РЕКВИЗИТЫ', text)
    if text[result.start()-1] == ' ':
      text = text[:result.start()-1] + ' .' + text[result.start()-1:]
  if re.search('ВИД', text):
    result = re.search('ВИД', text)
    if text[result.start()-1] != ' ':
      text = text[:result.start()] + ' ' + text[result.start():]
    result = re.search('ВИД', text)
    if text[result.start()-1] == ' ':
      text = text[:result.start()-1] + ' .' + text[result.start()-1:]
  if re.search('ИНЫЕ', text):
    result = re.search('ИНЫЕ', text)
    if text[result.start()-1] != ' ':
      text = text[:result.start()] + ' ' + text[result.start():]
    result = re.search('ИНЫЕ', text)
    if text[result.start()-1] == ' ':
      text = text[:result.start()-1] + ' .' + text[result.start()-1:]
  if re.search('ОСНОВАНИЕ', text):
    result = re.search('ОСНОВАНИЕ', text)
    if text[result.start()-1] != ' ':
      text = text[:result.start()] + ' ' + text[result.start():]
    result = re.search('ОСНОВАНИЕ', text)
    if text[result.start()-1] == ' ':
      text = text[:result.start()-1] + ' .' + text[result.start()-1:]
  if re.search('ОПРЕДЕЛЕНИЯ', text):
    result = re.search('ОПРЕДЕЛЕНИЯ', text)
    if text[result.start()-1] != ' ':
      text = text[:result.start()] + ' ' + text[result.start():]
    result = re.search('ОПРЕДЕЛЕНИЯ', text)
    if text[result.start()-1] == ' ':
      text = text[:result.start()-1] + ' .' + text[result.start()-1:]
  if re.search('ПРИЛАГАЕМЫЕ', text):
    result = re.search('ПРИЛАГАЕМЫЕ', text)
    if text[result.start()-1] != ' ':
      text = text[:result.start()] + ' ' + text[result.start():]
    result = re.search('ПРИЛАГАЕМЫЕ', text)
    if text[result.start()-1] == ' ':
      text = text[:result.start()-1] + ' .' + text[result.start()-1:]
  if re.search('к/с', text):
    result = re.search('к/с', text)
    if text[result.start()-1] != ' ':
      text = text[:result.start()] + ' ' + text[result.start():]
  if re.search('Отметк', text):
    result = re.search('Отметк', text)
    if text[result.start()-1] != ' ':
      text = text[:result.start()] + ' ' + text[result.start():]
    result = re.search('Отметк', text)
    if text[result.start()-1] == ' ':
      text = text[:result.start()-1] + ' .' + text[result.start()-1:]
  if re.findall('([\.|\s]19[0-9][0-9]\D|[\.|\s]20[0-9][0-9]\D)', text):
    n = re.findall('([\.|\s]19[0-9][0-9]\D|[\.|\s]20[0-9][0-9]\D)', text)
    r = re.compile('([\.|\s]19[0-9][0-9]\D|[\.|\s]20[0-9][0-9]\D)')
    for i in range(len(n)):
      result = [m.end() for m in r.finditer(text)]
      if text[result[i]-1] != '.' and text[result[i]-1] != 'г' and text[result[i]] == 'г' and text[result[i]+1] != 'о':
        text = text[:result[i]-1] + text[result[i]:]
  for i in range(len(n)):
    result = [m.end() for m in r.finditer(text)]
    if (text[result[i]] != '.' and text[result[i]-1] == 'г' and text[result[i]].isupper()) \
      or (text[result[i]] != '.' and text[result[i]-1] == 'г' and text[result[i]+1].islower()): 
      text = text[:result[i]] + '.' + text[result[i]:]
  for i in range(len(n)):
    result = [m.end() for m in r.finditer(text)]
    if (text[result[i]] == '.' and text[result[i]-1] == 'г' and text[result[i]+1].isupper()) \
      or (text[result[i]] == '.' and text[result[i]-1] == 'г' and text[result[i]+1].islower()): 
      text = text[:result[i]+1] + ' ' + text[result[i]+1:]
  for i in range(len(n)):
    result = [m.end() for m in r.finditer(text)]
    if (text[result[i]] == '.' and text[result[i]-1] == 'г' and text[result[i]+2].islower()) :
      text = text[:result[i]+1] + ',' + text[result[i]+1:]
  if re.findall('[\.|\s][1|2][098][0-9]{2}г\.\s{1,3}[)|(|№]|[\.|\s][1|2][098][0-9]{2}г\.[)|(|№]', text):
    n = re.findall('[\.|\s][1|2][098][0-9]{2}г\.\s{1,3}[)|(|№]|[\.|\s][1|2][098][0-9]{2}г\.[)|(|№]', text)
    r = re.compile('[\.|\s][1|2][098][0-9]{2}г\.\s{1,3}[)|(|№]|[\.|\s][1|2][098][0-9]{2}г\.[)|(|№]')
    for i in range(len(n)):
      result = [m.start()+6 for m in r.finditer(text)]
      text = text[:result[0]+1] + ',' + text[result[0]+1:]
  if re.findall('[\.|\s][1|2][098][0-9]{2}г\.\s{1,3}[\–|\-]|[\.|\s][1|2][098][0-9]{2}г\.\s[\–|\-]', text):
    n = re.findall('[\.|\s][1|2][098][0-9]{2}г\.\s{1,3}[\–|\-]|[\.|\s][1|2][098][0-9]{2}г\.\s[\–|\-]', text)
    r = re.compile('[\.|\s][1|2][098][0-9]{2}г\.\s{1,3}[\–|\-]|[\.|\s][1|2][098][0-9]{2}г\.\s[\–|\-]')
    for i in range(len(n)):
      result = [m.start()+6 for m in r.finditer(text)]
      text = text[:result[0]+1] + ',' + text[result[0]+1:]
  if re.findall('20[0-9]{2}\.[А-я]', text):
    n = re.findall('20[0-9]{2}\.[А-я]', text)
    r = re.compile('20[0-9]{2}\.[А-я]')
    for i in range(len(n)):
      result = [m.end()-1 for m in r.finditer(text)]
      text = text[:result[0]] + ' ' + text[result[0]:]
  if re.findall('[\.|\s][1|2][098][0-9]{2}г\.\s[)|(|№]|[\.|\s][1|2][098][0-9]{2}г\.\d', text):
    n = re.findall('[\.|\s][1|2][098][0-9]{2}г\.\s[)|(|№]|[\.|\s][1|2][098][0-9]{2}г\.\d', text)
    r = re.compile('[\.|\s][1|2][098][0-9]{2}г\.\s[)|(|№]|[\.|\s][1|2][098][0-9]{2}г\.\d')
    for i in range(len(n)):
      result = [m.end()-1 for m in r.finditer(text)]
      text = text[:result[0]] + ' ' + text[result[0]:]
  if re.findall('[\.|\s][1|2][098][0-9]{2}[^г^\s^\.^\d^\-]', text):
    n = re.findall('[\.|\s][1|2][098][0-9]{2}[^г^\s^\.^\d^\-]', text)
    r = re.compile('[\.|\s][1|2][098][0-9]{2}[^г^\s^\.^\d^\-]')
    for i in range(len(n)):
      result = [m.end()-1 for m in r.finditer(text)]
      text = text[:result[0]] + ' ' + text[result[0]:]
  if re.findall('года', text):
    n = re.findall('года', text)
    r = re.compile('года')
    for i in range(len(n)):
      result = [m.end() for m in r.finditer(text)]
      if text[result[0]].isupper(): 
        text = text[:result[0]] + '. ' + text[result[0]:]
      elif text[result[0]].isspace() and text[result[0]+1].isupper(): 
        text = text[:result[0]] + '.' + text[result[0]:]
  if re.findall('[)|»|"]\.[А-Я]', text):
    n = re.findall('[)|»|"]\.[А-Я]', text)
    r = re.compile('[)|»|"]\.[А-Я]')
    for i in range(len(n)):
      result = [m.start()+1 for m in r.finditer(text)] 
      text = text[:result[0]+1] + ' ' + text[result[0]+1:]
  if re.findall('[»|)|"]\d', text):
    n = re.findall('[»|)|"]\d', text)
    r = re.compile('[»|)|"]\d')
    for i in range(len(n)):
      result = [m.start()+1 for m in r.finditer(text)]
      text = text[:result[0]] + ' ' + text[result[0]:]
  if re.findall('[а-я]\.[А-Я]', text):
    n = re.findall('[а-я]\.[А-Я]', text)
    r = re.compile('[а-я]\.[А-Я]')
    for i in range(len(n)):
     result = [m.start()+1 for m in r.finditer(text)]
     text = text[:result[0]+1] + ' ' + text[result[0]+1:]
  if re.findall('\d\.\d\.\d\.', text):
   n = re.findall('\d\.\d\.\d\.', text)
   r = re.compile('\d\.\d\.\d\.')
   for i in range(len(n)):
     result = [m.end()-1 for m in r.finditer(text)] 
     text = text[:result[0]] + text[result[0]+1:]
  if re.findall('\d\.\d\.', text):
    n = re.findall('\d\.\d\.', text)
    r = re.compile('\d\.\d\.')
    for i in range(len(n)):
      result = [m.end()-1 for m in r.finditer(text)] 
      text = text[:result[0]] + text[result[0]+1:]
  if re.findall('\d\.\s[А-Я]', text):
    n = re.findall('\d\.\s[А-Я]', text)
    r = re.compile('\d\.\s[А-Я]')
    for i in range(len(n)):
      result = [m.start()+1 for m in r.finditer(text)]
      text = text[:result[0]] + text[result[0]+1:]
  if re.findall('[а-я]{4}\.\d\.\d', text):
    n = re.findall('[а-я]{4}\.\d\.\d', text)
    r = re.compile('[а-я]{4}\.\d\.\d')
    for i in range(len(n)):
      result = [m.start()+4 for m in r.finditer(text)] 
      text = text[:result[0]+1] + ' ' + text[result[0]+1:]
  if re.findall('п[\.|\.\s|\s\.]\d\.\D', text):
    n = re.findall('п[\.|\.\s|\s\.]\d\.\D', text)
    r = re.compile('п[\.|\.\s|\s\.]\d\.\D')
    for i in range(len(n)):
      result = [m.end()-1 for m in r.finditer(text)] 
      text = text[:result[0]-1] + text[result[0]:]
  if re.findall('п\.\s\d\.', text):
    n = re.findall('п\.\s\d\.', text)
    r = re.compile('п\.\s\d\.')
    for i in range(len(n)):
      result = [m.start()+2 for m in r.finditer(text)]
      text = text[:result[0]] + text[result[0]+1:]
  if re.findall('п\.\d\.\s[а-я]', text):
    n = re.findall('п\.\d\.\s[а-я]', text)
    r = re.compile('п\.\d\.\s[а-я]')
    for i in range(len(n)):
      result = [m.start()+3 for m in r.finditer(text)]
      text = text[:result[0]] + text[result[0]+1:]
  if re.findall('п\.\d\.\d{2}[А-я]|п\.\s\d\.\d{2}[А-я]', text):
    n = re.findall('п\.\d\.\d{2}[А-я]|п\.\s\d\.\d{2}[А-я]', text)
    r = re.compile('п\.\d\.\d{2}[А-я]|п\.\s\d\.\d{2}[А-я]')
    for i in range(len(n)):
      result = [m.end()-1 for m in r.finditer(text)]
      text = text[:result[0]] + ' ' + text[result[0]:]
  if re.findall('[а-я][А-Я]', text):
    n = re.findall('[а-я][А-Я]', text)
    r = re.compile('[а-я][А-Я]')
    for i in range(len(n)):
      result = [m.end()-1 for m in r.finditer(text)]
      text = text[:result[0]] + ' ' + text[result[0]:]
  if re.findall('[А-Я]{2}\.[А-Я][^\.]', text):
    n = re.findall('[А-Я]{2}\.[А-Я][^\.]', text)
    r = re.compile('[А-Я]{2}\.[А-Я][^\.]')
    for i in range(len(n)):
      result = [m.end()-2 for m in r.finditer(text)]
      text = text[:result[0]] + ' ' + text[result[0]:]
  if re.findall('[А-я][«|(|"]\w', text):
    n = re.findall('[А-я][«|(|"]\w', text)
    r = re.compile('[А-я][«|(|"]\w')
    for i in range(len(n)):
      result = [m.start()+1 for m in r.finditer(text)]
      text = text[:result[0]] + ' ' + text[result[0]:]
  if re.findall('[»|)|"][\w|\.]\w', text):
    n = re.findall('[»|)|"][\w|\.]\w', text)
    r = re.compile('[»|)|"][\w|\.]\w')
    for i in range(len(n)):
      result = [m.end()-2 for m in r.finditer(text)]
      if text[result[0]] == '.':
        text = text[:result[0]+1] + ' ' + text[result[0]+1:]
      else: 
        text = text[:result[0]] + ' ' + text[result[0]:]
  if re.findall('[\D|^р]\/[А-Я]', text):
    n = re.findall('[\D|^р]\/[А-Я]', text)
    r = re.compile('[\D|^р]\/[А-Я]')
    for i in range(len(n)):
      result = [m.end()-1 for m in r.finditer(text)]
      text = text[:result[0]-1] + text[result[0]:]
  if re.findall('[а-я|\D]\/[^с]', text):
    n = re.findall('[а-я|\D]\/[^с]', text)
    r = re.compile('[а-я|\D]\/[^с]')
    for i in range(len(n)):
      result = [m.end()-1 for m in r.finditer(text)]
      text = text[:result[0]-1] + text[result[0]:]
  if re.findall('расч\.\s\с', text):
    n = re.findall('расч\.\s\с', text)
    r = re.compile('расч\.\s\с')
    for i in range(len(n)):
      result = [m.end()-1 for m in r.finditer(text)]
      text = text[:result[0]-1] + text[result[0]:]
  if re.findall('[А-яа-яА-Я]{3,4}\:[\w|\S]', text):
    n = re.findall('[А-яа-яА-Я]{3,4}:[\w|\S]', text)
    r = re.compile('[А-яа-яА-Я]{3,4}:[\w|\S]')
    for i in range(len(n)):
      result = [m.end()-1 for m in r.finditer(text)]
      text = text[:result[0]] + ' ' + text[result[0]:]
  if re.findall('[А-я]{4,6}\.\d\.', text):
    n = re.findall('[А-я]{4,6}\.\d\.', text)
    r = re.compile('[А-я]{4,6}\.\d\.')
    for i in range(len(n)):
      result = [m.end()-2 for m in r.finditer(text)]
      text = text[:result[0]] + ' ' + text[result[0]:]
  if re.findall('[А-я]{4,6}\.\d', text):
    n = re.findall('[А-я]{4,6}\.\d', text)
    r = re.compile('[А-я]{4,6}\.\d')
    for i in range(len(n)):
      result = [m.end()-1 for m in r.finditer(text)]
      text = text[:result[0]] + ' ' + text[result[0]:]
  if re.findall('[А-я]{4,6}\.\d{2}\.', text):
    n = re.findall('[А-я]{4,6}\.\d{2}\.', text)
    r = re.compile('[А-я]{4,6}\.\d{2}\.')
    for i in range(len(n)):
      result = [m.end()-3 for m in r.finditer(text)]
      text = text[:result[0]] + ' ' + text[result[0]:]
  if re.findall('[А-я]{3,4}.{1,2}\.\s\d{1,2}\.\s[А-Я]', text):
    n = re.findall('[А-я]{3,4}.{1,2}\.\s\d{1,2}\.\s[А-Я]', text)
    r = re.compile('[А-я]{3,4}.{1,2}\.\s\d{1,2}\.\s[А-Я]')
    for i in range(len(n)):
      result = [m.end()-3 for m in r.finditer(text)]
      text = text[:result[0]] + text[result[0]+1:]
  if re.findall('\d{3,4}\,[А-я]', text):
    n = re.findall('\d{3,4}\,[А-я]', text)
    r = re.compile('\d{3,4}\,[А-я]')
    for i in range(len(n)):
      result = [m.end()-1 for m in r.finditer(text)]
      text = text[:result[0]] + ' ' + text[result[0]:]
  if re.findall('\:\s\d\.[А-Я]', text):
    n = re.findall('\:\s\d\.[А-Я]', text)
    r = re.compile('\:\s\d\.[А-Я]')
    for i in range(len(n)):
      result = [m.start()+4 for m in r.finditer(text)]
      text = text[:result[0]] + ' ' + text[result[0]:]
  if re.findall('оф\.\s\d{1,2}', text):
    n = re.findall('оф\.\s\d{1,2}', text)
    r = re.compile('оф\.\s\d{1,2}')
    for i in range(len(n)):
      result = [m.start()+3 for m in r.finditer(text)]
      text = text[:result[0]] + text[result[0]+1:]
  if re.findall('\d{4,6}[А-Я]', text):
    n = re.findall('\d{4,6}[А-Я]', text)
    r = re.compile('\d{4,6}[А-Я]')
    for i in range(len(n)):
      result = [m.end()-1 for m in r.finditer(text)]
      text = text[:result[0]] + ' ' + text[result[0]:]
  if re.findall('\d{4,6}\.[А-Я]', text):
    n = re.findall('\d{4,6}\.[А-Я]', text)
    r = re.compile('\d{4,6}\.[А-Я]')
    for i in range(len(n)):
      result = [m.end()-1 for m in r.finditer(text)]
      text = text[:result[0]] + ' ' + text[result[0]:]
  if re.findall('\d{5,8}\.[А-я]', text):
    n = re.findall('\d{5,8}\.[А-я]', text)
    r = re.compile('\d{5,8}\.[А-я]')
    for i in range(len(n)):
      result = [m.end()-1 for m in r.finditer(text)]
      text = text[:result[0]] + ' ' + text[result[0]:]
  if re.findall('\d\.\d{2}[А-Я]', text):
    n = re.findall('\d\.\d{2}[А-Я]', text)
    r = re.compile('\d\.\d{2}[А-Я]')
    for i in range(len(n)):
      result = [m.end()-1 for m in r.finditer(text)]
      text = text[:result[0]] + ' ' + text[result[0]:]
  if re.findall('[А-Я]{4,6}\d\.\d', text):
    n = re.findall('[А-Я]{4,6}\d\.\d', text)
    r = re.compile('[А-Я]{4,6}\d\.\d')
    for i in range(len(n)):
      result = [m.end()-3 for m in r.finditer(text)]
      text = text[:result[0]] + ' ' + text[result[0]:]
  if re.findall('\d\.\d[А-Я]', text):
    n = re.findall('\d\.\d[А-Я]', text)
    r = re.compile('\d\.\d[А-Я]')
    for i in range(len(n)):
      result = [m.start()+3 for m in r.finditer(text)]
      text = text[:result[0]] + ' ' + text[result[0]:]
  if re.findall('\-\s\d\.[А-Я]', text):
    n = re.findall('\-\s\d\.[А-Я]', text)
    r = re.compile('\-\s\d\.[А-Я]')
    for i in range(len(n)):
      result = [m.end()-1 for m in r.finditer(text)]
      text = text[:result[0]] + ' ' + text[result[0]:]
  if re.findall('\S\(', text):
    n = re.findall('\S\(', text)
    r = re.compile('\S\(')
    for i in range(len(n)):
      result = [m.end()-1 for m in r.finditer(text)]
      text = text[:result[0]] + ' ' + text[result[0]:]
  if re.findall('\)[А-я]', text):
    n = re.findall('\)[А-я]', text)
    r = re.compile('\)[А-я]')
    for i in range(len(n)):
      result = [m.end()-1 for m in r.finditer(text)]
      text = text[:result[0]] + ' ' + text[result[0]:]
  if re.findall('\,[^\s\d]', text):
    n = re.findall('\,[^\s\d]', text)
    r = re.compile('\,[^\s\d]')
    for i in range(len(n)):
      result = [m.end()-1 for m in r.finditer(text)]
      text = text[:result[0]] + ' ' + text[result[0]:]
  if re.findall('комн\.\s\d{1,3}', text):
    n = re.findall('комн\.\s\d{1,3}', text)
    r = re.compile('комн\.\s\d{1,3}')
    for i in range(len(n)):
      result = [m.start()+5 for m in r.finditer(text)]
      text = text[:result[0]] + text[result[0]+1:]
  if re.findall('ком\.\s\d{1,3}', text):
    n = re.findall('ком\.\s\d{1,3}', text)
    r = re.compile('ком\.\s\d{1,3}')
    for i in range(len(n)):
      result = [m.start()+4 for m in r.finditer(text)]
      text = text[:result[0]] + text[result[0]+1:]
  if re.findall('влд\.\s\d{1,3}', text):
    n = re.findall('влд\.\s\d{1,3}', text)
    r = re.compile('влд\.\s\d{1,3}')
    for i in range(len(n)):
      result = [m.start()+4 for m in r.finditer(text)]
      text = text[:result[0]] + text[result[0]+1:]
  if re.findall('эт\.\s\d{1,3}', text):
    n = re.findall('эт\.\s\d{1,3}', text)
    r = re.compile('эт\.\s\d{1,3}')
    for i in range(len(n)):
      result = [m.start()+3 for m in r.finditer(text)]
      text = text[:result[0]] + text[result[0]+1:]
  if re.findall('кв\.\s\d{1,3}', text):
    n = re.findall('кв\.\s\d{1,3}', text)
    r = re.compile('кв\.\s\d{1,3}')
    for i in range(len(n)):
      result = [m.start()+3 for m in r.finditer(text)]
      text = text[:result[0]] + text[result[0]+1:]
  if re.findall('д\.\s\d{1,2}[А-Я]|д\.\d{1,2}[А-Я]', text):
    n = re.findall('д\.\s\d{1,2}[А-Я]|д\.\d{1,2}[А-Я]', text)
    r = re.compile('д\.\s\d{1,2}[А-Я]|д\.\d{1,2}[А-Я]')
    for i in range(len(n)):
      result = [m.end()-1 for m in r.finditer(text)]
      text = text[:result[0]] + ' ' + text[result[0]:]
  if re.findall('стр\.\s\d{1,2}[А-Я]|стр\.\d{1,2}[А-Я]', text):
    n = re.findall('стр\.\s\d{1,2}[А-Я]|стр\.\d{1,2}[А-Я]', text)
    r = re.compile('стр\.\s\d{1,2}[А-Я]|стр\.\d{1,2}[А-Я]')
    for i in range(len(n)):
      result = [m.end()-1 for m in r.finditer(text)]
      text = text[:result[0]] + ' ' + text[result[0]:]
  if re.findall('\w\_\D', text):
    n = re.findall('\w\_\D', text)
    r = re.compile('\w\_\D')
    for i in range(len(n)):
      result = [m.end()-2 for m in r.finditer(text)]
      text = text[:result[0]] + text[result[0]+1:]
  if re.findall('\D\_\w', text):
    n = re.findall('\D\_\w', text)
    r = re.compile('\D\_\w')
    for i in range(len(n)):
      result = [m.end()-2 for m in r.finditer(text)]
      text = text[:result[0]] + text[result[0]+1:]
  if re.findall('\s\_\s', text):
    n = re.findall('\s\_\s', text)
    r = re.compile('\s\_\s')
    for i in range(len(n)):
      result = [m.end()-2 for m in r.finditer(text)]
      text = text[:result[0]] + text[result[0]+1:]
  while re.findall('\.\.', text):
    text = text.replace('..', '.')
  while re.findall('\s\s', text):
    text = text.replace('  ', ' ')

  return text

def sentProc(sents):
 for s in sents:
   if len(s) < 5:
     sents.remove(s)
 sentences = []
 for s in sents:
   if re.findall('\s\.', s):
     n = re.findall('\s\.', s)
     r = re.compile('\s\.')
     for i in range(len(n)):
       result = [m.start() for m in r.finditer(s)]
       s = s[:result[0]] + s[result[0]+1:]
   if re.findall('\"\s[А-Я]', s):
     n = re.findall('\"\s[А-Я]', s)
     r = re.compile('\"\s[А-Я]')
     for i in range(len(n)):
       result = [m.end()-2 for m in r.finditer(s)]
       s = s[:result[0]] + s[result[0]+1:]
   if re.findall('\s\)', s):
     n = re.findall('\s\)', s)
     r = re.compile('\s\)')
     for i in range(len(n)):
       result = [m.end()-2 for m in r.finditer(s)]
       s = s[:result[0]] + s[result[0]+1:]
   if re.findall('\,\)', s):
     n = re.findall('\,\)', s)
     r = re.compile('\,\)')
     for i in range(len(n)):
       result = [m.end()-2 for m in r.finditer(s)]
       s = s[:result[0]] + s[result[0]+1:]
   if re.findall('\.\.', s):
     n = re.findall('\.\.', s)
     r = re.compile('\.\.')
     for i in range(len(n)):
       result = [m.end()-2 for m in r.finditer(s)]
       s = s[:result[0]] + s[result[0]+1:]   
   sentences.append(s)
 for s in sentences:
   if len(s) < 5:
    sentences.remove(s)

 return sentences

def getWords(sentences):
  f_words = []
  for w in range(len(sentences)):
    word = ''
    s_words = []
    for i in range(len(sentences[w])):
        if not(sentences[w][i] == ' ' or sentences[w][i] == ',' or sentences[w][i] == '.' or sentences[w][i] == ':' or sentences[w][i] == '('
              or sentences[w][i] == ')' or sentences[w][i] == '/' or sentences[w][i] == '"' or sentences[w][i] == '<'
              or sentences[w][i] == '«' or sentences[w][i] == '»' or sentences[w][i] == '?' or sentences[w][i] == ';'):
          word += sentences[w][i]
        else:
          s_words.append(word)
          if not(sentences[w][i] == ' '):
            s_words.append(str(sentences[w][i]))
          word = ''
    f_words.append(s_words)

  set_words = []
  for i in range(len(f_words)):
    d = []
    for l in range(len(f_words[i])):
      if not(f_words[i][l] == ''):
        d.append(f_words[i][l])
    set_words.append(d)

  return set_words