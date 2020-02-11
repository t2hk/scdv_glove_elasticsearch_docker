import pandas as pd
import json, argparse, glob
from elasticsearch import Elasticsearch
from elasticsearch import helpers

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str)
    parser.add_argument('--port', type=str, default='9200')
    parser.add_argument('--index', type=str)
    parser.add_argument('--input_dir', type=str)

    return parser.parse_args()

def main(args):
    csv_files = glob.glob(args.input_dir + '/*.csv')

    for csv_file in csv_files:
      situation_col_name = '災害状況'
      if 'kikaisaigai' in csv_file:
          situation_col_name = '災害発生状況'

      df = pd.read_csv(csv_file, encoding='utf-8', header=0)
      sentences = df[situation_col_name]
      categories = df['業種(大分類)_分類名']

      es = Elasticsearch(host=args.host, port=args.port)

      for col, sentence in enumerate(sentences):
         json_data = '{"category":"%s","sentence":"%s"}' % (categories[col], sentence)

         print(json_data)
         es.index(index=args.index, doc_type="_doc", body=json_data)

if __name__ == '__main__':
  main(parse_args())
