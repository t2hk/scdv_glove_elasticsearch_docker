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

def create_script(sentence_type, sentence_id, vector):
    script = ""

    if sentence_type == "title":
        script = '{"script":{"source":"ctx._source.title.vector = params.vector","lang":"painless","params":{"id":"' + sentence_id + '","vector":' + vector + '}}}'
    else:
        script = '{"script":{"source":"for (int i = 0; i < ctx._source.' + sentence_type + '.length; i++) {if(ctx._source.' + sentence_type + '[i].' + sentence_type + '_id == params.id) { ctx._source.' + sentence_type + '[i].vector = params.vector; break}}","lang":"painless","params":{"id":"' + sentence_id + '","vector":"' + vector + '"}}}'

    return script

def main(args):
    client = elasticsearchClient(args.host, args.port)

    scdv_vec = scdv.build_model(args.input_csv, 20, "gmm_cluster.pkl", "gmm_prob_cluster.pkl")

    for index, doc_id, sentence_id, category, vector in scdv_vec:
        if index == 'anzen':
            sentence_type = "title"

            if '_c_' in sentence_id:
                sentence_type = "cause"
            elif '_m_' in sentence_id:
                sentence_type = "measures"
            elif '_s_' in sentence_id:
                sentence_type = "situation"

            vector = str(vector.tolist())
            script = create_script(sentence_type, sentence_id, vector)
            script = script.replace('"[','[').replace(']"',']')

            client.update(index, doc_id, script)
        elif index == 'accident':
            client.update(index, doc_id, {'doc':{'scdv_vector':vector.tolist()}})

if __name__ == '__main__':
    main(parse_args())
