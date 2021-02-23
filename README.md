# NICT BERT モデルの動作確認スクリプト

[NICT によって配布されている BERTモデル](https://alaginrc.nict.go.jp/nict-bert/index.html)が，
正常に動作しているかを確認するため，
[公式の実験手順](https://alaginrc.nict.go.jp/nict-bert/Experiments_on_RCQA.html)を，
最近の transformers-4.x および datasets で動作するように移植した．

なお，動作確認が目的なので，mecab-jumandic を利用して，既に報告されて
いる最適パラメータで学習・テストするだけの形に単純化されている．

## 実行手順

```
sh run.sh
```

## 変更部分

 * RCQA を SQuAD 互換に変換するコードを，datasets 用に変更した．
 * `run_squad.py` の代わりに `run_qa.py` を使うように変更した．
