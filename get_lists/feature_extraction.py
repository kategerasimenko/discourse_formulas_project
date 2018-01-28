import re

class TextByLines:
    def __init__(self, intext):
        self.text = intext
        self.lines = self.text.split('\n')


def joinarrays(a1, a2):
    for i in a2:
        a1.append(i)
    return a1

    
def PREP_delete_speakers (text):
    new_text = re.sub('\n[ ]*[А-ЯЁ ]+?(?: ?\(.+?\))? ?[.:]', '\n', text)
    if len(new_text) > len(text) - 500:
        print('speakers not in uppercase')
        new_text = re.sub('\n[ ]*[А-яЁё]+?(?: ?\(.+?\))? ?[.:]','\n',text)
    return new_text

    
def is_discourse(text):
    if ('}}' in text and not text.startswith('}}')) or ('{{' in text and not text.endswith('{{')):
        d = 1
        before = re.search('(^[^{}]+?\\w+.*?){{', text)
        if before is not None:
            d = 0
        else:
            after = re.search('}}([^{}]+?\\w+.*)', text)
            if after is not None:
                d = 0
    else:
        d = 0
    text = text.replace('{{', '')
    text = text.replace('}}', '')
    return d, text.lower()


def splitbylist (a, splist):
    for i in splist:
        a = a.replace(i, i+'<<splitter>>')
    out = a.split('<<splitter>>')
    return out
        