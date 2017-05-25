import re
from collections import deque, OrderedDict
import html

def PREP_delete_speakers (text,repl = ''):
    new_text = re.sub('\n[\t ]*[А-ЯЁ ]+?(?: ?\(.+?\))? ?[.:]', '\n'+repl, text)
    if len(new_text) > len(text) - 500:
        new_text = re.sub('\n[\t ]*[А-яЁё]+?(?: ?\(.+?\))? ?[.:]','\n'+repl,text)
    return new_text


    
def go_through_texts(table,speakers):
    textlist = list(OrderedDict.fromkeys([x[0] for x in table]))
    formula_table = open('formula_list.csv','w',encoding='utf-8-sig')
    formula_table.write(';'.join(['document','left context','formula','','','unique','count'])+'\n')
    unique_deque = deque()
    for file in textlist:
        try:
            text = open('./texts/'+file+'.txt','r',encoding='cp1251').read()
        except:
            text = open('./texts/'+file+'.txt','r',encoding='utf-8-sig').read()
        text = html.unescape(text)
        new_table = table_for_text(table,file)
        unique_deque = contexts(text,new_table,formula_table,speakers,unique_deque)      
    formula_table.close()


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
    splitters = ['\.',',','\?','!',' -','\:',';','\}','\{',
                 ' -- ', '\(','\)', '\n+','…','"','—','–','»','«','[0-9]+','[A-z]+']
    for spl in splitters:
        if len(spl) == 1 or ('\\' in spl and len(spl) == 2) :
            one_symbols += spl[-1]
        else:
            regstr += spl+'|'
    regstr += one_symbols+']|)'
    return regstr



def contexts(text,table,formula_table,speakers,unique_deque):
    text = text.replace(';',',')
    if speakers:
        text = PREP_delete_speakers(text,'\t')
    spl = regstr_splitters()
    for n,row in enumerate(table):
        if type(row[3]) == str:
            unique_deque.append((row[3],row[4]))
        if row[2] == 1:
            if unique_deque:
                unique = unique_deque.popleft()
            else:
                unique = ('','')
            if n == 0:
                context = 'no context'
            else:
                if n == 1:
                    re_cl_context = '('+regstr(table[n-1][1])+' ?'+spl+'{1,3}\\s*?'+\
                                    spl+'{0,3} ?)('+regstr(row[1])+' ?'+spl+')'
                else:
                    re_cl_context = '('+regstr(table[n-2][1])+' ?'+spl+'{1,3}\\s*?'+\
                                    spl+'{0,3} ?'+regstr(table[n-1][1])+' ?'+spl+'{1,3}\\s*?'+\
                                    spl+'{0,3} ?)('+regstr(row[1])+' ?'+spl+')'
                phrase = re.search(re_cl_context,text)
                if not phrase:
                    context = 'context not found'
                else:
                    cl_context = phrase.group()
                    context_re = re.search('[.…!?]{1,3} ?[–—»)]?\s*?((?:[«(А-яЁёA-z0-9][^.…!?]*?[.…!?]{1,3}[»)]?\s*?){2}[^.…!?]*?'+re.escape(cl_context)+')',text)
                    if context_re is not None:
                        context = context_re.group(1)
                    else:
                        context = cl_context
                    context = re.sub('(\r?\n)+',' ',context)
                    context = context[:(len(context)-(len(row[1])+1))]
                    context = re.sub('\{+|\}+','',context)
            formula_table.write(';'.join([row[0],context,row[1],'','',unique[0],str(unique[1])])+'\n')
    return unique_deque
