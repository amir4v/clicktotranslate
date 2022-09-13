from django import template
from app.models import Text, Word


register = template.Library()


@register.filter(name='doiknow')
def do_i_know(value, arg):
    text = Text.objects.get(pk=arg)
    
    en = list(value.lower().strip().replace('<br>', ''))
    en = [
        c for c in en if c in 'qazwsxedcrfvtgbyhnujmikolpQAZWSXEDCRFVTGBYHNUJMIKOLP'
    ]    
    en = ''.join(en)
    
    if text.words.filter(en=en).exists():
        return 'checked'
    return ''