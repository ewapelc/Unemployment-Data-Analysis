import pandas as pd
import numpy as np
import os
import csv
import argparse

def process(input_dir, output_file):
    # check if file already exists, if yes remove
    file_path = output_file
    if os.path.exists(file_path):
        os.remove(file_path)
        print('File removed succesfully!')
    
    # create new file, and insert headers
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        headers = ['date', 'value']
        writer.writerow(headers)

    for file in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file)
        print(f"Processing\t {file}")
        df = pd.read_csv(file_path, sep=';')
        nazwa_przekroj = df.loc[0, 'nazwa_przekroj']
        df = df[df.nazwa_przekroj == nazwa_przekroj]
        df = df[['zmienna', 'nazwa_pozycja_5', 'opis_okres', 'wartosc']]
        df['wartosc'] = df['wartosc'].str.replace(',', '.').astype('float')

        mask = ~df[['nazwa_pozycja_5', 'opis_okres']].duplicated()
        df = df[mask]
        df['opis_okres'] = df['opis_okres'].str.replace(' M', '-')
        df['opis_okres'] = df['opis_okres'] + '-01'
        d = round(df.groupby(['opis_okres'])['wartosc'].mean(), 2)
        d = d.to_frame()

        d.to_csv(output_file, mode='a', index=True, header=False)

if __name__ == "__main__":
    # create parser for arguments
    parser = argparse.ArgumentParser(description='Process some data.')
    parser.add_argument('--input_dir', help='Ścieżka do katalogu z plikami wejściowymi')
    parser.add_argument('--output_file', help='Ścieżka do pliku wyjściowego')

    # parse arguments from command line
    args = parser.parse_args()

    # preprocess data with given arguments
    process(args.input_dir, args.output_file)



