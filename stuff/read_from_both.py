from clicktotranslate import settings

en_path = 'stuff/'+'All-English-Words.txt'
all_en = open(settings.BASE_DIR / en_path, 'r').read().split('\n')
fa_path = 'stuff/'+'All-Persian-Words.txt'
all_fa = open(settings.BASE_DIR / fa_path, 'r').read().split('\n')

def get():
    return zip(all_en, all_fa)
