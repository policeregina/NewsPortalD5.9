from django import template
import re

register = template.Library()

UNWANTED_SYMBOLS = {'жир' : 'ж**',
                    'Жир' : 'Ж**',
                    'страна' : 'с*****',
                    'Страна' : 'С*****',
   }

@register.filter()
def censor(value):
    list_value = value.split()
    for i in list_value:
        i_ = re.sub(r'[^\w\s]', '', i)
        if i_ in UNWANTED_SYMBOLS.keys():
            k = UNWANTED_SYMBOLS[i_]
            value = value.replace(i_, k)
    return f'{value}'