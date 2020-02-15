import pandas as pd
import json, argparse, glob
from elasticsearch import Elasticsearch
from elasticsearch import helpers

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str)
    parser.add_argument('--port', type=str, default='9200')
    parser.add_argument('--index', type=str)
    parser.add_argument('--input_csv', type=str)

    return parser.parse_args()

def main(args):
    es = Elasticsearch(host=args.host, port=args.port)
    df = pd.read_csv(args.input_csv, header=0)

    for index, row in df.iterrows():
      doc_id = row['doc_id']
      category = row['category']
      text_id = row['text_id']
      text = row['text']

      json_data = '{"doc_id":"%s","category":"%s","text_id":"%s","text":"%s"}' % (doc_id, category, text_id, text)
      print(json_data)
      es.index(index=args.index, doc_type="_doc", body=json_data)

if __name__ == '__main__':
  main(parse_args())
