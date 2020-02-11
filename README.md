# 自然言語処理用Docker環境

## 概要
GloVeによる単語ベクトル、SCDVによる文章ベクトルを活用し、類義語検索や類義文検索を行う。

## 環境

- ホスト環境

| 環境 | バージョン |
| --- | --- |
| Ubuntu | 18.04 |
| Docker | 18.09.7 |
| Docker Compose | 1.17.1 |

- Dockerイメージ

| 環境 | バージョン |
| --- | --- |
| Jupyter Lab | jupyter/datascience-notebook |
| Elasticsearch | docker.elastic.co/elasticsearch/elasticsearch:7.5.0 |
| Kibana | docker.elastic.co/kibana/kibana:7.5.0 |

## Dockerイメージ概要
  -Jupyter Lab 
    - Sudachi、Ginza導入
    - matplitlib用の日本語フォント導入

  - Elasticsearch 
    - analysis-sudachi-elasticsearch導入

## 構築方法
- Dockerをインストールする。
  ```
  $ sudo apt update
  $ sudo apt install docker docker-compose
  ```
- 初期設定を行う。
  ```
  $ ./init.sh
  ```

- docker-composeでコンテナを起動する。
  ```
  $ sudo docker-compose up
  ```

## 各環境へのアクセス方法
- Jupyter Labコンテナ
http://[ホスト]:8888

- Kibana
http://[ホスト]:5601

- Elasticsearch
http://[ホスト]:9800

## 使い方
基本的にJupyter Lab上での作業となる。

### 1. 環境の初期設定、データクローリング、GloVeとSCDVによる単語・文章のベクトル化
1. Jupyter Labコンテナにアクセスする。
2. nlp_book.ipynbを開く
3. セルの先頭から順番に実行する
   主な処理は以下の通り。
   - データクローリング
   - データの前処理
   - Elasticsearchへの登録
   - Elasticsearchによる文章のトークナイズ
   - GloVeによる単語ベクトルの生成
   - SCDVによる文章ベクトルの生成とElasticsearchへの登録

### 2. 類似語の抽出
GloVeによる単語ベクトルを使い、類似語を抽出する。

1. Similarity.ipynbを開く。
2. 最初のセルに類似語を抽出したい単語と、上位何件を取得するか変数に記述する。
   - word : 類似語を抽出したい単語
   - top_k : 上位何位まで取得するか
3. セルを実行する。

### 3. LDAトピックモデル
トークナイズした単語を使い、LDAトピックモデルによる分類を行う。

1. LDA_topic_model.ipynbを開く。
2. セルを上から順に実行する。
   - LDAトピックモデルの学習
   - 学習したトピック毎に特徴的な単語をWordCloudで可視化
   - pyLDAvisによるトピックの分布を可視化
