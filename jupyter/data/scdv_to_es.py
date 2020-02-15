import elasticsearch
import json, argparse, scdv

class elasticsearchClient():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = elasticsearch.Elasticsearch(self.host + ":" + self.port, timeout=30)

    def update(self, index, doc_id, body):
        response = self.client.update(
                index = index, 
                id = doc_id, 
                body = body)
        print(response)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='localhost')
    parser.add_argument('--port', type=str, default='9200')
    parser.add_argument('--input_csv', type=str)

    return parser.parse_args()

def main(args):
    client = elasticsearchClient(args.host, args.port)

    scdv_vec = scdv.build_model(args.input_csv, 20, "gmm_cluster.pkl", "gmm_prob_cluster.pkl")

    for index, doc_id, text_id, category, vector in scdv_vec:
        # ベクトルが全てゼロの場合、スキップする
        if not all(vector) and not any(vector):
            continue

        if index == 'anzen':
            client.update(index, doc_id, {'doc':{'vector':vector.tolist()}})
        elif index == 'accident':
            client.update(index, doc_id, {'doc':{'scdv_vector':vector.tolist()}})

if __name__ == '__main__':
    main(parse_args())
