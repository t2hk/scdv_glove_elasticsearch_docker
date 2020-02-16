from elasticsearch import Elasticsearch
import json, argparse, scdv


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='localhost')
    parser.add_argument('--port', type=str, default='9200')
    parser.add_argument('--input_csv', type=str)
    parser.add_argument('--num_clusters', type=int, default=20)

    return parser.parse_args()

def main(args):
    es = Elasticsearch(host=args.host, port=args.port)
    scdv_vec = scdv.build_model(args.input_csv, args.num_clusters, "./vector/gmm_cluster.pkl", "./vector/gmm_prob_cluster.pkl")

    for index, id, text_id, category, vector in scdv_vec:
        # ベクトルが全てゼロの場合、スキップする
        if not all(vector) and not any(vector):
            continue

        #json_data = '{"doc_id":"%s","index":"%s","category":"%s","text_id":"%s","vector":"%s"}' % (id, index, category, text_id, vector.tolist())
        json_data = {"doc_id":id,"index":index,"category":category,"text_id":text_id,"vector":vector.tolist()}
        print(json_data)
        es.index(index="vector", doc_type="_doc", body=json_data)

if __name__ == '__main__':
    main(parse_args())
