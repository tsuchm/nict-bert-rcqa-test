# BERT モデルの動作確認スクリプト

[解答可能性付き読解データセット](http://www.cl.ecei.tohoku.ac.jp/rcqa/)を例題として，BERTモデルが正常に動作しているかを確認するための実験手順をまとめているリポジトリ．

## NICT BERT モデル

[NICT によって配布されている BERT モデル](https://alaginrc.nict.go.jp/nict-bert/index.html)が，正常に動作しているかを確認するため，
[公式の実験手順](https://alaginrc.nict.go.jp/nict-bert/Experiments_on_RCQA.html)を，最近の transformers-4.x および datasets で動作するように移植した．移植による変更箇所は以下の2点．

 * RCQA を SQuAD 互換に変換するコードを，datasets 用に変更．
 * `run_squad.py` の代わりに `run_qa.py` を使うように変更．

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
***** eval metrics *****
  eval_HasAns_exact      = 72.9782
  eval_HasAns_f1         = 75.8301
  eval_HasAns_total      =    3079
  eval_NoAns_exact       = 81.8006
  eval_NoAns_f1          = 81.8006
  eval_NoAns_total       =    3099
  eval_best_exact        = 77.4199
  eval_best_exact_thresh =     0.0
  eval_best_f1           = 78.8412
  eval_best_f1_thresh    =     0.0
  eval_exact             = 77.4037
  eval_f1                =  78.825
  eval_samples           =    6181
  eval_total             =    6178
```

## 自家製 BERT モデル

[自家製 BERT モデル](https://github.com/tutcsis/bert-japanese)が，正常に動作しているかを確認する手順．
このリポジトリと同一階層のディレクトリに，[自家製 BERT モデル](https://github.com/tutcsis/bert-japanese)を checkout して学習が完了しているという想定．

```sh
sh run_jawiki.sh
```

または，以下のようにバッチジョブとして投入する．

```sh
qsub -q full-gpu -l select=1:ncpus=16:ngpus=8 run_jawiki.sh
```

ハイパーパラメータの探索は行っていないが，東北大 BERT モデルとほぼ同等の性能が出るはずである．

```
***** eval metrics *****
  eval_HasAns_exact      = 68.2364
  eval_HasAns_f1         = 71.3658
  eval_HasAns_total      =    3079
  eval_NoAns_exact       = 83.3817
  eval_NoAns_f1          = 83.3817
  eval_NoAns_total       =    3099
  eval_best_exact        = 75.8336
  eval_best_exact_thresh =     0.0
  eval_best_f1           = 77.3932
  eval_best_f1_thresh    =     0.0
  eval_exact             = 75.8336
  eval_f1                = 77.3932
  eval_samples           =    6183
  eval_total             =    6178
```

## 自家製 RoBERTa モデル

[自家製 RoBERTa モデル](https://github.com/tutcsis/roberta-japanese)が，正常に動作しているかを確認する手順．
このリポジトリと同一階層のディレクトリに，[自家製 RoBERTa モデル](https://github.com/tutcsis/roberta-japanese)を checkout して学習が完了しているという想定．

```sh
sh run_roberta.sh
```

または，以下のようにバッチジョブとして投入する．

```sh
qsub -q full-gpu -l select=1:ncpus=16:ngpus=8 run_roberta.sh
```

ハイパーパラメータの探索は行っていないが，東北大 BERT モデルとほぼ同等の性能が出るはずである．

```
***** eval metrics *****
  eval_HasAns_exact      =  71.127
  eval_HasAns_f1         = 75.6204
  eval_HasAns_total      =    3079
  eval_NoAns_exact       = 67.5702
  eval_NoAns_f1          = 67.5702
  eval_NoAns_total       =    3099
  eval_best_exact        =  69.359
  eval_best_exact_thresh =     0.0
  eval_best_f1           = 71.5876
  eval_best_f1_thresh    =     0.0
  eval_exact             = 69.3428
  eval_f1                = 71.5822
  eval_samples           =    6181
  eval_total             =    6178
```

## 東北大 BERT モデル

[東北大によって配布されている BERT モデル](https://huggingface.co/cl-tohoku/bert-base-japanese-v2)が，正常に動作しているかを確認するための手順．実行手順は以下の通り．

```sh
sh run_tohoku.sh
```

または，以下のようにバッチジョブとして投入する．

```sh
qsub -q one-gpu -l select=1:ncpus=2:ngpus=1 run_tohoku.sh
```

以下のような性能が得られるはずである．

```
{'exact': 77.87309808999676,
 'f1': 79.40088750010351,
 'total': 6178,
 'HasAns_exact': 70.96459889574537,
 'HasAns_f1': 74.03010164847016,
 'HasAns_total': 3079,
 'NoAns_exact': 84.73701193933528,
 'NoAns_f1': 84.73701193933528,
 'NoAns_total': 3099,
 'best_exact': 77.90547102622207, 
 'best_exact_thresh': 0.0,
 'best_f1': 79.4332604363289, 
 'best_f1_thresh': 0.0}
```

NICT BERTモデルとは異なり，東北大 BERT モデルの tokenizer は，BertTokenizerFast を継承していないので，以前の `run_squad.py` を改変して使用．ただし，並列学習にバグがあるらしく，複数 GPU を用いるとエラーになる．
