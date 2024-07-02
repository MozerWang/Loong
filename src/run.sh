#!/bin/bash

# MODEL
MODEL="gpt4o"
MODEL_CONFIG="$MODEL.yaml"
EVAL_MODEL_CONFIG="gpt4.yaml"
# INPUT PATH
DOC_PATH="../data/doc"
INPUT_PATH="../data/loong.jsonl"
MODEL_CONFIG_DIR="../config/models"
# OUTPUT PATH
OUTPUT_PROCESS_PATH="../data/loong_process.jsonl"
OUTPUT_PATH="../output/$MODEL/loong_generate.jsonl"
OUTPUT_EVALUATE_PATH="../output/$MODEL/loong_evaluate.jsonl"
# ARGUMENTS
MAX_LENGTH="120000" # According to the context window of llm
PROCESS_NUM="1" # Concurrency number of generate function
DEBUG_NUM="-1" # -1 means all data


ARGS="--models $MODEL_CONFIG --eval_model $EVAL_MODEL_CONFIG --debug_num $DEBUG_NUM --doc_path $DOC_PATH --input_path $INPUT_PATH --output_process_path $OUTPUT_PROCESS_PATH --output_path $OUTPUT_PATH --evaluate_output_path $OUTPUT_EVALUATE_PATH --max_length $MAX_LENGTH --model_config_dir $MODEL_CONFIG_DIR --process_num $PROCESS_NUM"

# Execute in order
python step1_load_data.py $ARGS
python step2_model_generate.py $ARGS
python step3_model_evaluate.py $ARGS
python step4_cal_metric.py $ARGS
