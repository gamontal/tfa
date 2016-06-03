import os
from tfa_nltk import analyzer

options = {
    'allow_digits': False,
    'ignore_list': [],
    'content': './samples/warandpeace.txt',
    'max_n_word': 4,
    'top_n': 4
}

results = analyzer(options)
print(results)
