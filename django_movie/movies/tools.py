from django.utils.text import slugify
from django.utils.deconstruct import deconstructible

import os


def transliterate(s):
    slovar = {'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e',
      'ж':'zh','з':'z','и':'i','й':'i','к':'k','л':'l','м':'m','н':'n',
      'о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'h',
      'ц':'c','ч':'cz','ш':'sh','щ':'scz','ъ':'','ы':'y','ь':'','э':'e',
      'ю':'u','я':'ja', 'А':'A','Б':'B','В':'V','Г':'G','Д':'D','Е':'E','Ё':'E',
      'Ж':'ZH','З':'Z','И':'I','Й':'I','К':'K','Л':'L','М':'M','Н':'N',
      'О':'O','П':'P','Р':'R','С':'S','Т':'T','У':'U','Ф':'F','Х':'H',
      'Ц':'C','Ч':'CZ','Ш':'SH','Щ':'SCH','Ъ':'','Ы':'y','Ь':'','Э':'E',
      'Ю':'U','Я':'YA',',':'','?':'',' ':'_','~':'','!':'','@':'','#':'',
      '$':'','%':'','^':'','&':'','*':'','(':'',')':'','-':'','=':'','+':'',
      ':':'',';':'','<':'','>':'','\'':'','"':'','\\':'','/':'','№':'',
      '[':'',']':'','{':'','}':'','ґ':'','ї':'', 'є':'','Ґ':'g','Ї':'i',
      'Є':'e', '—':''}
    return slugify(''.join(slovar.get(w, w) for w in s.lower()), allow_unicode=True)


@deconstructible
class Path_and_rename:
    def __init__(self, path='media', postfix=None):
        self.path = path
        self.postfix = postfix

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        if getattr(instance, 'name', None):
            title = transliterate(instance.name)
        elif getattr(instance, 'title', None):
            title = transliterate(instance.title)

        if title and self.postfix:
            filename = '{}_{}.{}'.format(title, self.postfix, ext)
        elif title:
            filename = '{}.{}'.format(title, ext)
        else:
            from uuid import uuid4
            filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join(self.path, filename)


# def path_and_rename(path='media', postfix=None):
#     def wrapper(instance, filename):
#         ext = filename.split('.')[-1]
#         if getattr(instance, 'name', None):
#             title = transliterate(instance.name)
#         elif getattr(instance, 'title', None):
#             title = transliterate(instance.title)

#         if title and postfix:
#             filename = '{}_{}.{}'.format(title, postfix, ext)
#         elif title:
#             filename = '{}.{}'.format(title, ext)
#         else:
#             from uuid import uuid4
#             filename = '{}.{}'.format(uuid4().hex, ext)
#         return os.path.join(path, filename)
#     return wrapper
