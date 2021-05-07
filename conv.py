#!/usr/bin/python3
# -*- coding: utf-8; -*-

import gzip
import json
import os
import sys
import io

import fugashi
import mojimoji

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

dicdir = '/var/lib/mecab/dic/juman-utf8'
rcfile = '/etc/mecabrc'
tagger = fugashi.GenericTagger(f'-r {rcfile} -d {dicdir}')
assert tagger.dictionary_info[0]['charset'] == 'utf-8'

dataset = []
with gzip.open("all-v1.0.json.gz", "rt", encoding="utf-8") as fp:
    for line in fp:
        data = json.loads(line)
        if data["documents"]:
            dataset.append(data)

train_dataset = [data for data in dataset if data["timestamp"] < "2009"]
dev_dataset = [data for data in dataset if "2009" <= data["timestamp"] < "2010"]
test_dataset = [data for data in dataset if "2010" <= data["timestamp"]]

def tokenize(line):
    line = mojimoji.han_to_zen(line).replace("\u3000", " ")
    tokens = []
    for w in tagger(line):
        try:
            tokens.append(w.surface)
        except:
            pass
    return ' '.join(tokens)

def convert(filename, datasplit):
    entries = []
    for data in datasplit:
        for i, document in enumerate(data["documents"]):
            q_id = "{}{:04d}".format(data["qid"], i + 1)
            question = tokenize(data["question"])
            answer = "".join(ch for ch in tokenize(data["answer"]) if not ch.isspace())
            context = tokenize(document["text"])
            is_impossible = document["score"] < 2
            if not is_impossible:
                context_strip, offsets = zip(*[(ch, ptr) for ptr, ch in enumerate(context) if not ch.isspace()])
                idx = "".join(context_strip).index(answer)
                answer_start, answer_end = offsets[idx], offsets[idx + len(answer) - 1]
                answer = context[answer_start:answer_end + 1]
                entries.append({'answers': {'answer_start': [answer_start], 'text': [answer]},
                                'context': context,
                                'id': q_id,
                                'question': question,
                                'title': q_id})
            else:
                entries.append({'answers': {'answer_start': [], 'text': []},
                                'context': context,
                                'id': q_id,
                                'question': question,
                                'title': q_id})
    return entries

for filename, datasplit in (("rcqa_train.json", train_dataset),
                            ("rcqa_dev.json", dev_dataset),
                            ("rcqa_test.json", test_dataset)):
    entries = convert(filename, datasplit)
    with open(filename, "w", encoding="utf-8") as fp:
        json.dump({"data": entries}, fp, ensure_ascii=False)
