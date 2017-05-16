import os
import re

def get_formulas(text):
    formulas = re.findall('\{\{(.*?)\}\}',text)
    return formulas

def get_zeroes():
    anns = open('formulas_non-formulas.csv','r',encoding='cp1251')
    zeroanns = set()
    for line in anns:
        line = line.strip().split(';')
        if line[1] == '0':
            zeroanns.add(line[0])
    return zeroanns

def delete_non_formulas():
    texts = os.listdir('./texts')
    zeroanns = get_zeroes()
    for filename in texts:
        try:
            f = open('./texts/'+filename,'r',encoding='cp1251')
            text = f.read()
            f.close()
        except:
            f = open('./texts/'+filename,'r',encoding='utf-8-sig')
            text = f.read()
            f.close()        
        formulas = get_formulas(text)
        for formula in formulas:
            if formula.strip().strip('.,:;-!?()…{}[]"').strip().lower() in zeroanns:
                text = text.replace('{{'+formula+'}}',formula)
##      delete all contexts
        text = text.replace('$$','')
        text = text.replace('%%', '')
        
##      delete unnecessary contexts - not ideal
##      contexts = re.findall('\$\$([^\r\n]*?)\$\$(.*?(?:(?:\{)|(?:\$\${)|(?=\$)))',text,flags=re.DOTALL)
##      for context in contexts:
##          if not context[1].endswith('{'):
##              text = text.replace('$$'+context[0]+'$$',context[0])

        f = open('./texts/'+filename,'w',encoding='utf-8-sig')
        f.write(text)
        f.close()
