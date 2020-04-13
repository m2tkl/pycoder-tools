# pycoder-tools <img alt="Run pytest" src="https://github.com/kenchalros/pycoder-tools/workflows/Python application/badge.svg"></a>

pythonでatcoderやるときに便利なスクリプトです。  
テストケースのコピペから開放されます。  

## 目次

- [概要](#概要)
- [準備](#準備)
  - [設定ファイルの作成](#設定ファイルの作成)
  - [ディレクトリ構成](#ディレクトリ構成)
- [使い方](#使い方)
  - [コンテストの準備](#コンテストの準備)
  - [テストの実行](#テストの実行)
  - [テストケースの追加](#テストケースの追加)
  - [ソースコード提出](#ソースコード提出)

## 概要

### できること
- コンテスト用のディレクトリ、ファイル作成
- サンプルテストケースの取得
- テストケースの追加
- ソースコードの提出

### できないこと（現在）
- テストの実行時間計測
- ~解答の提出~ -> `judge.py`にてオプション指定で提出できるようになりました。
- ~abc以外のコンテストでの利用~ -> arcでも利用できます（agcは確認してないです）

など。（そのうちできるように頑張ります。）

## 準備

### 外部ライブラリのインストール
```
pipenv install
```
pipenvがない場合はpipenvの導入をお願いします．

### 設定ファイルの作成
`pycoder-tools`ディレクトリ直下に`config.py`というファイルを作成します。
```python
USERNAME = 'hoge'
PASSWORD = 'fuga'
ATCODER_DIR_PATH = 'piyo' # ex: '/Users/hoge/Documents/atcoder/'
```
`USERNAME`、`PASSWORD`はatcoderの問題ページからサンプルテストケースを取得する際に必要になります。
`ATCODER_DIR_PATH`はatcoderを管理している自分のディレクトリへのパスを指定します。  
（`config.py`はgit管理から外しています。）

### ディレクトリ構成
ディレクトリ構成は以下のようになります。  
`xxx`にはコンテストの番号が入ります。  
`tests/x/...`にはテストケースが入ります。  

```txt
atcoder/ABC/xxx/A.py
                B.py
                C.py
                D.py
                E.py
                F.py
                tests/A/...
                      B/...
                      C/...
                      D/...
                      E/...
                      F/...
       
       /ARC/...
       
       /AGC/...
```

## 使い方
仮想環境に入る．
```
pipenv shell
```
仮想環境から出る．
```
exit
```

### コンテストの準備
`pycode.py`を実行するとコンテスト用のディレクトリ準備とサンプルテストケースの取得を行います。

![スクリーンショット 0002-04-02 午後6 10 49](https://user-images.githubusercontent.com/37099863/78231139-5340c600-750d-11ea-99cd-07bcb4f1dfd8.png)

![スクリーンショット 0002-04-02 午後5 02 49](https://user-images.githubusercontent.com/37099863/78224661-e1b04a00-7503-11ea-9506-0084864e5c9c.png)

### テストの実行
`judge.py`を実行するとテストができます。`-v`オプションで入力と出力も表示できます。

![スクリーンショット 0002-04-02 午後6 12 02](https://user-images.githubusercontent.com/37099863/78231266-7f5c4700-750d-11ea-92db-dbf0231ce671.png)

間違えた場合は期待された出力と実際の出力を表示します。
![スクリーンショット 0002-04-02 午後6 13 02](https://user-images.githubusercontent.com/37099863/78231354-a286f680-750d-11ea-9b1d-9c0a3939fa94.png)

問題の中には、出力との誤差がある値以下かどうかを判定に使うものがありますが、`-d`オプションを指定することでテストできます。  
詳しくは`-h`オプションで確認してみてください。

### テストケースの追加
`testmake.py`は`pycode.py`によってサンプルテストケース入手の際に呼び出されますが、
`testmake.py`をオプション`-a`指定で実行するとテストケースを追加することができます。  
`Input:`、`Output:`のあとにそれぞれ入力し、改行（Enter）で入力を終了します。

![スクリーンショット 0002-04-02 午後6 05 28](https://user-images.githubusercontent.com/37099863/78230677-9ea6a480-750c-11ea-95fd-fa74cb715c0c.png)

追加したテストケースも`judge.py`により実行されます。

![スクリーンショット 0002-04-02 午後6 08 50](https://user-images.githubusercontent.com/37099863/78230951-0e1c9400-750d-11ea-9115-b878f8faa9c7.png)

### ソースコード提出
`judge.py`実行時に`-s`オプションを指定することで、テストケースに全て通った場合にソースコードを提出します。
オプション引数には`p`と`pp`を指定することができ、`p`を指定すると`Python3`で、`pp`を指定するとPyPy3で提出します。

![スクリーンショット 0002-04-03 午前2 17 06](https://user-images.githubusercontent.com/37099863/78278650-4e056a80-7551-11ea-92f3-ba28004b53f8.png)
