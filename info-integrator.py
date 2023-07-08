import os
import re

import pandas as pd

def main():
    path = "./"
    list_info = [i for i in os.listdir(path) \
        if 'info-' in i and i.endswith('.csv')]
    
    list_a = []
    list_b = []
    list_c = []
    
    for info in list_info:
        df = pd.read_csv(info)
        list_nama_objek_wisata = []
        list_amenitas = []
        list_nama_amenitas = []
        for c in df.columns:
            list_tmp =  [x for x in df[c].values if x == x]
            list_amenitas += ([c.lower()] * len(list_tmp))
            list_nama_amenitas += list_tmp
        nama_tempat_wisata = ' '.join(re.split('-|\\.', info)[1:-1])
        list_nama_objek_wisata = [nama_tempat_wisata] * len(list_amenitas)

        list_a += list_nama_objek_wisata
        list_b += list_amenitas
        list_c += list_nama_amenitas
    
    df_final = pd.DataFrame({
        'nama_objek_wisata': list_a,
        'amenitas': list_b,
        'nama_amenitas': list_c})

    file_name = 'set-info.csv'
    df_final.to_csv(file_name, index=False)

if __name__ == "__main__":
    main()