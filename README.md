# 自然言語処理用Docker環境

## 概要
GloVeによる単語ベクトル、SCDVによる文章ベクトルを活用し、類義語検索や類義文検索を行う。
環境はJupyter Lab、DBはElasticsearchを使用している。

## 環境

- ホスト環境

| 環境 | バージョン |
| --- | --- |
| Ubuntu | 18.04 |
| Docker | 19.03.5 |
| Docker Compose | 1.25.0 |

- Dockerイメージ

| 環境 | バージョン |
| --- | --- |
| Jupyter Lab | jupyter/datascience-notebook |
| Elasticsearch | docker.elastic.co/elasticsearch/elasticsearch:7.5.0 |
| Kibana | docker.elastic.co/kibana/kibana:7.5.0 |

## Dockerイメージ概要
  - Jupyter Lab
    * 機械学習用の各種ツールを導入
    * Sudachi、Ginzaを導入
    * matplitlib用の日本語フォントを導入

  - Elasticsearch
    * analysis-sudachi-elasticsearchを導入

## 構築方法
- Dockerをインストールする。
  ```
  $ sudo apt update
  $ sudo apt install docker docker-compose
  ```
- 初期設定を行う。ホスト側で以下を実行する。

  必要なディレクトリの作成やツールのダウンロードを行う。
  ```
  $ ./init.sh
  ```

- docker-composeでコンテナを起動する。

  JupyterLab、Elasticsearch、Kibanaのコンテナが起動する。
  ```
  $ sudo docker-compose up
  ```

## 各環境へのアクセス方法
各コンテナへのアクセスは以下の通りである。

| コンテナ | ホストからのアクセス | コンテナ間のアクセス |
| --- | --- | --- |
| Jupyter Lab | http://[ホスト]:8888 | - |
| Kibana | http://[ホスト]:5601 | http://kibana:5601 |
| Elasticsearchコンテナ | http://[ホスト]:9200 | http://elasticsearch:9200 |

## データの保存場所
各コンテナのデータはホスト側に永続するように設定しており、以下のディレクトリに保存される。

| コンテナ | ホスト側の保存場所 |
| --- | --- |
| Jupyter Lab | ./jupyter/data/ |
| Elasticsearch | ./elasticsearch/es-data |

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

### 4. 類似文書の検索
GloVeを使用したSCDVによる類似文書検索を行う。Elasticsearchのvectorフィールドを使用したcosineSimilarityによる類似検索の例である。

1. Elasticsearch_sim_search.ipyを開く。
2. セルを上から順に実行する。
