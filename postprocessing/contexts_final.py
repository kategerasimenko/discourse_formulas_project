import re
import time


def get_table(filename):
    table = []
    texttable = open(filename,'r',encoding='cp1251')
    for line in texttable:
        table.append(line.strip().split(';'))
    return table[1:]


def PREP_delete_speakers (text):
    new_text = re.sub('\n[\t ]*[А-ЯЁ ]+?(?: ?\(.+?\))?[.:]', '\n', text)
    if len(new_text) > len(text) - 500:
        print('speakers not in uppercase')
        new_text = re.sub('\n[\t ]*[А-яЁё]+?(?: ?\(.+?\))?[.:]','\n',text)
    return new_text


def get_list_of_texts(table):
    texts = set([x[0]+'.txt' for x in table])
    return texts

def get_etiquette():
    with open('etiquette_list.txt', 'r', encoding='utf-8-sig') as f:
        etiquette = {x.strip() for x in f.readlines()}
    return etiquette

def go_through_texts(textlist,table):
    new_full_table = []
    etiquette = get_etiquette()
    formula_table = open('formula_list.csv','w',encoding='utf-8-sig')
    formula_table.write(';'.join(['document','left context','formula'])+'\n')
    for file in textlist:
        print(file)
        try:
            text = open(file,'r',encoding='cp1251').read()
        except:
            text = open(file,'r',encoding='utf-8-sig').read()
        new_table = table_for_text(table,file[:-4])
        new_full_table += names_contexts(text,new_table,formula_table,etiquette)
    formula_table.close()
    return new_full_table


def table_for_text(table,textname):
    new_table = [x for x in table if x[0] == textname]
    return new_table


def regstr(formula):
    regstr = '['
    for i in formula:
        regstr += i+i.upper()+']['
    return regstr[:-1]


def regstr_splitters():
    regstr = '(?:'
    one_symbols = '['
    splitters = ['\.',',','\?','!',' -','\:',';',' ?или',' ?и','\}','\{',' -- ',
                 '\(','\)', '\n+','…','"','—','–','»','«','“','”','[0-9]+','[A-z]+']
    for spl in splitters:
        if len(spl) == 1 or ('\\' in spl and len(spl) == 2) :
            one_symbols += spl[-1]
        else:
            regstr += spl+'|'
    regstr += one_symbols+']|)'
    return regstr


def del_conj(string):
    if string.endswith(' или'):
        return string[:-4]
    if string.endswith(' и'):
        return string[:-2]
    return string


def names_contexts(text,table,formula_table,etiquette):
    text = text.replace(' ',' ').replace(';',',')
    text = PREP_delete_speakers(text)
    spl = regstr_splitters()
    for n,row in enumerate(table):
        words = row[1].split()
        if row[1] in etiquette:
            table[n][2] = '1'
        if table[n][2] == '1':
            if n == 0:
                context = 'no context'
            else:
                if n == 1:
                    re_cl_context = regstr(del_conj(table[n-1][1]))+' ?'+spl+'{1,3}\\s*?'+\
                                    spl+'{0,3} ?'+regstr(del_conj(row[1]))+' ?'+spl
                else:
                    re_cl_context = regstr(del_conj(table[n-2][1]))+' ?'+spl+'{1,3}\\s*?'+\
                                    spl+'{0,3} ?'+regstr(del_conj(table[n-1][1]))+' ?'+spl+'{1,3}\\s*?'+\
                                    spl+'{0,3} ?'+regstr(del_conj(row[1]))+' ?'+spl
                phrase = re.search(re_cl_context,text)
                if not phrase:
                    context = 'context not found'
                else:
                    cl_context = phrase.group()
                    context_re = re.search('[.…!?]{1,3} ?[–—»)”]?\s*?((?:[«“(А-яЁёA-z0-9][^.…!?]*?[.…!?]{1,3}[»)”]?\s*?){2}[^.…!?]*?'+re.escape(cl_context)+')',text)
                    if context_re is not None:
                        context = context_re.group(1)
                    else:
                        context = cl_context
                    context = re.sub('\n+',' ',context)
                    context = context[:(len(context)-(len(row[1])+1))]
            formula_table.write(';'.join([row[0],context,row[1]])+'\n')
    return table


start = time.time()
table = get_table('predicted.csv')
texts = get_list_of_texts(table)
table = go_through_texts(texts,table)
print('total running time:',time.time()-start)

