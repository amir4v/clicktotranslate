from clicktotranslate import settings

en_path = 'stuff/'+'All-English-Words.txt'
all_en = open(settings.BASE_DIR / en_path, 'r').read().split('\n')
fa_path = 'stuff/'+'All-Persian-Words.txt'
all_fa = open(settings.BASE_DIR / fa_path, 'r').read().split('\n')

def get():
    return zip(all_en, all_fa)

"""
from stuff import read_from_both as r
from app.models import Word
words = [
    Word(
            en=w[0].lower(),
            fa=w[1].lower()
        ) for w in r.get()
]
Word.objects.bulk_create(words)
"""
