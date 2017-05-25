from text_to_csv import get_data
from model import get_dataframe
from contexts import go_through_texts
import os
import time

def get_all(speakers):
    start = time.time()
    texts = os.listdir('./texts')
    data = []
    target = []
    for textfile in texts:
        if textfile.endswith('.txt'):
            try:
                text = open('./texts/'+textfile,'r',encoding='cp1251').read()
            except:
                text = open('./texts/'+textfile,'r',encoding='utf-8-sig').read()
            one_data,one_target = get_data(text,textfile,speakers)
            if not data:
                data += one_data
            else:
                data += one_data[1:]
            target += one_target
    final_table = get_dataframe(data,target)
    go_through_texts(final_table,speakers)
    print('total running time:',time.time()-start)

if __name__ == '__main__':
    speakers = input('delete speakers? [y/n] ')
    if speakers == 'y':
        get_all(True)
    elif speakers == 'n':
        get_all(False)
