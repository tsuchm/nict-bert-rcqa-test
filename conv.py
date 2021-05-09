#!/usr/bin/python3
# -*- coding: utf-8; -*-

import gzip
import json
import os
import sys
import io

import fugashi
import unidic_lite
import mojimoji
import unicodedata

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

tagger = False
def common_tokenize(line):
    tokens = []
    for w in tagger(line):
        try:
            tokens.append(w.surface)
        except:
            pass
    return ' '.join(tokens)

def juman_tokenize(line, tagger=False):
    return common_tokenize(mojimoji.han_to_zen(line).replace("\u3000", " "))

def unidic_tokenize(line, tagger=False):
    return common_tokenize(unicodedata.normalize("NFKC", line))

def convert(datasplit, tokenizer, oldformat):
    entries = []
    for data in datasplit:
        for i, document in enumerate(data["documents"]):
            q_id = "{}{:04d}".format(data["qid"], i + 1)
            question = tokenizer(data["question"])
            answer = "".join(ch for ch in tokenizer(data["answer"]) if not ch.isspace())
            context = tokenizer(document["text"])
            is_impossible = document["score"] < 2
            if not is_impossible:
                context_strip, offsets = zip(*[(ch, ptr) for ptr, ch in enumerate(context) if not ch.isspace()])
                idx = "".join(context_strip).index(answer)
                answer_start, answer_end = offsets[idx], offsets[idx + len(answer) - 1]
                answer = context[answer_start:answer_end + 1]
            if not oldformat:
                entries.append({'answers': {'answer_start': [answer_start] if not is_impossible else [],
                                            'text': [answer] if not is_impossible else []},
                                'context': context,
                                'id': q_id,
                                'question': question,
                                'title': q_id})
            else:
                entries.append({"title": q_id,
                                "paragraphs": [{"context": context,
                                                "qas": [{"id": q_id,
                                                         "question": question,
                                                         "is_impossible": is_impossible,
                                                         "answers": [{"text": answer, "answer_start": answer_start}]
                                                         if not is_impossible else []}]}]})
    return entries

def parse_args():
    import argparse as ap
    p = ap.ArgumentParser()
    p.add_argument('--rcqafile', type=str, default="all-v1.0.json.gz")
    p.add_argument('--dicdir')
    p.add_argument('--rcfile')
    p.add_argument('--unidic', action='store_true')
    p.add_argument('--oldformat', action='store_true')
    return p.parse_args()

def main():
    args = parse_args()

    if args.unidic:
        dicdir = args.dicdir or unidic_lite.DICDIR
        rcfile = os.path.join(dicdir, 'mecabrc')
        tokenizer = unidic_tokenize
    else:
        dicdir = args.dicdir or '/var/lib/mecab/dic/juman-utf8'
        rcfile = args.rcfile or '/etc/mecabrc'
        tokenizer = juman_tokenize
    assert dicdir and rcfile

    global tagger
    tagger = fugashi.GenericTagger(f'-r {rcfile} -d {dicdir}')
    charset = tagger.dictionary_info[0]['charset']
    assert charset == 'utf-8' or charset == 'utf8'

    dataset = []
    with gzip.open(args.rcqafile, "rt", encoding="utf-8") as fp:
        for line in fp:
            data = json.loads(line)
            if data["documents"]:
                dataset.append(data)

    train_dataset = [data for data in dataset if data["timestamp"] < "2009"]
    dev_dataset = [data for data in dataset if "2009" <= data["timestamp"] < "2010"]
    test_dataset = [data for data in dataset if "2010" <= data["timestamp"]]

    for filename, datasplit in (("rcqa_train.json", train_dataset),
                                ("rcqa_dev.json", dev_dataset),
                                ("rcqa_test.json", test_dataset)):
        entries = convert(datasplit, tokenizer, args.oldformat)
        with open(filename, "w", encoding="utf-8") as fp:
            json.dump({"data": entries}, fp, ensure_ascii=False)

if __name__ == '__main__':
    main()
