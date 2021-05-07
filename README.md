# BERT モデルの動作確認スクリプト

## NICT BERT モデル

[NICT によって配布されている BERTモデル](https://alaginrc.nict.go.jp/nict-bert/index.html)が，正常に動作しているかを確認するため，
[公式の実験手順](https://alaginrc.nict.go.jp/nict-bert/Experiments_on_RCQA.html)を，最近の transformers-4.x および datasets で動作するように移植した．
移植による変更箇所は以下の2点．

 * RCQA を SQuAD 互換に変換するコードを，datasets 用に変更した．
 * `run_squad.py` の代わりに `run_qa.py` を使うように変更した．

なお，動作確認が目的なので，mecab-jumandic を利用して，既に報告されている最適パラメータで学習・テストするだけの形に単純化されている．

実行手順は以下の通り．

```sh
sh run.sh
```

または，以下のようにバッチジョブとして投入する．

```sh
qsub -q full-gpu -l select=1:ncpus=16:ngpus=8 run.sh 
```

以下のような性能が得られるはずである．

```
***** Eval results *****
  HasAns_exact = 71.6791165962975
  HasAns_f1 = 74.75169513952163
  HasAns_total = 3079
  NoAns_exact = 82.9945143594708
  NoAns_f1 = 82.9945143594708
  NoAns_total = 3099
  best_exact = 77.37131757850437
  best_exact_thresh = 0.0
  best_f1 = 78.90263343065514
  best_f1_thresh = 0.0
  exact = 77.35513111039171
  f1 = 78.88644696254237
  total = 6178
```

## 東北大 BERT モデル

[東北大によって配布されている BERTモデル](https://huggingface.co/cl-tohoku/bert-base-japanese-v2)が，正常に動作しているかを確認するための手順．実行手順は以下の通り．

```sh
sh run_tohoku.sh
```

または，以下のようにバッチジョブとして投入する．

```sh
qsub -q one-gpu -l select=1:ncpus=2:ngpus=1 run_tohoku.sh
```
