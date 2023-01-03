#!/bin/sh
#PBS -q full-gpu
#PBS -l select=1:ncpus=16:ngpus=8
#PBS -k doe
#PBS -j oe

RCQAFILE="all-v1.0.json.gz"
RCQAURL="http://www.cl.ecei.tohoku.ac.jp/rcqa/data/${RCQAFILE}"

SCRIPTS="run_qa.py trainer_qa.py utils_qa.py"
BASEURL="https://raw.githubusercontent.com/huggingface/transformers/v4.25.1/examples/pytorch/question-answering"

DATADIR=data/unidic
TRAINFILE=${DATADIR}/rcqa_train.json
VALIDFILE=${DATADIR}/rcqa_dev.json
TESTFILE=${DATADIR}/rcqa_test.json

MODELDIR=../bert-japanese/models/jawiki-20210301
MODELNAME=`basename ${MODELDIR}`
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

if [ ! -f ${TRAINFILE} ]; then
	mkdir -p ${DATADIR}
	cd ${DATADIR} && python3 ../../conv.py --rcqafile ../../${RCQAFILE} --unidic
fi

for f in ${SCRIPTS}; do
	if [ ! -f ${f} ]; then
		wget ${BASEURL}/${f}
	fi
done

python3 run_qa.py \
    --model_name_or_path          ${MODELDIR} \
    --output_dir                  train_output_${MODELNAME}_batch${BATCH}_lr${LR}_epochs${EPOCH} \
    --train_file                  ${TRAINFILE} \
    --validation_file             ${VALIDFILE} \
    --overwrite_cache             \
    --version_2_with_negative     \
    --do_train                    \
    --do_eval                     \
    --gradient_accumulation_steps 1 \
    --per_device_train_batch_size $((BATCH / 8)) \
    --per_device_eval_batch_size  32 \
    --learning_rate               ${LR} \
    --num_train_epochs            ${EPOCH} \
    --save_steps                  10000 \
    --fp16                        \
    --fp16_opt_level              O2

python3 run_qa.py \
    --model_name_or_path          train_output_${MODELNAME}_batch${BATCH}_lr${LR}_epochs${EPOCH} \
    --output_dir                  eval_output_${MODELNAME}_batch${BATCH}_lr${LR}_epochs${EPOCH} \
    --train_file                  ${TRAINFILE} \
    --validation_file             ${TESTFILE} \
    --overwrite_cache             \
    --version_2_with_negative     \
    --do_eval                     \
    --per_device_eval_batch_size  32
