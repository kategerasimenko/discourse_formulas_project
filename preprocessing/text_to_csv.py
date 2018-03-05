from feature_extraction import *
from delete_zeroes import *
import csv
import re
import os

razm = input('Are files annotated? [y/n]')

#открыть и закрыть файлы для записи, чтобы при новом запуске программы файл создавался с нуля, а не добавлялся к старому
if razm == 'y':
    csvdata = open('train_data.csv', 'w', encoding='utf-8-sig')
    writer = csv.writer(csvdata, delimiter=';', quotechar='"', lineterminator='\n', quoting=csv.QUOTE_NONNUMERIC)
    row0 = ['Text_id', 'Text', 'Len', 'Subject', 'Object',  'Predicate', 'Emotions',  'Imperative', 'Question',
            'First', 'NOUN', 'ADJF', 'ADJS', 'COMP', 'VERB', 'INFN', 'PRTF', 'PRTS', 'GRND', 'NUMR', 'ADVB', 'NPRO', 'PRED', 'PREP', 'CONJ', 'PRCL', 'INTJ']
    writer.writerow(row0)
    csvdata.close()

    csvtarget = open('train_target.csv', 'w', encoding='utf-8-sig')
    row0 = ['Target']
    writer = csv.writer(csvtarget, delimiter=';', quotechar='"', lineterminator='\n', quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(row0)
    csvtarget.close()
    
    #delete_non_formulas()

else:
    csvdata = open('test_data.csv', 'w', encoding='utf-8-sig')
    writer = csv.writer(csvdata, delimiter=';', quotechar='"', lineterminator='\n', quoting=csv.QUOTE_NONNUMERIC)
    row0 = ['Text_id', 'Text', 'Len', 'Subject', 'Object',  'Predicate', 'Emotions',  'Imperative', 'Question',
            'First', 'NOUN', 'ADJF', 'ADJS', 'COMP', 'VERB', 'INFN', 'PRTF', 'PRTS', 'GRND', 'NUMR', 'ADVB', 'NPRO', 'PRED', 'PREP', 'CONJ', 'PRCL', 'INTJ']
    writer.writerow(row0)
    csvdata.close()

filenames = os.listdir('./texts')

for filename in filenames:
    if filename.endswith('.txt'):
        try:
            filein = open('./texts/'+filename, 'r', encoding='cp1251')
            rawtext = filein.read()
            filein.close()
        except:
            filein = open('./texts/'+filename, 'r', encoding='utf-8-sig')
            rawtext = filein.read()
            filein.close()
        print(filename)
        rawtext = PREP_delete_speakers(rawtext)
        linedtext = TextByLines(rawtext)
        allpseudoclauses_raw = []
        allpseudoclauses = []
        disc_target = []

        for j in linedtext.lines:
            curlinesplitted = splitbylist(j, ['.',',','?','!',' - ',':',';',' или ',' и ','(',')', '\n','…','"','—',' – ','»','”'])
            firstalreadybeen = False
            firstthree = 1
            for i in curlinesplitted:
                if re.findall('[А-яЁё]', i, flags=re.DOTALL):
                    disc, i = is_discourse(i.strip())
                    disc_target.append(disc)
                    if firstthree <= 3:
                        allpseudoclauses.append(Pseudoclause(i, str(disc), True))
                    else:
                        allpseudoclauses.append(Pseudoclause(i, str(disc), False))
                    firstthree += 1

        if razm == 'y':
            csvdata = open('train_data.csv', 'a', encoding='utf-8-sig')
        else:
            csvdata = open('test_data.csv', 'a', encoding='utf-8-sig')

        writer = csv.writer(csvdata, delimiter=';', quotechar='"', lineterminator='\n', quoting=csv.QUOTE_NONNUMERIC)
        for n in range(len(allpseudoclauses)):
            new_words = allpseudoclauses[n].text.strip('.,?!-:;()…"—–{}«»“”/\\').strip()
            row = [filename[:-4], new_words, len(new_words.split())]

            if len(allpseudoclauses[n].subject) > 0:
                row.append(1)
            else:
                row.append(0)

            if allpseudoclauses[n].object == '<<not required>>':
                row.append(0)
            elif allpseudoclauses[n].object:
                row.append(1)
            else:
                row.append(-1)

            if allpseudoclauses[n].predicate != 'no predicate':
                row.append(1)
            else:
                row.append(0)

            if allpseudoclauses[n].emotions:
                row.append(1)
            else:
                row.append(0)
            if allpseudoclauses[n].imperativeness:
                row.append(1)
            else:
                row.append(0)
            if allpseudoclauses[n].isquestion:
                row.append(1)
            else:
                row.append(0)
            if allpseudoclauses[n].firstinline:
                row.append(1)
            else:
                row.append(0)
            POS_list = []
            for i in ['NOUN', 'ADJF', 'ADJS', 'COMP', 'VERB', 'INFN', 'PRTF', 'PRTS', 'GRND', 'NUMR', 'ADVB', 'NPRO', 'PRED', 'PREP', 'CONJ', 'PRCL', 'INTJ']:
                POS_list.append(allpseudoclauses[n].POS_vector[i])
            row += POS_list
            writer.writerow(row)
        csvdata.close()
        
        # если есть разметка, то формируется целевой вектор
        if razm == 'y':
            csvtarget = open('train_target.csv', 'a', encoding='utf-8-sig')
            writer = csv.writer(csvtarget, delimiter=';', quotechar='"', lineterminator='\n', quoting=csv.QUOTE_NONNUMERIC)
            for i in disc_target:
                row = [i]
                writer.writerow(row)
            csvtarget.close()
