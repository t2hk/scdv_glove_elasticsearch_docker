import pandas as pd
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_anzen', type=str)
    parser.add_argument('--input_accident', type=str)
    parser.add_argument('--output_csv', type=str)

    return parser.parse_args()

def main(args):
    anzen_csv = args.input_anzen
    accident_csv = args.input_accident
    merge_csv = args.output_csv

    anzen_df = pd.read_csv(anzen_csv)
    accident_df = pd.read_csv(accident_csv)

    # accidentインデックスのデータのIDと分かち書きのみ取得し、INDEX列を追加する
    new_accident_df = accident_df.drop('sentence', axis=1).assign(index = 'accident').assign(sentence_id = 0)

    new_anzen_df = anzen_df.rename(columns={'種別':'category'}).drop('文章', axis=1).assign(index = 'anzen')
    new_anzen_df = new_anzen_df.rename(columns={'文章ID':'sentence_id'}).rename(columns={'分かち書き':'tokens'})

    merge_df = pd.concat([new_anzen_df, new_accident_df], sort=False)
    merge_df.to_csv(merge_csv, encoding='utf_8')

if __name__ == '__main__':
    main(parse_args())
