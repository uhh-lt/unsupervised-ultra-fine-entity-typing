#!/bin/bash 

# path of python
PYTHONBIN=/home/sevgili/anaconda3-2020-11/envs/unsupervisedufet-env/bin/python3.7
OUTDIR="predictions_jobimtext"


# ##################################
# ## run with best parameters test
# ##################################

# since the best scored one headword, the features tried on it.
echo "predictions of headword for unsupervised ultra-fine entity typing with prepro, include isas, mention sim, 50,50"
# ngram and first do not matter in the below config
# --weighted-average is not given
$PYTHONBIN open_type_et_with_jobimtext.py \
--model all-mpnet-base-v2 \
--file-path ../open_type/release/crowd/test.json \
--types-file-path ../open_type/release/ontology/types.txt \
--include-isas \
--number-of-isas 10 \
--number-of-predictions 10 \
--number-of-terms-in-cluster 10 \
--ngram 0 \
--first \
--not-use-sklearn \
--headword \
--apply-preprocess \
--apply-postprocess \
--not-lowerize \
--cluster-type "50,50" \
--not-analyse \
--include-mention-sim \
--not-include-mention \
--output-file-path $OUTDIR/predictions_test_open_type_with_jobimtext_headword_prepro_includeisas_inclmentionsim_5050.json \
--log-file $OUTDIR/predictions_test_open_type_with_jobimtext_headword_prepro_includeisas_inclmentionsim_5050.log \
--args-file $OUTDIR/args_test_open_type_with_jobimtext_headword_prepro_includeisas_inclmentionsim_5050.json


