from feature_extraction import *
import re
import html

def get_data(rawtext,filename,delete_speakers):
    data = [['Text_id', 'Text']]
    
    rawtext = html.unescape(rawtext)
    if delete_speakers:
        rawtext = PREP_delete_speakers(rawtext)
    linedtext = TextByLines(rawtext)
    allpseudoclauses_raw = []
    allpseudoclauses = []
    disc_target = []

    for j in linedtext.lines:
        curlinesplitted = splitbylist(j, ['.',',','?','!',' - ',':',';','(',')', '\n','…','"','—',' – ','»'])
        for i in curlinesplitted:
            if re.findall('[А-яЁё]', i, flags=re.DOTALL):
                disc, i = is_discourse(i.strip())
                disc_target.append(disc)
                allpseudoclauses.append(i)

    for n in range(len(allpseudoclauses)):
        new_words = allpseudoclauses[n].strip('.,?!-:;()…"—–«»{}').strip()
        row = [filename[:-4], new_words]
        data.append(row)
    return data, disc_target

