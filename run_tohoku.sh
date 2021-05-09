#!/bin/sh

RCQAFILE="all-v1.0.json.gz"
RCQAURL="http://www.cl.ecei.tohoku.ac.jp/rcqa/data/${RCQAFILE}"

SCRIPTFILE=run_squad.py
SCRIPTURL="https://raw.githubusercontent.com/huggingface/transformers/v4.4.2/examples/legacy/question-answering/${SCRIPTFILE}"

DATADIR=data/unidic_old
TRAINFILE=rcqa_train.json
VALIDFILE=rcqa_dev.json
TESTFILE=rcqa_test.json

MODELPATH=cl-tohoku/bert-base-japanese-v2
MODELNAME=`echo ${MODELPATH}|sed s,/,-,`

BATCH=32
LR=5e-5
EPOCH=2

if [ -n "${PBS_O_WORKDIR}" ]; then
	if [ "${PBS_ENVIRONMENT}" != PBS_INTERACTIVE ]; then
		cd "${PBS_O_WORKDIR}"
	fi
fi

if [ ! -f ${RCQAFILE} ]; then
	wget ${RCQAURL}
fi

if [ ! -f ${DATADIR}/${TRAINFILE} ]; then
	mkdir -p ${DATADIR}
	cd ${DATADIR} && python3 ../../conv.py --rcqafile ../../${RCQAFILE} --oldformat --unidic
fi

if [ ! -f ${SCRIPTFILE} ]; then
	wget ${SCRIPTURL}
fi

python3 ${SCRIPTFILE} \
    --model_type                  bert \
    --model_name_or_path          ${MODELPATH} \
    --output_dir                  train_output_${MODELNAME}_batch${BATCH}_lr${LR}_epochs${EPOCH} \
    --data_dir                    ${DATADIR} \
    --train_file                  ${TRAINFILE} \
    --predict_file                ${VALIDFILE} \
    --version_2_with_negative     \
    --do_train                    \
    --do_eval                     \
    --gradient_accumulation_steps $((BATCH / 8)) \
    --per_gpu_train_batch_size    8 \
    --per_gpu_eval_batch_size     32 \
    --learning_rate               ${LR} \
    --num_train_epochs            ${EPOCH} \
    --save_steps                  10000 \
    --fp16                        \
    --fp16_opt_level              O2

python3 ${SCRIPTFILE} \
    --model_type                  bert \
    --model_name_or_path          train_output_${MODELNAME}_batch${BATCH}_lr${LR}_epochs${EPOCH} \
    --output_dir                  eval_output_${MODELNAME}_batch${BATCH}_lr${LR}_epochs${EPOCH} \
    --data_dir                    ${DATADIR} \
    --predict_file                ${TESTFILE} \
    --overwrite_cache             \
    --version_2_with_negative     \
    --do_eval                     \
    --per_gpu_eval_batch_size     32
