import os
import re

import pandas as pd

def main():
    path = "./"
    list_review = [i for i in os.listdir(path) \
        if 'ulasan-' in i and i.endswith('.csv')]
    
    list_a = []
    list_b = []
    list_c = []
    
    for review in list_review:
        df = pd.read_csv(review)
        
        list_review = df['Ulasan'].values.tolist()
        list_rating = df['Rating'].values.tolist()

        nama_tempat_wisata = ' '.join(re.split('-|\\.', review)[1:-1])
        list_nama_objek_wisata = [nama_tempat_wisata] * len(list_review)
    
        list_a += list_nama_objek_wisata
        list_b += list_review
        list_c += list_rating
    
    df_final = pd.DataFrame({
        'nama_objek_wisata': list_a,
        'review': list_b,
        'rating': list_c})

    file_name = 'set-reviews.csv'
    df_final.to_csv(file_name, index=False)

if __name__ == "__main__":
    main()