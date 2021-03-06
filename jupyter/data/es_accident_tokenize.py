import elasticsearch
import json, argparse, scdv

class elasticsearchClient():
    def __init__(self, host, port, index):
        self.host = host
        self.port = port
        self.index = index
        self.client = elasticsearch.Elasticsearch(self.host + ":" + self.port)

    # sentenceをトークナイズする。
    def tokenize(self, sentence):
        body_ = {"analyzer": "sudachi_analyzer", "text": sentence}
        json_tokens = self.client.indices.analyze(
                index = self.index, body=body_)

        tokens = [token['token'] for token in json_tokens['tokens']]
        return tokens

    def parse_data(self, items):
        results = []

        for item in items:
            index = json.dumps(item['_id'])
            category = json.dumps(
                    item['_source']['category'], 
                    indent=2, ensure_ascii=False)
            sentence = json.dumps(
                    item['_source']['sentence'], 
                    indent=2, ensure_ascii=False)

            tokens = self.tokenize(sentence)
            results.append((index, category, sentence, tokens))
        return results

    # 全データを取得する
    def get_all_data(self, scroll_time, scroll_size):
        results = []

        data = self.client.search(
                index = self.index,
                scroll = scroll_time,
                size = scroll_size,
                body = {})
        sid = data['_scroll_id']
        scroll_size = len(data['hits']['hits'])

        results = self.parse_data(data['hits']['hits'])

        while scroll_size > 0:
            data = self.client.scroll(
                    scroll_id = sid, 
                    scroll = scroll_time)

            sid = data['_scroll_id']
            scroll_size = len(data['hits']['hits'])
            scroll_results = self.parse_data(data['hits']['hits'])
            results.extend(scroll_results)

        return results
    def update(self, row_id, body):
        response = self.client.update(
                index = self.index, 
                id = row_id, 
                body = body)
        print(response)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str)
    parser.add_argument('--port', type=str, default='9200')
    parser.add_argument('--index', type=str)
    parser.add_argument('--output', type=str)
    parser.add_argument('--scroll_limit', type=str, default='1m')
    parser.add_argument('--scroll_size', type=int, default=100)

    return parser.parse_args()

def main(args):
    client = elasticsearchClient(args.host, args.port, args.index)
    results = client.get_all_data(args.scroll_limit, args.scroll_size)

    output_txt = args.output + '.txt'
    output_csv = args.output + '.csv'
    with open(output_csv, "w") as f_csv:
        with open(output_txt, "w") as f_txt:
            f_csv.writelines('ID,category,sentence,tokens\n')

            for result in results:
                tokens = " ".join(result[3])
                f_csv.writelines(result[0] + ',' + result[1] + ',' + result[2] + ',"' + tokens + '"\n')
                f_txt.writelines(tokens + '\n')

if __name__ == '__main__':
    main(parse_args())
