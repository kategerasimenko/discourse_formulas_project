import numpy as np 
import pandas as pd
from scipy.sparse import csr_matrix, hstack, vstack
from collections import Counter

def get_dataframe(table,cv_cum):
    headers = table.pop(0)
    data = pd.DataFrame(table,columns=headers)
    cv_cum = np.array(cv_cum)
    
    all_formulas = data[cv_cum == 1]['Text']
    unique_formulas = Counter(all_formulas).most_common()
    
    st1 = ('всего уникальных формул: '+str(len(unique_formulas)),'')
    st2 = (str(round((len(unique_formulas) / len(all_formulas)) * 100,1))+'% всех формул','')
    unique_formulas = [st1,st2] + list(unique_formulas)
    print(len(unique_formulas))
    final = pd.concat((data[['Text_id','Text']].reset_index(drop=True),
                       pd.DataFrame(cv_cum),
                       pd.DataFrame([x[0] for x in unique_formulas]),
                       pd.DataFrame([x[1] for x in unique_formulas])), axis = 1)
    return final.values.tolist()
    
